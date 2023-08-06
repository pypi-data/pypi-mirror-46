import sys

import vtk
from PySide2.QtCore import *
from PySide2.QtOpenGL import QGLWidget
from PySide2.QtWidgets import *

import convert


class Mouse:
    def __init__(self):
        self._Enter = self._Leave = self._Wheel = self._Move = self.none
        self._LeftButtonPress = self._LeftButtonPressMove = self.none
        self._LeftButtonPressMoveRelease = self._LeftButtonPressRelease = self.none
        self._MidButtonPress = self._MidButtonPressMove = self.none
        self._MidButtonPressMoveRelease = self._MidButtonPressRelease = self.none
        self._RightButtonPress = self._RightButtonPressMove = self.none
        self._RightButtonPressMoveRelease = self._RightButtonPressRelease = self.none

        self.mouse = {
            b'NoButton': {
                'Enter': self._Enter,
                'Leave': self._Leave,
                'Wheel': self._Wheel,
                'Move': self._Move},
            b'LeftButton': {
                'Press': self._LeftButtonPress,
                'PressMove': self._LeftButtonPressMove,
                'PressMoveRelease': self._LeftButtonPressMoveRelease,
                'PressRelease': self._LeftButtonPressRelease},
            b'MidButton': {
                'Press': self._MidButtonPress,
                'PressMove': self._MidButtonPressMove,
                'PressMoveRelease': self._MidButtonPressMoveRelease,
                'PressRelease': self._MidButtonPressRelease},
            b'RightButton': {
                'Press': self._RightButtonPress,
                'PressMove': self._RightButtonPressMove,
                'PressMoveRelease': self._RightButtonPressMoveRelease,
                'PressRelease': self._RightButtonPressRelease}}

    @staticmethod
    def none(**kwargs): pass


class Widget(Mouse, QGLWidget):
    """vtk场景"""

    def __init__(self, parent=None):
        Mouse.__init__(self)
        QGLWidget.__init__(self, parent)

        self.setAttribute(Qt.WA_OpaquePaintEvent)
        self.setAttribute(Qt.WA_PaintOnScreen)
        self.setFocusPolicy(Qt.WheelFocus)
        self.setMouseTracking(True)

        # 渲染器
        self._Renderer = vtk.vtkRenderer()
        self._Renderer.SetUseHiddenLineRemoval(1)  # 隐线消除
        self._Renderer.SetUseFXAA(False)  # 快速近似抗锯齿

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
        self._Hidden.destroyed.connect(self._Finalize)

        # 更新请求
        self._UpdateAtOnce: bool = False

        # 鼠标位置
        self._MousePosLast: QPoint = QPoint(0, 0)
        self._MousePos: QPoint = QPoint(0, 0)

        # 鼠标正在交互的对象
        self._PropEnter: vtk.vtkProp = None
        self._ViEnter: Widget = None

        # 鼠标按键状态
        self._ButtonPress = self._ButtonPressMove = b'NoButton'

    def __setstate__(self, s):
        self.__init__()
        self.__dict__.update(s)

        for kw in s['_VTKGets']:
            convert.vtkset(getattr(self, kw), s['_VTKGets'][kw])

    def __getstate__(self):
        s = self.__dict__.copy()

        s['_VTKGets'] = {name: convert.vtkget(getattr(self, name)) for name in
                         ['_RenderWindow', '_Renderer', '_Interactor', '_Camera',
                          '_Picker', '_PickerProp', '_PickerPoint', '_PickerCell']}

        for kw in s['_VTKGets']:
            del s[kw]
        del s['_OrientationMarker'], s['_Timer'], s['_Hidden'], s['__METAOBJECT__']
        return s

    def _Finalize(self):
        self._Timer.stop()
        self._RenderWindow.Finalize()

    def closeEvent(self, ev):
        self._Finalize()

    def updateInTime(self):
        """及时刷新视图"""
        self._UpdateAtOnce = True

    def updateAtOnce(self):
        """立即刷新视图"""
        self._Renderer.ResetCameraClippingRange()
        self._RenderWindow.Render()
        self._UpdateSum += 1

    def timeout(self):
        if self._UpdateAtOnce:
            self._UpdateAtOnce = False
        self.updateAtOnce()

        if self._Time.elapsed() > 0.5e3:
            self._FPS = 1000 * self._UpdateSum / self._Time.elapsed()
            self.setWindowTitle('FPS: {:.0f}'.format(self._FPS))
            self._Time.restart()
            self._UpdateSum = 0

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

            t, value = [], {'fp': fp, 'cp': cp, 'up': up, 'look': look, 'right': right}
            for key in args:
                if key in value.keys():
                    t.append(value[key])
            return t

    def sizeHint(self):
        return QSize(400, 400)

    def paintEngine(self):
        return None

    def paintEvent(self, ev):
        self._Interactor.Render()

    def resizeEvent(self, ev):
        w = self.width()
        h = self.height()
        vtk.vtkRenderWindow.SetSize(self._RenderWindow, w, h)
        self._Interactor.SetSize(w, h)
        self._Interactor.ConfigureEvent()
        self.update()

    def setOrientationMarkerVisible(self, arg: bool):
        """显示/隐藏方位标"""
        self._OrientationMarker.GetOrientationMarker().SetVisibility(arg)
        self.updateInTime()

    def mouseButtonRotateFocal(self, **kwargs):
        if kwargs['event'] == 'PressMove':
            dx, dy = self.mouseOverDisplay()
            rx, ry = -200 * dx / self.height(), 200 * dy / self.width()
            self.camera().Azimuth(rx)
            self.camera().Elevation(ry)
            self.camera().OrthogonalizeViewUp()
            self.updateInTime()

    def mouseButtonPan(self, **kwargs):
        if kwargs['event'] == 'PressMove':
            dp = self.mouseOverFPlane()
            fp, cp = self.camera('fp', 'cp')
            fp = [fp[i] - dp[i] for i in range(3)]
            cp = [cp[i] - dp[i] for i in range(3)]
            self.camera().SetFocalPoint(fp)
            self.camera().SetPosition(cp)

            if self._Interactor.GetLightFollowCamera():
                self._Renderer.UpdateLightsGeometryToFollowCamera()

            self.updateInTime()

    def mouseButtonZoom(self, **kwargs):
        if kwargs['event'] == 'PressMove':
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

    def setMouseStyle(self, style):
        if style.lower() == 'none':
            for b in self.mouse:
                for e in self.mouse[b]:
                    self.mouse[b][e] = self.none
        elif style.lower() == 'volume':
            self.setMouseStyle('none')
            for e in self.mouse[b'LeftButton']:
                self.mouse[b'LeftButton'][e] = self.mouseButtonRotateFocal
            for e in self.mouse[b'MidButton']:
                self.mouse[b'MidButton'][e] = self.mouseButtonPan
            for e in self.mouse[b'RightButton']:
                self.mouse[b'RightButton'][e] = self.mouseButtonZoom
        elif style.lower() == 'slice':
            self.setMouseStyle('none')

    def mousePos(self):
        """返回当前鼠标位置"""
        return self._MousePos.x(), self._MousePos.y()

    def mousePosLast(self):
        """返回上一鼠标位置"""
        return self._MousePosLast.x(), self._MousePosLast.y()

    def mouseOverDisplay(self):
        """返回鼠标位移向量
        -> (dx, dy)"""
        return self._MousePos.x() - self._MousePosLast.x(), self._MousePos.y() - self._MousePosLast.y()

    def mouseOverFPlane(self):
        """返回鼠标在焦平面上的位移向量
        -> (x, y, z)"""
        pt = self.pickFPlane(self._MousePos)
        ptLast = self.pickFPlane(self._MousePosLast)
        return [pt[i] - ptLast[i] for i in range(3)]

    def entered(self):
        """返回鼠标悬停状态，在物体上->prop/在场景内->vmi/在场景外->None"""
        return self._PropEnter if self._PropEnter else (self._ViEnter if self._ViEnter else self)

    def enterEvent(self, ev):
        self._ViEnter = self
        c, b, e = self, b'NoButton', 'Enter'
        c.mouse[b][e](caller=c, event=e, button=b)

        self._PropEnter, *_ = self.pickProp(ev.pos())
        if self._PropEnter:
            c = self._PropEnter
            c.mouse[b][e](caller=c, event=e, button=b)

    def leaveEvent(self, ev):
        if self._ViEnter:
            c, b, e = self, b'NoButton', 'Leave'
            c.mouse[b][e](caller=c, event=e, button=b)
        if self._PropEnter:
            c, b, e = self._PropEnter, b'NoButton', 'Leave'
            c.mouse[b][e](caller=c, event=e, button=b)
        self._ViEnter = self._PropEnter = None

    def wheelEvent(self, ev):
        d = ev.delta() / 120
        c, b, e = self.entered(), b'NoButton', 'Wheel'
        c.mouse[b][e](caller=c, event=e, button=b, delta=d)

    def mouseMoveEvent(self, ev):
        self._MousePosLast, self._MousePos = self._MousePos, ev.pos()

        if self._ButtonPress == b'NoButton':
            prop, *_ = self.pickProp(ev.pos())
            last_prop, self._PropEnter = self._PropEnter, prop

            if not last_prop and not prop:
                c, b, e = self, b'NoButton', 'Move'
                c.mouse[b][e](caller=c, event=e, button=b)
            elif not last_prop and prop:
                c, b, e = prop, b'NoButton', 'Enter'
                c.mouse[b][e](caller=c, event=e, button=b)
            elif last_prop and not prop:
                c, b, e = last_prop, b'NoButton', 'Leave'
                c.mouse[b][e](caller=c, event=e, button=b)
            elif last_prop and prop and last_prop is prop:
                c, b, e = prop, b'NoButton', 'Move'
                c.mouse[b][e](caller=c, event=e, button=b)
            elif last_prop and prop and last_prop is not prop:
                c, b, e = last_prop, b'NoButton', 'Leave'
                c.mouse[b][e](caller=c, event=e, button=b)
                c, b, e = prop, b'NoButton', 'Enter'
                c.mouse[b][e](caller=c, event=e, button=b)
        else:
            self._ButtonPressMove = self._ButtonPress
            c, b, e = self.entered(), self._ButtonPressMove, 'PressMove'
            c.mouse[b][e](caller=c, event=e, button=b)

    def mousePressEvent(self, ev):
        if self._ButtonPress == b'NoButton':
            self._ButtonPress = ev.button().name
            d = ev.type() == QEvent.Type.MouseButtonDblClick
            c, b, e = self.entered(), self._ButtonPress, 'Press'
            c.mouse[b][e](caller=c, event=e, button=b, double=d)

    def mouseReleaseEvent(self, ev):
        if ev.button().name == self._ButtonPressMove:
            c, b, e = self.entered(), self._ButtonPressMove, 'PressMoveRelease'
            c.mouse[b][e](caller=c, event=e, button=b)
            self._ButtonPress = self._ButtonPressMove = b'NoButton'
        elif ev.button().name == self._ButtonPress:
            c, b, e = self.entered(), self._ButtonPress, 'PressRelease'
            c.mouse[b][e](caller=c, event=e, button=b)
            self._ButtonPress = self._ButtonPressMove = b'NoButton'

    def _pick(self, pos: QPoint, picker=None):
        """拾取场景对象"""

        picker.Pick(pos.x(), self.height() - pos.y(), 0, self._Renderer)
        prop = picker.GetViewProp()
        prop = prop._Prop if prop else None
        return prop, picker.GetPickPosition(), picker

    def pickBBox(self, pos: QPoint):
        """拾取场景对象的包围盒
        pickBBox(QPoint(x, y)) -> (x, y, z)"""
        return self._pick(pos=pos, picker=self._Picker)

    def pickProp(self, pos: QPoint):
        """拾取场景对象
        pickProp(QPoint(x, y)) -> (x, y, z)"""
        return self._pick(pos=pos, picker=self._PickerProp)

    def pickPoint(self, pos: QPoint):
        """拾取场景对象的点
        pickPoint(QPoint(x, y)) -> (x, y, z)"""
        return self._pick(pos=pos, picker=self._PickerPoint)

    def pickCell(self, pos: QPoint):
        """拾取场景对象的单元
        pickCell(QPoint(x, y)) -> (x, y, z)"""
        return self._pick(pos=pos, picker=self._PickerCell)

    def pickFPlane(self, pos: QPoint):
        """拾取场景的焦平面
        pickFPlane(QPoint(x, y)) -> (x, y, z)"""
        t = [0] * 4
        vtk.vtkInteractorObserver.ComputeDisplayToWorld(
            self._Renderer, pos.x(), self.height() - pos.y(), 0, t)
        pt = [_ / t[3] for _ in t[:3]]

        fp, look = self.camera('fp', 'look')
        vtk.vtkPlane.ProjectPoint(pt, fp, look, pt)
        return pt

    def pickToDisplay(self, pt: list):
        """拾取的场景坐标转换为屏幕坐标
        pickToDisplay((x, y, z) -> QPoint(x, y)"""
        t = [0] * 3
        vtk.vtkInteractorObserver.ComputeWorldToDisplay(
            self._Renderer, pt[0], pt[1], pt[2], t)
        return QPoint(t[0], self.height() - t[1])


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
    app.setOrganizationName('Vi')
    app.setApplicationName('Vi')

    w = Widget()
    w.show()
    w.setMouseStyle('Volume')
    w._Renderer.SetBackground(1, 0.5, 0.5)

    # import shelve
    #
    # with shelve.open('db') as db:
    #     db['w'] = w
    #
    # with shelve.open('db') as db:
    #     v = db['w']
    #     v.show()

    sys.exit(app.exec_())
