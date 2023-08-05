import sys

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import vtk

import vmi

tr = QObject()
tr = tr.tr


class PolyActor(QObject, vmi.Menu, vmi.Mouse):
    def __init__(self, view: vmi.View, name=None):
        QObject.__init__(self)

        self.name = name if name else tr('物体 （Poly)')
        vmi.Menu.__init__(self, name=self.name)

        vmi.Mouse.__init__(self)
        for b in self.mouse:
            for e in self.mouse[b]:
                if e == 'Enter':
                    self.mouse[b][e] = self.mouseEnter
                elif e == 'Leave':
                    self.mouse[b][e] = self.mouseLeave
                elif e == 'Press':
                    self.mouse[b][e] = self.mousePress
                elif e == 'PressMoveRelease':
                    self.mouse[b][e] = self.mouseRelease
                elif e == 'PressRelease':
                    self.mouse[b][e] = self.mouseRelease

        self.view = view
        self._Mapper = vtk.vtkPolyDataMapper()
        self._Prop = vtk.vtkActor()
        self._Prop._Prop = self
        self.view._Renderer.AddActor(self._Prop)

        self._Property: vtk.vtkProperty = self._Prop.GetProperty()
        self._RGB, self._Alpha = [0.5, 0.5, 0.5], 1.0
        self.color()
        self._Pickable = False
        self.pickable()
        self._Shade = True
        self.shade(True)
        self._AlwaysOnTop = False
        self.alwaysOnTop(False)

        self._Dataset = vtk.vtkPolyData()
        self._BindDataset = self
        self.bindDataset()

    def __setstate__(self, s):
        self.__init__(s['view'], s['name'])
        self.__dict__.update(s)
        s = self.__dict__

        self._Dataset.DeepCopy(vmi.loads(s['_Dumps']['_Dataset']))
        del s['_Dumps']

        for kw in s['_VTKGets']:
            vmi.vtkset(getattr(self, kw), s['_VTKGets'][kw])
        del s['_VTKGets']

        self.bindDataset()

    def __getstate__(self):
        s = self.__dict__.copy()
        for kw in ['menu', 'actions', '__METAOBJECT__']:
            if kw in s:
                del s[kw]

        s['_Dumps'] = {'_Dataset': vmi.dumps(self._Dataset)}
        for kw in s['_Dumps']:
            del s[kw]

        s['_VTKGets'] = {name: vmi.vtkget(getattr(self, name)) for name in
                         ['_Mapper', '_Prop', '_Property']}
        for kw in s['_VTKGets']:
            del s[kw]
        return s

    def dataset(self):
        return self._BindDataset._Dataset

    def bindDataset(self, other=None):
        if hasattr(other, '_Dataset'):
            self._BindDataset = other
        self._Mapper.SetInputData(self.dataset())
        self._Prop.SetMapper(self._Mapper)
        self.view.updateInTime()

    def clone(self, other):
        if other is None:
            self.dataset().ShallowCopy(self.dataset().__class__())
        elif hasattr(other, '_Dataset'):
            self.dataset().ShallowCopy(other.dataset())
        elif isinstance(other, self.dataset().__class__):
            self.dataset().ShallowCopy(other)
        else:
            raise TypeError(type(other))

    def alwaysOnTop(self, arg=None):
        self.view.updateInTime()
        if arg is True:
            self._AlwaysOnTop = True
            self._Mapper.SetRelativeCoincidentTopologyLineOffsetParameters(0, -66000)
            self._Mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(0, -66000)
            self._Mapper.SetRelativeCoincidentTopologyPointOffsetParameter(-66000)
        elif arg is False:
            self._AlwaysOnTop = False
            self._Mapper.SetRelativeCoincidentTopologyLineOffsetParameters(-1, -1)
            self._Mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(-1, -1)
            self._Mapper.SetRelativeCoincidentTopologyPointOffsetParameter(-1)
        return self._AlwaysOnTop

    def color(self, rgb=None, alpha=None):
        self.view.updateInTime()
        if rgb is not None:
            self._RGB = rgb
        if alpha is not None:
            self._Alpha = alpha
        self._Property.SetColor(self._RGB)
        self._Property.SetOpacity(self._Alpha)
        return {'rgb': self._RGB, 'alpha': self._Alpha}

    def colorLight(self):
        c = QColor()
        c.setRgbF(self._RGB[0], self._RGB[1], self._RGB[2])
        c = c.lighter(120)
        self._Property.SetColor(c.redF(), c.greenF(), c.blueF())
        self.view.updateInTime()

    def colorDark(self):
        c = QColor()
        c.setRgbF(self._RGB[0], self._RGB[1], self._RGB[2])
        c = c.darker(120)
        self._Property.SetColor(c.redF(), c.greenF(), c.blueF())
        self.view.updateInTime()

    def colorNormal(self):
        self._Property.SetColor(self._RGB)
        self.view.updateInTime()

    def delete(self):
        self._Dataset.ReleaseData()
        self.view._Renderer.RemoveActor(self._Prop)

    def pickable(self, arg=None):
        if arg is True:
            self._Pickable = True
        elif arg is False:
            self._Pickable = False
        self._Prop.SetPickable(1 if self._Pickable else 0)
        self.view.updateInTime()
        return self._Pickable

    def rep(self, arg=None):
        self.view.updateInTime()
        if isinstance(arg, str):
            if arg.lower() == 'points':
                self._Property.SetRepresentationToPoints()
            elif arg.lower() == 'wireframe':
                self._Property.SetRepresentationToWireframe()
            elif arg.lower() == 'surface':
                self._Property.SetRepresentationToSurface()
            elif arg.lower() == 'toggle':
                r = (self._Property.GetRepresentation() + 1) % 3
                self.rep(('points', 'wireframe', 'surface')[r])
        return ('points', 'wireframe', 'surface')[self._Property.GetRepresentation()]

    def shade(self, arg=None):
        self.view.updateInTime()
        if arg is True:
            self._Shade = True
            self._Property.SetAmbient(0)
            self._Property.SetDiffuse(1)
        elif arg is False:
            self._Shade = False
            self._Property.SetAmbient(1)
            self._Property.SetDiffuse(0)
        return self._Shade

    def size(self, **kwargs):
        self.view.updateInTime()
        if 'point' in kwargs:
            self._Property.SetPointSize(kwargs['point'])
        if 'line' in kwargs:
            self._Property.SetLineWidth(kwargs['line'])
        return {'point': self._Property.GetPointSize(),
                'line': self._Property.GetLineWidth()}

    def mouseEnter(self, **kwargs):
        self.colorLight()
        self.vpass()

    def mousePress(self, **kwargs):
        self.colorDark()
        self.vpass()

    def mouseRelease(self, **kwargs):
        self.colorNormal()
        self.vpass()

    def mouseLeave(self, **kwargs):
        self.colorNormal()
        self.vpass()


class TextActor(QObject, vmi.Menu, vmi.Mouse):
    def __init__(self, view: vmi.View, name=None):
        QObject.__init__(self)

        self.name = name if name else tr('文字 （Text)')
        vmi.Menu.__init__(self, name=self.name)

        vmi.Mouse.__init__(self)
        for b in self.mouse:
            for e in self.mouse[b]:
                if e == 'Enter':
                    self.mouse[b][e] = self.mouseEnter
                elif e == 'Leave':
                    self.mouse[b][e] = self.mouseLeave
                elif e == 'Press':
                    self.mouse[b][e] = self.mousePress
                elif e == 'PressMoveRelease':
                    self.mouse[b][e] = self.mouseRelease
                elif e == 'PressRelease':
                    self.mouse[b][e] = self.mouseRelease

        self.view = view
        self._Prop = vtk.vtkTextActor()
        self._Prop._Prop = self
        self.view._Renderer.AddActor(self._Prop)

        self._Prop.SetTextScaleModeToNone()

        self._Property: vtk.vtkTextProperty = self._Prop.GetTextProperty()
        self._Property.SetFontSize(0)
        self._Property.SetFontFamily(vtk.VTK_FONT_FILE)
        self._Property.SetLineSpacing(1.5)
        self._Property.SetShadow(1)

        self._Text = ''
        self.text()

        self._Aligns = {'left': vtk.VTK_TEXT_LEFT, 'right': vtk.VTK_TEXT_RIGHT,
                        'top': vtk.VTK_TEXT_TOP, 'bottom': vtk.VTK_TEXT_BOTTOM,
                        'center': vtk.VTK_TEXT_CENTERED, }

        self._Align = ['left', 'bottom']
        self.align()
        self._Pos = [0, 0]
        self.pos()
        self._Font = 'alizh'
        self.font()
        self._FontSize = 16
        self.size()

        self._RGB, self._Alpha = [0.8, 0.8, 0.8], 1.0
        self.color()
        self._Pickable = True
        self.pickable()

    def __setstate__(self, s):
        self.__init__(s['view'], s['name'])
        self.__dict__.update(s)
        s = self.__dict__

        del s['_Dumps']

        for kw in s['_VTKGets']:
            vmi.vtkset(getattr(self, kw), s['_VTKGets'][kw])
        del s['_VTKGets']

    def __getstate__(self):
        s = self.__dict__.copy()
        for kw in ['menu', 'actions', '__METAOBJECT__']:
            if kw in s:
                del s[kw]

        s['_Dumps'] = {}
        for kw in s['_Dumps']:
            del s[kw]

        s['_VTKGets'] = {name: vmi.vtkget(getattr(self, name)) for name in
                         ['_Prop', '_Property']}
        for kw in s['_VTKGets']:
            del s[kw]
        return s

    def text(self, text=None):
        if text is not None:
            self._Text = text
        self._Prop.SetInput(self._Text)
        self.view.updateInTime()

    def align(self, h=None, v=None):
        if h is not None:
            self._Align[0] = h
        if v is not None:
            self._Align[1] = v
        self._Property.SetJustification(self._Aligns[self._Align[0]])
        self._Property.SetVerticalJustification(self._Aligns[self._Align[1]])
        self.view.updateInTime()
        return self._Align

    def pos(self, x=None, y=None):
        if x is not None:
            self._Pos[0] = x
        if y is not None:
            self._Pos[1] = y
        self._Prop.SetPosition(self._Pos)
        self.view.updateInTime()
        return self._Pos

    def font(self, font=None):
        if font is not None and font in vmi.appFonts:
            self._Font = font
        self._Property.SetFontFile(vmi.appFonts[self._Font])
        self.view.updateInTime()
        return self._Font

    def color(self, rgb=None, alpha=None):
        self.view.updateInTime()
        if rgb is not None:
            self._RGB = rgb
        if alpha is not None:
            self._Alpha = alpha
        self._Property.SetColor(self._RGB)
        self._Property.SetOpacity(self._Alpha)
        return {'rgb': self._RGB, 'alpha': self._Alpha}

    def colorLight(self):
        c = QColor()
        c.setRgbF(self._RGB[0], self._RGB[1], self._RGB[2])
        c = c.lighter(120)
        self._Property.SetColor(c.redF(), c.greenF(), c.blueF())
        self.view.updateInTime()

    def colorDark(self):
        c = QColor()
        c.setRgbF(self._RGB[0], self._RGB[1], self._RGB[2])
        c = c.darker(120)
        self._Property.SetColor(c.redF(), c.greenF(), c.blueF())
        self.view.updateInTime()

    def colorNormal(self):
        self._Property.SetColor(self._RGB)
        self.view.updateInTime()

    def delete(self):
        self.view._Renderer.RemoveActor(self._Prop)

    def pickable(self, arg=None):
        if arg is True:
            self._Pickable = True
        elif arg is False:
            self._Pickable = False
        self._Prop.SetPickable(1 if self._Pickable else 0)
        self.view.updateInTime()
        return self._Pickable

    def size(self, **kwargs):
        if 'font' in kwargs:
            self._FontSize = kwargs['font']
        self._Property.SetFontSize(self._FontSize)
        self.view.updateInTime()
        return self._FontSize

    def mouseEnter(self, **kwargs):
        self.colorLight()
        self.vpass()

    def mousePress(self, **kwargs):
        self.colorDark()
        self.vpass()

    def mouseRelease(self, **kwargs):
        self.colorNormal()
        self.vpass()

    def mouseLeave(self, **kwargs):
        self.colorNormal()
        self.vpass()


class ImageSlice(QObject, vmi.Menu, vmi.Mouse):
    """场景表示，图像数据的断层表示
    vtk.vtkImageData -> vtk.vtkImageSlice"""

    def __init__(self, view: vmi.View, name=None):
        QObject.__init__(self)

        self.name = name if name else tr('图面 （Image slice)')
        vmi.Menu.__init__(self, name=self.name)

        self.actions = {'Visible': QAction(''),
                        'SlicePlaneValueNormal': QAction(''),
                        'SlicePlaneAxial': QAction(tr('横断位 (Axial)')),
                        'SlicePlaneSagittal': QAction(tr('矢状位 (Sagittal)')),
                        'SlicePlaneCoronal': QAction(tr('冠状位 (Coronal)')),
                        'WindowValue': QAction(''),
                        'WindowAuto': QAction(tr('自动 (Auto)')),
                        'WindowBone': QAction(tr('骨骼 (Bone)')),
                        'WindowSoft': QAction(tr('组织 (Soft)'))}

        self.actions['Visible'].triggered.connect(self.visibleToggle)
        self.actions['SlicePlaneAxial'].triggered.connect(self.setSlicePlaneAxial)
        self.actions['SlicePlaneSagittal'].triggered.connect(self.setSlicePlaneSagittal)
        self.actions['SlicePlaneCoronal'].triggered.connect(self.setSlicePlaneCoronal)
        self.actions['WindowAuto'].triggered.connect(self.setWindowAuto)
        self.actions['WindowBone'].triggered.connect(self.setWindowBone)
        self.actions['WindowSoft'].triggered.connect(self.setWindowSoft)

        def aboutToShow():
            self.actions['Visible'].setText(
                tr('可见 (Visible)') + ' = ' + (tr('显示 (Show)') if self.visible() else tr('隐藏 (Hide)')))
            self.actions['SlicePlaneValueNormal'].setText(
                tr('法向 (Normal)') + ' = ' + repr(self._BindSlicePlane._SlicePlane.GetNormal()))
            self.actions['WindowValue'].setText(
                tr('宽/位 (W/L)') + ' = ' + (repr(tuple(self._Window))))

            self.menu.clear()
            self.menu.addAction(self.actions['Visible'])

            menu = QMenu(tr('切面 (Slice plane)'))
            menu.addAction(self.actions['SlicePlaneValueNormal'])
            menu.addSeparator()
            menu.addAction(self.actions['SlicePlaneAxial'])
            menu.addAction(self.actions['SlicePlaneSagittal'])
            menu.addAction(self.actions['SlicePlaneCoronal'])
            self.menu.addMenu(menu)

            menu = QMenu(tr('窗 (Window)'))
            menu.addAction(self.actions['WindowValue'])
            menu.addSeparator()
            menu.addAction(self.actions['WindowAuto'])
            menu.addAction(self.actions['WindowBone'])
            menu.addAction(self.actions['WindowSoft'])
            self.menu.addMenu(menu)

        self.menu.aboutToShow.connect(aboutToShow)

        vmi.Mouse.__init__(self, menu=self)
        self.mouse['NoButton']['Wheel'] = self.slice
        self.mouse['LeftButton']['PressMove'] = self.window

        self.view = view
        self._Mapper = vtk.vtkImageResliceMapper()
        self._Prop = vtk.vtkImageSlice()
        self._Prop._Prop = self
        self.view._Renderer.AddViewProp(self._Prop)

        self._Property = self._Prop.GetProperty()
        self._Property.SetInterpolationTypeToCubic()
        self._Property.SetUseLookupTableScalarRange(1)

        self._Dataset = vtk.vtkImageData()
        self._BindDataset = self

        self._SlicePlane = vtk.vtkPlane()
        self._BindSlicePlane = self

        self._LookupTable = vtk.vtkLookupTable()
        self._BindLookupTable = self

        self._Window = [1000, 400]

        self.bindDataset()
        self.bindSlicePlane()
        self.bindLookupTable()
        self.setWindowSoft()

    def __setstate__(self, s):
        self.__init__(s['view'], s['name'])
        self.__dict__.update(s)
        s = self.__dict__

        self._Dataset.DeepCopy(vmi.loads(s['_Dumps']['_Dataset']))
        self._LookupTable.DeepCopy(vmi.loads(s['_Dumps']['_LookupTable']))
        del s['_Dumps']

        for kw in s['_VTKGets']:
            vmi.vtkset(getattr(self, kw), s['_VTKGets'][kw])
        del s['_VTKGets']

        self._Pickable = True
        self.pickable()

        self.bindDataset()
        self.bindSlicePlane()
        self.bindLookupTable()

    def __getstate__(self):
        s = self.__dict__.copy()
        for kw in ['menu', 'menuWindow', 'menuSlicePlane', 'actions', '__METAOBJECT__']:
            if kw in s:
                del s[kw]

        s['_Dumps'] = {'_Dataset': vmi.dumps(self._Dataset),
                       '_LookupTable': vmi.dumps(self._LookupTable)}
        for kw in s['_Dumps']:
            del s[kw]

        s['_VTKGets'] = {name: vmi.vtkget(getattr(self, name)) for name in
                         ['_Mapper', '_Prop', '_Property', '_SlicePlane']}
        for kw in s['_VTKGets']:
            del s[kw]

        return s

    def dataset(self):
        return self._BindDataset._Dataset

    def bindDataset(self, other=None):
        if hasattr(other, '_Dataset'):
            self._BindDataset = other
        self._Mapper.SetInputData(self.dataset())
        self._Prop.SetMapper(self._Mapper)
        self.view.updateInTime()

    def bindSlicePlane(self, other=None):
        if hasattr(other, '_SlicePlane'):
            self._BindSlicePlane = other
        self._Mapper.SetSlicePlane(self._BindSlicePlane._SlicePlane)
        self.view.updateInTime()

    def bindLookupTable(self, other=None):
        if hasattr(other, '_LookupTable'):
            self._BindLookupTable = other
        self._Property.SetLookupTable(self._BindLookupTable._LookupTable)
        self.view.updateInTime()

    def clone(self, other):
        if other is None:
            self.dataset().ShallowCopy(self.dataset().__class__())
        elif hasattr(other, '_Dataset'):
            self.dataset().ShallowCopy(other.dataset())
        elif isinstance(other, self.dataset().__class__):
            self.dataset().ShallowCopy(other)
        else:
            raise TypeError(type(other))

    def delete(self, *args):
        self._Dataset.ReleaseData()
        self.view._Renderer.RemoveViewProp(self._Prop)

    def pickable(self, arg=None):
        if arg is True:
            self._Pickable = True
        elif arg is False:
            self._Pickable = False
        self._Prop.SetPickable(1 if self._Pickable else 0)
        self.view.updateInTime()
        return self._Pickable

    def ori3(self):
        return list(self.dataset().GetOrigin())

    def bnd6(self):
        return list(self.dataset().GetBounds())

    def cnt3(self):
        return list(self.dataset().GetCenter())

    def dim3(self):
        return list(self.dataset().GetDimensions())

    def ext6(self, bnd6=None):
        if bnd6 is not None:
            ori, dth, ext = self.ori3(), self.dth3(), self.ext6()
            first, last = [bnd6[0], bnd6[2], bnd6[4]], [bnd6[1], bnd6[3], bnd6[5]]
            for i in range(3):
                f = int((first[i] - ori[i]) / dth[i])
                l = int((last[i] - ori[i]) / dth[i] + 1)
                if f > ext[2 * i]:
                    ext[2 * i] = f
                if l < ext[2 * i + 1]:
                    ext[2 * i + 1] = l
            return ext
        return list(self.dataset().GetExtent())

    def dth3(self):
        return list(self.dataset().GetSpacing())

    def dn(self, n3=None):
        if n3 is None:
            n3 = self._BindSlicePlane._SlicePlane.GetNormal()
        n3, dth3 = [abs(_) for _ in vmi.normalized3(n3)], self.dth3()
        return n3[0] * dth3[0] + n3[1] * dth3[1] + n3[2] * dth3[2]

    def lth3(self):
        bnd = self.bnd6()
        return [bnd[1] - bnd[0], bnd[3] - bnd[2], bnd[5] - bnd[4]]

    def lth(self, *args):
        lth, l = self.lth3(), 0
        for i in range(3):
            l += lth[i] ** 2 if i in args else 0
        return l ** 0.5

    def lthn(self, n3=None):
        if n3 is None:
            n3 = self._BindSlicePlane._SlicePlane.GetNormal()
        n3, lth3 = [abs(_) for _ in vmi.normalized3(n3)], self.lth3()
        return n3[0] * lth3[0] + n3[1] * lth3[1] + n3[2] * lth3[2]

    def stencil(self, polydata):
        stencil = vtk.vtkPolyDataToImageStencil()
        stencil.SetInputData(polydata)
        stencil.SetOutputOrigin(self.ori3())
        stencil.SetOutputSpacing(self.dth3())
        stencil.SetOutputWholeExtent(self.ext6())
        stencil.Update()
        return stencil.GetOutput()

    def it(self, ext=None, stencil=None):
        it = vtk.vtkImagePointIterator()
        it.Initialize(self.dataset(), ext, stencil)
        return it

    def value(self, ijk=None, value=None, m=0):
        if value is not None:
            self.dataset().SetScalarComponentFromDouble(ijk[0], ijk[1], ijk[2], m, value)
            self.dataset().Modified()
        return self.dataset().GetScalarComponentAsDouble(ijk[0], ijk[1], ijk[2], m)

    def visible(self, visible=None):
        if visible is not None:
            self._Prop.SetVisibility(1 if visible else 0)
            self.view.updateInTime()
        return True if self._Prop.GetVisibility() else False

    def visibleToggle(self, *args):
        self.visible(not self.visible())

    def setSlicePlane(self, origin=None, normal=None):
        if isinstance(origin, str):
            if origin.lower() == 'c':
                o = self.dataset().GetCenter()
                self._BindSlicePlane._SlicePlane.SetOrigin(o[0], o[1], o[2])
            elif origin.lower() in ('b0', 'b1', 'b2', 'b3', 'b4', 'b5'):
                i = int(origin[-1])
                o = list(self.dataset().GetCenter())
                o[int(i / 2)] = self.dataset().GetBounds()[i]
                self._BindSlicePlane._SlicePlane.SetOrigin(o[0], o[1], o[2])
        elif origin is not None:
            self._BindSlicePlane._SlicePlane.SetOrigin(origin[0], origin[1], origin[2])
        if isinstance(normal, str):
            if normal.lower() == 'sagittal':
                self._BindSlicePlane._SlicePlane.SetNormal(1, 0, 0)
            elif normal.lower() == 'coronal':
                self._BindSlicePlane._SlicePlane.SetNormal(0, 1, 0)
            elif normal.lower() == 'axial':
                self._BindSlicePlane._SlicePlane.SetNormal(0, 0, 1)
        elif normal is not None:
            self._BindSlicePlane._SlicePlane.SetNormal(normal[0], normal[1], normal[2])
        self.view.updateInTime()

    def setSlicePlaneAxial(self):
        self.setSlicePlane(normal='axial')

    def setSlicePlaneSagittal(self):
        self.setSlicePlane(normal='sagittal')

    def setSlicePlaneCoronal(self):
        self.setSlicePlane(normal='coronal')

    def setWindow(self, preset=None, width=None, level=None):
        if preset is None:
            if width is not None:
                self._Window[0] = width
            if level is not None:
                self._Window[1] = level

            self._Window[0] = int(self._Window[0])
            self._Window[1] = int(self._Window[1])

            r = [self._Window[1] - 0.5 * self._Window[0],
                 self._Window[1] + 0.5 * self._Window[0]]

            t = self._BindLookupTable._LookupTable
            t.SetNumberOfTableValues(self._Window[0])
            t.SetTableRange(r)
            t.SetBelowRangeColor(0, 0, 0, 1.0)
            t.SetAboveRangeColor(1, 1, 1, 1.0)
            t.SetUseBelowRangeColor(1)
            t.SetUseAboveRangeColor(1)

            for i in range(self._Window[0]):
                v = i / self._Window[0]
                t.SetTableValue(i, (v, v, v, 1.0))
            self.view.updateInTime()

        elif preset.lower() == 'auto':
            r = vtk.vtkImageHistogramStatistics()
            r.SetInputData(self.dataset())
            r.SetAutoRangePercentiles(1, 99)
            r.SetGenerateHistogramImage(0)
            r.Update()
            r = r.GetAutoRange()

            self.setWindow(width=r[1] - r[0], level=0.5 * (r[0] + r[1]))
        elif preset.lower() == 'bone':
            self.setWindow(width=1000, level=400)
        elif preset.lower() == 'soft':
            self.setWindow(width=350, level=50)

    def setWindowAuto(self, **kwargs):
        self.setWindow('auto')

    def setWindowBone(self, **kwargs):
        self.setWindow('bone')

    def setWindowSoft(self, **kwargs):
        self.setWindow('soft')

    def slice(self, **kwargs):
        o = list(self._BindSlicePlane._SlicePlane.GetOrigin())
        n = self._BindSlicePlane._SlicePlane.GetNormal()
        dim = self.dataset().GetDimensions()
        dxyz = self.dataset().GetSpacing()

        n = [abs(_) / (n[0] ** 2 + n[1] ** 2 + n[2] ** 2) ** 0.5 for _ in n]
        dn = n[0] * dxyz[0] + n[1] * dxyz[1] + n[2] * dxyz[2]

        for i in range(3):
            if dim[i] > 1:
                o[i] += kwargs['delta'] * dn * n[i]

        if vtk.vtkMath.PlaneIntersectsAABB(self.dataset().GetBounds(), n, o) == 0:
            self.setSlicePlane(origin=o)

    def window(self, **kwargs):
        dx, dy = self.view.mouseOverDisplay()

        r = self.dataset().GetScalarRange()
        t = (r[1] - r[0]) / 2048
        self._Window[0] += t * dx
        self._Window[1] -= t * dy

        self._Window[0] = max(self._Window[0], 0)
        self._Window[0] = min(self._Window[0], r[1] - r[0])
        self._Window[1] = max(self._Window[1], r[0])
        self._Window[1] = min(self._Window[1], r[1])
        self.setWindow()


class ImageVolume(QObject, vmi.Menu, vmi.Mouse):
    """场景表示，图像数据的立体表示
    vtk.vtkImageData -> vtk.vtkVolume"""

    def __init__(self, view: vmi.View, name=None):
        QObject.__init__(self)

        self.name = name if name else tr('图体 （Image volume)')
        vmi.Menu.__init__(self, name=self.name)

        self.actions = {'Visible': QAction(''),
                        'Threshold': QAction(tr('阈值 (Threshold)'))}

        self.actions['Visible'].triggered.connect(self.visibleToggle)
        self.actions['Threshold'].triggered.connect(self.threshold)

        def aboutToShow():
            self.actions['Visible'].setText(
                tr('可见 (Visible)') + ' = ' + (tr('显示 (Show)') if self.visible() else tr('隐藏 (Hide)')))

            self.menu.clear()
            self.menu.addAction(self.actions['Visible'])

            menu = QMenu(tr('风格 (Style)'))
            menu.addAction(self.actions['Threshold'])
            self.menu.addMenu(menu)

        self.menu.aboutToShow.connect(aboutToShow)

        vmi.Mouse.__init__(self)

        self.view = view
        self._Mapper = vtk.vtkGPUVolumeRayCastMapper()
        self._Prop = vtk.vtkVolume()
        self._Prop._Prop = self
        self.view._Renderer.AddVolume(self._Prop)

        self._Mapper.SetBlendModeToComposite()
        self._Mapper.SetMaxMemoryInBytes(4096)
        self._Mapper.SetMaxMemoryFraction(1)
        self._Mapper.SetAutoAdjustSampleDistances(0)
        self._Mapper.SetLockSampleDistanceToInputSpacing(1)
        self._Mapper.SetUseJittering(1)

        self._Property = self._Prop.GetProperty()
        self._Property.SetInterpolationTypeToLinear()
        self._Property.SetAmbient(0.1)
        self._Property.SetDiffuse(0.9)
        self._Property.SetShade(1)

        self._Dataset = vtk.vtkImageData()
        self._BindDataset = self

        self._Color = {0: (1, 1, 1)}
        self._ScalarOpacity = {0: 0, 400: 1}
        self._GradientOpacity = {}

        self._Pickable = True
        self.pickable()

        self.bindDataset()
        self.setColor()
        self.setScalarOpacity()
        self.setGradientOpacity()

    def __setstate__(self, s):
        self.__init__(s['view'], s['name'])
        self.__dict__.update(s)
        s = self.__dict__

        self._Dataset.DeepCopy(vmi.loads(s['_Dumps']['_Dataset']))
        del s['_Dumps']

        for kw in s['_VTKGets']:
            vmi.vtkset(getattr(self, kw), s['_VTKGets'][kw])
        del s['_VTKGets']

        self.bindDataset()
        self.setColor()
        self.setScalarOpacity()
        self.setGradientOpacity()

    def __getstate__(self):
        s = self.__dict__.copy()
        for kw in ['menu', 'actions', '__METAOBJECT__']:
            if kw in s:
                del s[kw]

        s['_Dumps'] = {'_Dataset': vmi.dumps(self._Dataset),
                       '_Color': self._Color}
        for kw in s['_Dumps']:
            del s[kw]

        s['_VTKGets'] = {name: vmi.vtkget(getattr(self, name)) for name in
                         ['_Mapper', '_Prop', '_Property']}
        for kw in s['_VTKGets']:
            del s[kw]

        return s

    def dataset(self):
        return self._BindDataset._Dataset

    def bindDataset(self, other=None):
        if hasattr(other, '_Dataset'):
            self._BindDataset = other
        self._Mapper.SetInputData(self.dataset())
        self._Prop.SetMapper(self._Mapper)
        self.view.updateInTime()

    def clone(self, other):
        if other is None:
            self.dataset().ShallowCopy(self.dataset().__class__())
        elif hasattr(other, 'dataset'):
            self.dataset().ShallowCopy(other.dataset())
        elif isinstance(other, self.dataset().__class__):
            self.dataset().ShallowCopy(other)
        else:
            raise TypeError(type(other))

    def delete(self):
        # self._Dataset.ReleaseData()
        image = vtk.vtkImageData()
        image.SetExtent(0, 1, 0, 0, 0, 0)
        image.AllocateScalars(vtk.VTK_SHORT, 1)
        self.clone(image)
        self.view._Renderer.RemoveVolume(self._Prop)

    def pickable(self, arg=None):
        if arg is True:
            self._Pickable = True
        elif arg is False:
            self._Pickable = False
        self._Prop.SetPickable(1 if self._Pickable else 0)
        self.view.updateInTime()
        return self._Pickable

    def ori3(self):
        return list(self.dataset().GetOrigin())

    def bnd6(self):
        return list(self.dataset().GetBounds())

    def cnt3(self):
        return list(self.dataset().GetCenter())

    def dim3(self):
        return list(self.dataset().GetDimensions())

    def ext6(self, bnd6=None):
        if bnd6 is not None:
            ori, dth, ext = self.ori3(), self.dth3(), self.ext6()
            first, last = [bnd6[0], bnd6[2], bnd6[4]], [bnd6[1], bnd6[3], bnd6[5]]
            for i in range(3):
                f = int((first[i] - ori[i]) / dth[i])
                l = int((last[i] - ori[i]) / dth[i] + 1)
                if f > ext[2 * i]:
                    ext[2 * i] = f
                if l < ext[2 * i + 1]:
                    ext[2 * i + 1] = l
            return ext
        return list(self.dataset().GetExtent())

    def dth3(self):
        return list(self.dataset().GetSpacing())

    def dn(self, n3=None):
        if n3 is None:
            n3 = self._BindSlicePlane._SlicePlane.GetNormal()
        n3, dth3 = [abs(_) for _ in vmi.normalized3(n3)], self.dth3()
        return n3[0] * dth3[0] + n3[1] * dth3[1] + n3[2] * dth3[2]

    def lth3(self):
        bnd = self.bnd6()
        return [bnd[1] - bnd[0], bnd[3] - bnd[2], bnd[5] - bnd[4]]

    def lth(self, *args):
        lth, l = self.lth3(), 0
        for i in range(3):
            l += lth[i] ** 2 if i in args else 0
        return l ** 0.5

    def lthn(self, n3=None):
        if n3 is None:
            n3 = self._BindSlicePlane._SlicePlane.GetNormal()
        n3, lth3 = [abs(_) for _ in vmi.normalized3(n3)], self.lth3()
        return n3[0] * lth3[0] + n3[1] * lth3[1] + n3[2] * lth3[2]

    def stencil(self, polydata):
        stencil = vtk.vtkPolyDataToImageStencil()
        stencil.SetInputData(polydata)
        stencil.SetOutputOrigin(self.ori3())
        stencil.SetOutputSpacing(self.dth3())
        stencil.SetOutputWholeExtent(self.ext6())
        stencil.Update()
        return stencil.GetOutput()

    def it(self, ext=None, stencil=None):
        it = vtk.vtkImagePointIterator()
        it.Initialize(self.dataset(), ext, stencil)
        return it

    def value(self, ijk=None, value=None, m=0):
        if value is not None:
            self.dataset().SetScalarComponentFromDouble(ijk[0], ijk[1], ijk[2], m, value)
            self.dataset().Modified()
        return self.dataset().GetScalarComponentAsDouble(ijk[0], ijk[1], ijk[2], m)

    def visible(self, visible=None):
        if visible is not None:
            self._Prop.SetVisibility(1 if visible else 0)
            self.view.updateInTime()
        return True if self._Prop.GetVisibility() else False

    def visibleToggle(self, *args):
        self.visible(not self.visible())

    def setColor(self, scalar_rgb=None):
        if scalar_rgb is not None:
            self._Color = scalar_rgb
            self.setColor()
        else:
            f = vtk.vtkColorTransferFunction()
            for x in self._Color:
                r, g, b = self._Color[x]
                f.AddRGBPoint(x, r, g, b)
            self._Property.SetColor(f)

    def setScalarOpacity(self, scalar_opacity=None):
        if scalar_opacity is not None:
            self._ScalarOpacity = scalar_opacity
            self.setScalarOpacity()
        else:
            f = vtk.vtkPiecewiseFunction()
            for x in self._ScalarOpacity:
                f.AddPoint(x, self._ScalarOpacity[x])
            self._Property.SetScalarOpacity(f)

    def setGradientOpacity(self, gradient_opacity=None):
        if gradient_opacity is None:
            f = vtk.vtkPiecewiseFunction()
            for x in self._GradientOpacity:
                f.AddPoint(x, self._GradientOpacity[x])
            self._Property.SetGradientOpacity(f)
        else:
            self._Color = gradient_opacity
            self.setGradientOpacity()

    def threshold(self, *args, value=None):
        if value is None:
            value = vmi.askInt(vtk.VTK_SHORT_MIN, 0, vtk.VTK_SHORT_MAX, tr('阈值 (Threshold value)'))
        if value is not None:
            self.setScalarOpacity({value - 1: 0, value: 1})
