import sys
import numpy.linalg as npl

import vtk
from PySide2.QtWidgets import *

import convert
from widget import Mouse, Widget


class Prop(Mouse):
    """场景物体
    self.prop is a vtk.vtkProp"""

    def __init__(self, vi: Widget):
        Mouse.__init__(self)

        self._Vi = vi
        self.setMouseStyle('Vi')
        self._Prop: vtk.vtkProp = None

    def setMouseStyle(self, style):
        if style == 'None':
            for b in self.mouse:
                for e in self.mouse[b]:
                    self.mouse[b][e] = self.none
        elif style == 'Vi':
            for b in self.mouse:
                for e in self.mouse[b]:
                    self.mouse[b][e] = self._Vi.mouse[b][e]

    def pickable(self, arg=None):
        if arg is None:
            return self._Prop.GetPickable()
        else:
            self._Prop.SetPickable(arg)
            self._Vi.updateInTime()

    def visible(self, arg=None):
        if arg is None:
            return self._Prop.GetVisibility()
        else:
            self._Prop.SetVisibility(arg)
            self._Vi.updateInTime()


class Dataset:
    """场景物体的数据表达
    self.data is vtk.vtkDataSet"""

    def __init__(self):
        self._Dataset = None

    def clone(self, other=None):
        if other is not None:
            self._Dataset.ShallowCopy(self._Dataset.__class__())
        if hasattr(other, '_Dataset'):
            self._Dataset.ShallowCopy(other._Dataset)
        if isinstance(other, self._Dataset.__class__):
            self._Dataset.ShallowCopy(other)
        else:
            raise TypeError(type(other))


class ImageSlice(Prop, Dataset):
    """场景表示，图像数据的断层表示
    vtk.vtkImageData -> vtk.vtkImageSlice"""

    def __init__(self, vi: Widget):
        Prop.__init__(self, vi)
        Dataset.__init__(self)

        self._Mapper = vtk.vtkImageResliceMapper()
        self._Prop = vtk.vtkImageSlice()
        self._Prop._Prop = self
        self._Vi._Renderer.AddViewProp(self._Prop)

        self._Property = self._Prop.GetProperty()
        self._Property.SetInterpolationTypeToCubic()
        self._Property.SetUseLookupTableScalarRange(1)

        self._Dataset = vtk.vtkImageData()
        self._BindDataset = self

        self._SlicePlane = vtk.vtkPlane()
        self._BindSlicePlane = self

        self._LookupTable = vtk.vtkLookupTable()
        self._BindLookupTable = self

        self._WindowWidth = self._WindowLevel = 400

        self.bindDataset()
        self.bindSlicePlane()
        self.bindLookupTable()

        self.mouse[b'NoButton']['Wheel'] = self.slice
        self.mouse[b'LeftButton']['PressMove'] = self.window

    def delete(self):
        self._Dataset.ReleaseData()
        self._Vi._Renderer.RemoveViewProp(self._Prop)
        self._Dataset = self._Mapper = self._Prop = self._Property = self._Vi = None
        self._BindDataset = self._BindSlicePlane = self._BindLookupTable

    def __setstate__(self, s):
        self.__init__(s['_Vi'])
        self.__dict__.update(s)
        s = self.__dict__

        self._Dataset.DeepCopy(convert.loads(s['_Dumps']['_Dataset']))
        self._LookupTable.DeepCopy(convert.loads(s['_Dumps']['_LookupTable']))
        del s['_Dumps']

        for kw in s['_VTKGets']:
            convert.vtkset(getattr(self, kw), s['_VTKGets'][kw])
        del s['_VTKGets']

        self.bindDataset()
        self.bindSlicePlane()
        self.bindLookupTable()

    def __getstate__(self):
        s = self.__dict__.copy()

        s['_Dumps'] = {'_Dataset': convert.dumps(self._Dataset),
                       '_LookupTable': convert.dumps(self._LookupTable)}
        for kw in s['_Dumps']:
            del s[kw]

        s['_VTKGets'] = {name: convert.vtkget(getattr(self, name)) for name in
                         ['_Mapper', '_Prop', '_Property', '_SlicePlane']}
        for kw in s['_VTKGets']:
            del s[kw]

        return s

    def bindDataset(self, other=None):
        if hasattr(other, '_Dataset'):
            self._BindDataset = other
        self._Mapper.SetInputData(self._BindDataset._Dataset)
        self._Prop.SetMapper(self._Mapper)
        self._Vi.updateInTime()

    def bindSlicePlane(self, other=None):
        if hasattr(other, '_SlicePlane'):
            self._BindSlicePlane = other
        self._Mapper.SetSlicePlane(self._BindSlicePlane._SlicePlane)
        self._Vi.updateInTime()

    def bindLookupTable(self, other=None):
        if hasattr(other, '_LookupTable'):
            self._BindLookupTable = other
        self._Property.SetLookupTable(self._BindLookupTable._LookupTable)
        self._Vi.updateInTime()

    def setSlicePlane(self, origin=None, normal=None):
        if isinstance(origin, str):
            if origin.lower() == 'c':
                o = self._BindDataset._Dataset.GetCenter()
                self._BindSlicePlane._SlicePlane.SetOrigin(o[0], o[1], o[2])
            elif origin.lower() in ('b0', 'b1', 'b2', 'b3', 'b4', 'b5'):
                i = int(origin[-1])
                o = list(self._BindDataset._Dataset.GetCenter())
                o[int(i / 2)] = self._BindDataset._Dataset.GetBounds()[i]
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
        self._Vi.updateInTime()

    def setWindow(self, preset=None, width=None, level=None):
        if preset is None:
            if width is not None:
                self._WindowWidth = width
            if level is not None:
                self._WindowLevel = level

            self._WindowWidth = int(self._WindowWidth)
            self._WindowLevel = int(self._WindowLevel)

            r = [self._WindowLevel - 0.5 * self._WindowWidth,
                 self._WindowLevel + 0.5 * self._WindowWidth]

            t = self._BindLookupTable._LookupTable
            t.SetNumberOfTableValues(self._WindowWidth)
            t.SetTableRange(r)
            t.SetBelowRangeColor(0, 0, 0, 1.0)
            t.SetAboveRangeColor(1, 1, 1, 1.0)
            t.SetUseBelowRangeColor(1)
            t.SetUseAboveRangeColor(1)

            for i in range(self._WindowWidth):
                v = i / self._WindowWidth
                t.SetTableValue(i, (v, v, v, 1.0))
            self._Vi.updateInTime()

        elif preset.lower() == 'auto':
            r = vtk.vtkImageHistogramStatistics()
            r.SetInputData(self._BindDataset._Dataset)
            r.SetAutoRangePercentiles(1, 99)
            r.SetGenerateHistogramImage(0)
            r.Update()
            r = r.GetAutoRange()
            self.setWindow(r[1] - r[0], 0.5 * (r[0] + r[1]))
        elif preset.lower() == 'bone':
            self.setWindow(width=1000, level=400)
        elif preset.lower() == 'soft':
            self.setWindow(width=350, level=50)

    def slice(self, **kwargs):
        o = list(self._BindSlicePlane._SlicePlane.GetOrigin())
        n = self._BindSlicePlane._SlicePlane.GetNormal()
        dim = self._BindDataset._Dataset.GetDimensions()
        dxyz = self._BindDataset._Dataset.GetSpacing()

        n = [_ / npl.norm(n) for _ in n]
        dn = n[0] * dxyz[0] + n[1] * dxyz[1] + n[2] * dxyz[2]

        for i in range(3):
            if dim[i] > 1:
                o[i] += kwargs['delta'] * dn * n[i]

        if vtk.vtkMath.PlaneIntersectsAABB(self._Dataset.GetBounds(), n, o) == 0:
            self.setSlicePlane(origin=o)

    def window(self, **kwargs):
        dx, dy = self._Vi.mouseOverDisplay()

        r = self._Dataset.GetScalarRange()
        t = (r[1] - r[0]) / 2048
        self._WindowWidth += t * dx
        self._WindowLevel -= t * dy

        self._WindowWidth = max(self._WindowWidth, 0)
        self._WindowWidth = min(self._WindowWidth, r[1] - r[0])
        self._WindowLevel = max(self._WindowLevel, r[0])
        self._WindowLevel = min(self._WindowLevel, r[1])
        self.setWindow()


class ImageVolume(Prop, Dataset):
    """场景表示，图像数据的立体表示
    vtk.vtkImageData -> vtk.vtkVolume"""

    def __init__(self, vi: Widget):
        Prop.__init__(self, vi)
        Dataset.__init__(self)

        self._Mapper = vtk.vtkGPUVolumeRayCastMapper()
        self._Prop = vtk.vtkVolume()
        self._Prop._Prop = self
        self._Vi._Renderer.AddVolume(self._Prop)

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

        self.bindDataset()
        self.setColor()
        self.setScalarOpacity()
        self.setGradientOpacity()

    def delete(self):
        self._Dataset.ReleaseData()
        self._Vi._Renderer.RemoveVolume(self._Prop)

    def __setstate__(self, s):
        self.__init__(s['_Vi'])
        self.__dict__.update(s)
        s = self.__dict__

        self._Dataset.DeepCopy(convert.loads(s['_Dumps']['_Dataset']))
        del s['_Dumps']

        for kw in s['_VTKGets']:
            convert.vtkset(getattr(self, kw), s['_VTKGets'][kw])
        del s['_VTKGets']

        self.bindDataset()
        self.setColor()
        self.setScalarOpacity()
        self.setGradientOpacity()

    def __getstate__(self):
        s = self.__dict__.copy()

        s['_Dumps'] = {'_Dataset': convert.dumps(self._Dataset),
                       '_Color': self._Color}
        for kw in s['_Dumps']:
            del s[kw]

        s['_VTKGets'] = {name: convert.vtkget(getattr(self, name)) for name in
                         ['_Mapper', '_Prop', '_Property']}
        for kw in s['_VTKGets']:
            del s[kw]

        return s

    def bindDataset(self, other=None):
        if hasattr(other, '_Dataset'):
            self._BindDataset = other
        self._Mapper.SetInputData(self._BindDataset._Dataset)
        self._Prop.SetMapper(self._Mapper)
        self._Vi.updateInTime()

    def setColor(self, scalar_rgb=None):
        if scalar_rgb is None:
            f = vtk.vtkColorTransferFunction()
            for x in self._Color:
                r, g, b = self._Color[x]
                f.AddRGBPoint(x, r, g, b)
            self._Property.SetColor(f)
        else:
            self._Color = scalar_rgb
            self.setColor()

    def setScalarOpacity(self, scalar_opacity=None):
        if scalar_opacity is None:
            f = vtk.vtkPiecewiseFunction()
            for x in self._ScalarOpacity:
                f.AddPoint(x, self._ScalarOpacity[x])
            self._Property.SetScalarOpacity(f)
        else:
            self._Color = scalar_opacity
            self.setScalarOpacity()

    def setGradientOpacity(self, gradient_opacity=None):
        if gradient_opacity is None:
            f = vtk.vtkPiecewiseFunction()
            for x in self._GradientOpacity:
                f.AddPoint(x, self._GradientOpacity[x])
            self._Property.SetGradientOpacity(f)
        else:
            self._Color = gradient_opacity
            self.setGradientOpacity()


class PolyActor(Prop, Dataset):
    """场景表示，聚合数据的表示
    vtk.vtkPolyData -> vtk.vtkActor"""

    def __init__(self, vi: Widget):
        Prop.__init__(self, vi)
        Dataset.__init__(self)

        self._Mapper = vtk.vtkPolyDataMapper()
        self._Prop = vtk.vtkActor()
        self._Prop._Prop = self
        self._Vi._Renderer.AddActor(self._Prop)

        self._Prop.SetPickable(1)  # 默认可拾取

        self._Property = self._Prop.GetProperty()
        self._Property.SetAmbient(0.1)
        self._Property.SetDiffuse(0.9)

        self._BackfaceProperty = self.propertyBackface()
        self._Prop.SetBackfaceProperty(self._Property)

        self._Dataset = vtk.vtkPolyData()
        self._BindDataset = self
        self.bindDataset()

    def __del__(self):
        self._Vi._Renderer.RemoveActor(self._Prop)

    def bindDataset(self, other=None):
        if hasattr(other, '_Dataset'):
            self._BindDataset = other
        self._Mapper.SetInputData(self._BindDataset._Dataset)
        self._Prop.SetMapper(self._Mapper)
        self._Vi.updateInTime()

    def propertyBackface(self):
        return self._Prop.GetBackfaceProperty()

    def __setstate__(self, s):
        self.__init__(s['_Vi'])
        self.__dict__.update(s)
        s = self.__dict__

        self._Dataset.DeepCopy(convert.loads(s['_Dumps']['_Dataset']))
        del s['_Dumps']

        for kw in s['_VTKGets']:
            convert.vtkset(getattr(self, kw), s['_VTKGets'][kw])
        del s['_VTKGets']

        self.bindDataset()

    def __getstate__(self):
        s = self.__dict__.copy()

        s['_Dumps'] = {'_Dataset': convert.dumps(self._Dataset)}
        for kw in s['_Dumps']:
            del s[kw]

        s['_VTKGets'] = {name: convert.vtkget(getattr(self, name)) for name in
                         ['_Mapper', '_Prop', '_Property', '_BackfaceProperty']}
        for kw in s['_VTKGets']:
            del s[kw]

        return s


class ViTextActor(Prop):
    """场景表示，聚合数据的表示
        vtk.vtkPolyData -> vtk.vtkActor"""

    def __init__(self, vi: Widget):
        Prop.__init__(self, vi)
        self.prop = vtk.vtkTextActor()


if __name__ == '__main__':
    from pprint import pprint

    app = QApplication(sys.argv)
    app.setOrganizationName('Vi')
    app.setApplicationName('Vi')

    w = Widget()
    w.setMouseStyle("Volume")
    w.show()

    cone = vtk.vtkConeSource()
    cone.SetResolution(8)
    cone.Update()

    reader = vtk.vtkSTLReader()
    reader.SetFileName('C:/Users/Medraw/Desktop/0921.stl')
    reader.Update()

    pa = PolyActor(w)
    pa.clone(reader.GetOutput())
    w._Renderer.ResetCamera()

    pa1 = PolyActor(w)
    pa1._Property.SetColor(1, 0.5, 0.5)
    pa1.bindDataset(pa)
    pa.visible(0)


    def f(**kwargs):
        pprint(kwargs)


    for b in pa.mouse:
        for e in pa.mouse[b]:
            if 'Move' not in e:
                pa.mouse[b][e] = f

    app.exec_()

    import shelve
    from pickle import HIGHEST_PROTOCOL

    with shelve.open('db', 'n', HIGHEST_PROTOCOL) as db:
        db['w'] = {'Vi': w, 'pa': pa, 'pa1': pa1}

    with shelve.open('db', 'r') as db:
        db = db['w']
        db['Vi'].show()
        sys.exit(app.exec_())
