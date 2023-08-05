import sys

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import vtk

from vmi import vio
from vmi.view import Mouse, View


class TextActor(Mouse, QObject):
    """场景表示，聚合数据的表示
        vtk.vtkPolyData -> vtk.vtkActor"""

    def __init__(self, w: View):
        Mouse.__init__(self, w)
        QObject.__init__(self)

        self.prop = vtk.vtkTextActor()
