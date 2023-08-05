import sys
from typing import Dict, Any, List
import threading
import time

import vtk
import numpy.linalg as npl
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtOpenGL import QGLWidget
from PySide2.QtWidgets import *
from PySide2.QtWinExtras import *

import vmi


class Mouse:
    def __init__(self, menu=None):
        i = 0

        def e():
            nonlocal i
            name = '_MouseEvent{}'.format(i)
            if not hasattr(self, name):
                setattr(self, '_MouseEvent{}'.format(i), self.vpass)
                i += 1
            return getattr(self, name)

        self.mouse = {
            'NoButton': {'Enter': e(), 'Leave': e(), 'Wheel': e(), 'Move': e()},
            'LeftButton': {'Press': e(), 'PressMove': e(), 'PressMoveRelease': e(), 'PressRelease': e()},
            'MidButton': {'Press': e(), 'PressMove': e(), 'PressMoveRelease': e(), 'PressRelease': e()},
            'RightButton': {'Press': e(), 'PressMove': e(), 'PressMoveRelease': e(), 'PressRelease': e()}}

        if menu:
            self.mouse['RightButton']['PressRelease'] = menu.vexec

    @staticmethod
    def vpass(**kwargs):
        return 'pass'

    @staticmethod
    def vblock(**kwargs):
        return


class Menu:
    def __init__(self, name=None):
        self.menu = QMenu()

        if name is not None:
            self.menu.setTitle(name)

    def vexec(self, **kwargs):
        self.menu.exec_(QCursor.pos())


class View(QGLWidget, Menu, Mouse):
    """vtk场景"""

    def __init__(self, name=None, parent=None):
        QGLWidget.__init__(self, parent)

        self.name = name if name else self.tr('视图 (View)')
        Menu.__init__(self, name=self.name)

        self.actions = {'CameraFit': QAction(self.tr('最适 (Fit)')),
                        'CameraReverse': QAction(self.tr('反向 (Reverse)')),
                        'CameraAxial': QAction(self.tr('横断位 (Axial)')),
                        'CameraSagittal': QAction(self.tr('矢状位 (Sagittal)')),
                        'CameraCoronal': QAction(self.tr('冠状位 (Coronal)')),
                        'Snapshot': QAction(self.tr('快照 (Snapshot)')), }

        self.actions['CameraFit'].triggered.connect(self.setCameraFit)
        self.actions['CameraReverse'].triggered.connect(self.setCameraReverse)
        self.actions['CameraAxial'].triggered.connect(self.setCameraAxial)
        self.actions['CameraSagittal'].triggered.connect(self.setCameraSagittal)
        self.actions['CameraCoronal'].triggered.connect(self.setCameraCoronal)
        self.actions['Snapshot'].triggered.connect(self.snapshot)

        def aboutToShow():
            self.menu.clear()
            self.menu.addAction(self.actions['CameraFit'])
            self.menu.addAction(self.actions['CameraReverse'])
            self.menu.addAction(self.actions['CameraAxial'])
            self.menu.addAction(self.actions['CameraSagittal'])
            self.menu.addAction(self.actions['CameraCoronal'])
            self.menu.addAction(self.actions['Snapshot'])

        self.menu.aboutToShow.connect(aboutToShow)

        Mouse.__init__(self, menu=self)
        self.mouse['LeftButton']['PressMove'] = self.mouseRotateFocal
        self.mouse['MidButton']['PressMove'] = self.mousePan
        self.mouse['RightButton']['PressMove'] = self.mouseZoom
        self._MStack: List[Mouse] = []

        rect = QGuiApplication.screens()[0].geometry()
        rect = QRect(rect.center() - QPoint(800, 450), QSize(1600, 900))
        self.setGeometry(rect)
        self.setAttribute(Qt.WA_OpaquePaintEvent)
        self.setAttribute(Qt.WA_PaintOnScreen)
        self.setFocusPolicy(Qt.WheelFocus)
        self.setMouseTracking(True)

        # 渲染器
        self._Renderer = vtk.vtkRenderer()
        self._Renderer.SetUseHiddenLineRemoval(1)  # 隐线消除
        self._Renderer.SetUseFXAA(False)  # 快速近似抗锯齿
        self._Renderer.SetBackground(1, 1, 1)

        # 渲染窗口
        self._RenderWindow = vtk.vtkRenderWindow()
        self._RenderWindow.SetWindowInfo(str(int(self.winId())))
        self._RenderWindow.AddRenderer(self._Renderer)

        # 交互器
        self._Interactor = vtk.vtkGenericRenderWindowInteractor()
        self._Interactor.SetRenderWindow(self._RenderWindow)
        self._Interactor.Initialize()

        # 方位标
        self._OrientationMarker = init_orientation_marker(self._Interactor)

        # 照相机
        self._Camera = self.camera()
        self.camera().SetParallelProjection(True)  # 平行投影

        # 拾取器
        self._Picker = vtk.vtkPicker()
        self._PickerProp = vtk.vtkPropPicker()
        self._PickerPoint = vtk.vtkPointPicker()
        self._PickerCell = vtk.vtkCellPicker()
        self._Picker.SetTolerance(0.005)
        self._PickerPoint.SetTolerance(0.005)
        self._PickerCell.SetTolerance(0.005)

        # 刷新计时器
        self._Timer = QTimer(self)
        self._Timer.timeout.connect(self.timeout)
        self._Timer.start(10)

        self._Time = QTime()
        self._Time.start()
        self._FPS = self._UpdateSum = 0

        # 创建一个隐藏控件，当销毁时调用清理vtk元素
        self._Hidden = QWidget(self)
        self._Hidden.hide()
        self._Hidden.destroyed.connect(self.delete)

        # 更新请求
        self._UpdateAtOnce: bool = False

        # 鼠标位置
        self._DblClick = False
        self._MousePosLast: QPoint = QPoint(0, 0)
        self._MousePos: QPoint = QPoint(0, 0)

        # 鼠标正在交互的对象
        self.activated = None
        self._PProp: vtk.vtkProp = None
        self._PView: View = None

        # 鼠标按键状态
        self._ButtonPress = self._ButtonPressMove = 'NoButton'

    def __setstate__(self, s):
        self.__init__(s['name'])
        self.__dict__.update(s)

        for kw in s['_VTKGets']:
            vmi.vtkset(getattr(self, kw), s['_VTKGets'][kw])

    def __getstate__(self):
        s = self.__dict__.copy()
        for kw in ['menu', 'menuCamera', 'actions', '_OrientationMarker', '_Timer', '_Hidden', '__METAOBJECT__']:
            if kw in s:
                del s[kw]

        s['_VTKGets'] = {name: vmi.vtkget(getattr(self, name)) for name in
                         ['_RenderWindow', '_Renderer', '_Interactor', '_Camera',
                          '_Picker', '_PickerProp', '_PickerPoint', '_PickerCell']}

        for kw in s['_VTKGets']:
            del s[kw]
        return s

    def camera(self, *args):
        if len(args) == 0:
            return self._Renderer.GetActiveCamera()
        elif len(args) > 0:
            fp = list(self.camera().GetFocalPoint())
            cp = list(self.camera().GetPosition())
            up = list(self.camera().GetViewUp())

            look, right = [fp[i] - cp[i] for i in range(3)], [0] * 3

            vtk.vtkMath.Cross(look, up, right)
            vtk.vtkMath.Normalize(look)
            vtk.vtkMath.Normalize(right)
            vtk.vtkMath.Normalize(up)

            t, value = [], {'focal': fp, 'position': cp, 'up': up, 'look': look, 'right': right}
            for key in args:
                if key in value.keys():
                    t.append(value[key])
            if len(t) == 1:
                t = t[0]
            return t

    def closeEvent(self, ev):
        self.delete()

    def delete(self):
        self._Timer.stop()
        self._RenderWindow.Finalize()

    def mousexec(self, stack, button, event, picked=None, **kwargs):
        if picked is None:
            if self._PView:
                picked = self._PView
            if self._PProp:
                picked = self._PProp

        for m in [m for m in stack if isinstance(m, Mouse)]:
            if m.mouse[button][event](picked=picked, **kwargs) != 'pass':
                break

    def addMouse(self, mouse):
        if mouse not in self._MStack:
            self._MStack.insert(0, mouse)

    def removeMouse(self, mouse):
        if mouse in self._MStack:
            self._MStack.remove(mouse)

    def checkMouse(self, mouse):
        return mouse in self._MStack and mouse is self._MStack[0]

    def entered(self):
        """返回鼠标悬停状态，在物体上->prop/在场景内->vmi/在场景外->None"""
        return self._PProp if self._PProp else (self._PView if self._PView else self)

    def enterEvent(self, ev):
        self._PView = self
        self._PProp, *_ = self.pickProp(ev.pos())
        self.mousexec([self._PView, self._PProp] + self._MStack, 'NoButton', 'Enter')

    def leaveEvent(self, ev):
        self.mousexec([self._PProp, self._PView] + self._MStack, 'NoButton', 'Leave')
        self._PView = self._PProp = None
        self._ButtonPress = self._ButtonPressMove = 'NoButton'

    def mouseMoveEvent(self, ev):
        self._MousePosLast, self._MousePos = self._MousePos, ev.pos()

        if self._ButtonPress == 'NoButton':
            prop, *_ = self.pickProp(ev.pos())
            last_prop, self._PProp = self._PProp, prop

            if not last_prop and not prop:
                self.mousexec(self._MStack + [self._PView], 'NoButton', 'Move')
            elif not last_prop and prop:
                self.mousexec([prop] + self._MStack, 'NoButton', 'Enter', prop)
            elif last_prop and not prop:
                self.mousexec([last_prop] + self._MStack, 'NoButton', 'Leave', last_prop)
            elif last_prop and prop and last_prop is prop:
                self.mousexec([self._PProp] + self._MStack + [self._PView], 'NoButton', 'Move')
            elif last_prop and prop and last_prop is not prop:
                self.mousexec([last_prop] + self._MStack, 'NoButton', 'Leave', last_prop)
                self.mousexec([prop] + self._MStack, 'NoButton', 'Enter', prop)
        elif self._MousePosLast != self._MousePos:
            self._ButtonPressMove = self._ButtonPress
            self.mousexec([self._PProp] + self._MStack + [self._PView], self._ButtonPressMove, 'PressMove')

    def mousePressEvent(self, ev):
        self._MousePosLast, self._MousePos = self._MousePos, ev.pos()

        if self._ButtonPress == 'NoButton':
            self._ButtonPress = ev.button().name.decode()
            self._DblClick = ev.type() == QEvent.Type.MouseButtonDblClick
            self.mousexec([self._PProp] + self._MStack + [self._PView], self._ButtonPress, 'Press',
                          double=self._DblClick)

    def mouseReleaseEvent(self, ev):
        self._MousePosLast, self._MousePos = self._MousePos, ev.pos()

        if self._ButtonPressMove == ev.button().name.decode():
            last_button = self._ButtonPress
            self._ButtonPress = self._ButtonPressMove = 'NoButton'
            self.mousexec([self._PProp] + self._MStack + [self._PView], last_button, 'PressMoveRelease')
        elif self._ButtonPress == ev.button().name.decode():
            last_button, last_double = self._ButtonPress, self._DblClick
            self._ButtonPress = self._ButtonPressMove = 'NoButton'
            self._DblClick = False
            self.mousexec([self._PProp] + self._MStack + [self._PView], last_button, 'PressRelease',
                          double=last_double)

    def mouseRotateFocal(self, **kwargs):
        dx, dy = self.mouseOverDisplay()
        rx, ry = -200 * dx / self.height(), 200 * dy / self.width()
        self.camera().Azimuth(rx)
        self.camera().Elevation(ry)
        self.camera().OrthogonalizeViewUp()
        self.updateInTime()

    def mousePan(self, **kwargs):
        over = self.mouseOverFPlane()
        fp, cp = self.camera('focal', 'position')
        fp = [fp[i] - over[i] for i in range(3)]
        cp = [cp[i] - over[i] for i in range(3)]
        self.camera().SetFocalPoint(fp)
        self.camera().SetPosition(cp)

        if self._Interactor.GetLightFollowCamera():
            self._Renderer.UpdateLightsGeometryToFollowCamera()

        self.updateInTime()

    def mouseZoom(self, **kwargs):
        c = self._Renderer.GetCenter()
        _, dy = self.mouseOverDisplay()
        factor = 1.1 ** (10 * -dy / c[1])

        if self.camera().GetParallelProjection():
            self.camera().SetParallelScale(self.camera().GetParallelScale() / factor)
        else:
            self.camera().Dolly(factor)

        if self._Interactor.GetLightFollowCamera():
            self._Renderer.UpdateLightsGeometryToFollowCamera()

        self.updateInTime()

    def mouseOverDisplay(self):
        """返回鼠标位移向量
        -> (dx, dy)"""
        return self._MousePos.x() - self._MousePosLast.x(), self._MousePos.y() - self._MousePosLast.y()

    def mouseOverFPlane(self, vt=None):
        """返回鼠标在焦平面上的位移向量
        -> (x, y, z)"""
        pt = self.pickFPlane(self._MousePos)
        ptLast = self.pickFPlane(self._MousePosLast)
        over = [pt[i] - ptLast[i] for i in range(3)]
        if vt is not None:
            over = vmi.vtOnVector(over, vt)
        return over

    def mousePos(self):
        """返回当前鼠标位置"""
        return self._MousePos

    def mousePosLast(self):
        """返回上一鼠标位置"""
        return self._MousePosLast

    def paintEngine(self):
        return None

    def paintEvent(self, ev):
        self._Interactor.Render()

    def pick(self, picker, pos: QPoint = None):
        """拾取场景对象"""
        pos = self._MousePos if pos is None else pos

        picker.Pick(pos.x(), self.height() - pos.y(), 0, self._Renderer)
        prop = picker.GetViewProp()
        prop = prop._Prop if prop else None
        return prop, picker.GetPickPosition(), picker

    def pickBBox(self, pos: QPoint):
        """拾取场景对象的包围盒
        pickBBox(QPoint(x, y)) -> (x, y, z)"""
        return self.pick(pos=pos, picker=self._Picker)

    def pickCell(self, pos: QPoint):
        """拾取场景对象的单元
        pickCell(QPoint(x, y)) -> (x, y, z)"""
        return self.pick(pos=pos, picker=self._PickerCell)

    def pickFPlane(self, pos: QPoint = None):
        """拾取场景的焦平面
        pickFPlane(QPoint(x, y)) -> (x, y, z)"""
        pos = self._MousePos if pos is None else pos

        t = [0] * 4
        vtk.vtkInteractorObserver.ComputeDisplayToWorld(
            self._Renderer, pos.x(), self.height() - pos.y(), 0, t)
        pt = [_ / t[3] for _ in t[:3]]

        fp, look = self.camera('focal', 'look')
        vtk.vtkPlane.ProjectPoint(pt, fp, look, pt)
        return pt

    def pickPoint(self, pos: QPoint):
        """拾取场景对象的点
        pickPoint(QPoint(x, y)) -> (x, y, z)"""
        return self.pick(pos=pos, picker=self._PickerPoint)

    def pickProp(self, pos: QPoint):
        """拾取场景对象
        pickProp(QPoint(x, y)) -> (x, y, z)"""
        return self.pick(pos=pos, picker=self._PickerProp)

    def pickToDisplay(self, pt):
        """拾取的场景坐标转换为屏幕坐标
        pickToDisplay((x, y, z) -> QPoint(x, y)"""
        t = [0] * 3
        vtk.vtkInteractorObserver.ComputeWorldToDisplay(
            self._Renderer, pt[0], pt[1], pt[2], t)
        return QPoint(t[0], self.height() - t[1])

    def pickToDisplayFlipY(self, pt):
        """拾取的场景坐标转换为屏幕坐标
        pickToDisplay((x, y, z) -> QPoint(x, y)"""
        t = [0] * 3
        vtk.vtkInteractorObserver.ComputeWorldToDisplay(
            self._Renderer, pt[0], pt[1], pt[2], t)
        return QPoint(t[0], t[1])

    def resizeEvent(self, ev):
        w = self.width()
        h = self.height()
        vtk.vtkRenderWindow.SetSize(self._RenderWindow, w, h)
        self._Interactor.SetSize(w, h)
        self._Interactor.ConfigureEvent()
        self.update()

    def setCamera(self, face=None, b6=None, focal=None):
        if face is not None:
            face = face.lower()
            vu = {'sagittal': [0, 0, 1],
                  'coronal': [0, 0, 1],
                  'axial': [0, -1, 0]}[face]
            vr = {'sagittal': [0, -1, 0],
                  'coronal': [1, 0, 0],
                  'axial': [1, 0, 0]}[face]
            vl = [0] * 3
            vtk.vtkMath.Cross(vu, vr, vl)

            fp = self.camera('focal')
            d = self.camera().GetDistance()
            cp = [fp[i] - d * vl[i] for i in range(3)]

            self.camera().SetPosition(cp)
            self.camera().SetFocalPoint(fp)
            self.camera().SetViewUp(vu)
            self._Renderer.ResetCameraClippingRange()
        if b6 is not None:
            if isinstance(b6, str) and b6.lower() == 'all':
                b6 = self._Renderer.ComputeVisiblePropBounds()
            b6 = list(b6)

            if focal is not None:
                c = [0.5 * (b6[0] + b6[1]), 0.5 * (b6[2] + b6[3]), 0.5 * (b6[4] + b6[5])]
                c = [focal[i] - c[i] for i in range(3)]
                for i in range(3):
                    if c[i] < 0:
                        b6[2 * i] += 2 * c[i]
                    else:
                        b6[2 * i + 1] += 2 * c[i]

            dxyz = b6[1] - b6[0], b6[3] - b6[2], b6[5] - b6[4]
            self._Renderer.ResetCamera(b6)

            vr, vu = self.camera('right', 'up')
            dr = [abs(_) / npl.norm(vr) for _ in vr]
            dr = dr[0] * dxyz[0] + dr[1] * dxyz[1] + dr[2] * dxyz[2]
            dr = dr if dr != 0 else 1
            du = [abs(_) / npl.norm(vu) for _ in vu]
            du = du[0] * dxyz[0] + du[1] * dxyz[1] + du[2] * dxyz[2]
            du = du if du != 0 else 1

            scale = 0.5 * du
            if du / dr < self.height() / self.width():
                scale = 0.5 * dr * self.height() / self.width()
            self.camera().SetParallelScale(scale)
        if focal is not None:
            vl = self.camera('look')
            b6 = self._Renderer.ComputeVisiblePropBounds()
            d = 0.5 * ((b6[1] - b6[0]) ** 2 + (b6[3] - b6[2]) ** 2 + (b6[5] - b6[4]) ** 2) ** 0.5
            cp = [focal[i] - d * vl[i] for i in range(3)]

            self.camera().SetPosition(cp)
            self.camera().SetFocalPoint(focal)
            self._Renderer.ResetCameraClippingRange()
        self.updateInTime()

    def setCameraFit(self):
        self.setCamera(b6='all')

    def setCameraReverse(self):
        fp, cp = self.camera('focal', 'position')
        for i in range(3):
            cp[i] = 2 * fp[i] - cp[i]
        self.camera().SetPosition(cp)
        self._Renderer.ResetCameraClippingRange()
        self.updateInTime()

    def setCameraAxial(self):
        self.setCamera(face='axial')

    def setCameraSagittal(self):
        self.setCamera(face='sagittal')

    def setCameraCoronal(self):
        self.setCamera(face='coronal')

    def setOrientationMarkerVisible(self, arg: bool):
        """显示/隐藏方位标"""
        self._OrientationMarker.GetOrientationMarker().SetVisibility(arg)
        self.updateInTime()

    def sizeHint(self):
        return QSize(1600, 900)

    def snapshot(self, file=None, *args):
        if file is None:
            file = vmi.askSaveFile(self.tr('快照 (Snapshot)'), '*.png')
        if file is not None:
            self.grab().save(file)
            vmi.askInfo('快照功能暂时无效')

    def timeout(self):
        if self._UpdateAtOnce:
            self.updateAtOnce()
        self._UpdateSum += 1

        if self._Time.elapsed() > 0.5e3:
            self._FPS = 1000 * self._UpdateSum / self._Time.elapsed()
            self.setWindowTitle(QApplication.applicationName() + ' FPS: {:.0f}'.format(self._FPS))
            self._Time.restart()
            self._UpdateSum = 0

    def updateInTime(self):
        """及时刷新视图"""
        self._UpdateAtOnce = True

    def updateAtOnce(self):
        if self._Timer.isActive():
            self._UpdateAtOnce = False
            self._Renderer.ResetCameraClippingRange()
            self._RenderWindow.Render()

    def wheelEvent(self, ev):
        d = ev.delta() / 120
        c, b, e = self.entered(), 'NoButton', 'Wheel'
        if not self.activated or 'pass' == self.activated.mouse[b][e](caller=c, delta=d):
            c.mouse[b][e](caller=c, delta=d)


def init_orientation_marker(i):
    """
    :param i: vtk.vtkRenderWindowInteractor
    :return: vtk.vtkOrientationMarkerWidget
    """

    vtk.vtkMapper.SetResolveCoincidentTopologyToPolygonOffset()

    cube = vtk.vtkAnnotatedCubeActor()
    cube.SetFaceTextScale(0.65)
    cube.SetXPlusFaceText("L")
    cube.SetXMinusFaceText("R")
    cube.SetYPlusFaceText("P")
    cube.SetYMinusFaceText("A")
    cube.SetZPlusFaceText("S")
    cube.SetZMinusFaceText("I")

    prop = cube.GetCubeProperty()
    prop.SetColor(0.75, 0.75, 1)

    prop = cube.GetTextEdgesProperty()
    prop.SetLineWidth(1)
    prop.SetDiffuse(0)
    prop.SetAmbient(1)
    prop.SetColor(0, 0, 0)

    prop = cube.GetXPlusFaceProperty()
    prop.SetColor(1, 0, 0)
    prop.SetInterpolationToFlat()
    prop = cube.GetXMinusFaceProperty()
    prop.SetColor(1, 0, 0)
    prop.SetInterpolationToFlat()
    prop = cube.GetYPlusFaceProperty()
    prop.SetColor(0, 1, 0)
    prop.SetInterpolationToFlat()
    prop = cube.GetYMinusFaceProperty()
    prop.SetColor(0, 1, 0)
    prop.SetInterpolationToFlat()
    prop = cube.GetZPlusFaceProperty()
    prop.SetColor(0, 0, 1)
    prop.SetInterpolationToFlat()
    prop = cube.GetZMinusFaceProperty()
    prop.SetColor(0, 0, 1)
    prop.SetInterpolationToFlat()

    axes = vtk.vtkAxesActor()

    axes.SetShaftTypeToCylinder()
    axes.SetXAxisLabelText("X")
    axes.SetYAxisLabelText("Y")
    axes.SetZAxisLabelText("Z")

    axes.SetTotalLength(1.5, 1.5, 1.5)
    axes.SetCylinderRadius(0.500 * axes.GetCylinderRadius())
    axes.SetConeRadius(1.025 * axes.GetConeRadius())
    axes.SetSphereRadius(1.500 * axes.GetSphereRadius())

    prop = axes.GetXAxisCaptionActor2D().GetCaptionTextProperty()
    prop.BoldOn()
    prop.ItalicOn()
    prop.ShadowOn()
    prop.SetFontFamilyToArial()
    prop.SetColor(1, 0, 0)

    prop = axes.GetYAxisCaptionActor2D().GetCaptionTextProperty()
    prop.BoldOn()
    prop.ItalicOn()
    prop.ShadowOn()
    prop.SetFontFamilyToArial()
    prop.SetColor(0, 1, 0)

    prop = axes.GetZAxisCaptionActor2D().GetCaptionTextProperty()
    prop.BoldOn()
    prop.ItalicOn()
    prop.ShadowOn()
    prop.SetFontFamilyToArial()
    prop.SetColor(0, 0, 1)

    assembly = vtk.vtkPropAssembly()
    assembly.AddPart(axes)
    assembly.AddPart(cube)

    ort = vtk.vtkOrientationMarkerWidget()
    ort.SetOrientationMarker(assembly)
    ort.SetViewport(0.0, 0.0, 0.2, 0.2)
    ort.SetInteractor(i)
    ort.SetEnabled(1)
    ort.SetInteractive(0)
    ort.On()

    return ort


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setOrganizationName('vmi')
    app.setApplicationName('vmi')

    w = View()
    w.show()
    w._Renderer.SetBackground(1, 0.5, 0.5)

    import shelve

    with shelve.open('C:/Users/Medraw/Desktop/d') as db:
        db['w'] = w

    with shelve.open('C:/Users/Medraw/Desktop/d') as db:
        v = db['w']
        v.show()

    sys.exit(app.exec_())
