import sys
import pathlib
import tempfile
from pprint import pprint

from PySide2.QtCore import *
from PySide2.QtWidgets import *
import vtk

vtkget_ignore = ('GetDebug', 'GetGlobalReleaseDataFlag', 'GetGlobalWarningDisplay', 'GetReferenceCount',
                 'GetAAFrames', 'GetFDFrames', 'GetSubFrames', 'GetUseConstantFDOffsets', 'GetStereoCapableWindow',
                 'GetForceCompileOnly', 'GetGlobalImmediateModeRendering', 'GetImmediateModeRendering',
                 'GetScalarMaterialMode', 'GetReleaseDataFlag')


def vtkset(self, gets: dict):
    for getname in gets:
        setname = getname.replace('Get', 'Set', 1)
        try:
            getattr(self, setname)(gets[getname])
        except TypeError:
            pass


def vtkget(self):
    gets = {}
    for getname in dir(self):
        if getname.startswith('Get'):
            setname = getname.replace('Get', 'Set', 1)
            if hasattr(self, setname) and getname not in vtkget_ignore:
                try:
                    a = getattr(self, getname)()
                    if 'vtk' not in str(type(a)):
                        gets[getname] = a
                except TypeError:
                    pass
    return gets


def dumps(arg):
    if isinstance(arg, vtk.vtkImageData):
        if arg.GetNumberOfPoints() == 0:
            return ['vtkImageData', bytes()]
        else:
            with tempfile.TemporaryDirectory() as p:
                p = pathlib.Path(p) / '.nii'
                w = vtk.vtkNIFTIImageWriter()
                w.SetFileName(str(p))
                w.SetInputData(arg)
                w.Update()
                return ['vtkImageData', p.read_bytes()]
    elif isinstance(arg, vtk.vtkPolyData):
        if arg.GetNumberOfPoints() == 0:
            return ['vtkPolyData', bytes()]
        else:
            with tempfile.TemporaryDirectory() as p:
                p = pathlib.Path(p) / '.vtp'
                w = vtk.vtkPolyDataWriter()
                w.SetFileTypeToBinary()
                w.SetFileName(str(p))
                w.SetInputData(arg)
                w.Update()
                return ['vtkPolyData', p.read_bytes()]
    elif isinstance(arg, vtk.vtkLookupTable):
        p = {'GetNumberOfTableValues': arg.GetNumberOfTableValues(),
             'GetTableRange': arg.GetTableRange(),
             'GetBelowRangeColor': arg.GetBelowRangeColor(),
             'GetAboveRangeColor': arg.GetAboveRangeColor(),
             'GetUseBelowRangeColor': arg.GetUseBelowRangeColor(),
             'GetUseAboveRangeColor': arg.GetUseAboveRangeColor(),
             'GetTableValue': []}
        for i in range(arg.GetNumberOfTableValues()):
            p['GetTableValue'].append(arg.GetTableValue(i))
        return ['vtkLookupTable', p]
    raise TypeError(type(arg))


def loads(arg):
    if arg[0] == 'vtkImageData':
        if len(arg[1]) == 0:
            return vtk.vtkImageData()
        else:
            with tempfile.TemporaryDirectory() as p:
                p = pathlib.Path(p) / '_'
                p.write_bytes(arg[1])
                r = vtk.vtkNIFTIImageReader()
                r.SetFileName(str(p))
                r.Update()
                return r.GetOutput()
    elif arg[0] == 'vtkPolyData':
        if len(arg[1]) == 0:
            return vtk.vtkPolyData()
        else:
            with tempfile.TemporaryDirectory() as p:
                p = pathlib.Path(p) / '_'
                p.write_bytes(arg[1])
                r = vtk.vtkPolyDataReader()
                r.SetFileName(str(p))
                r.Update()
                return r.GetOutput()
    elif arg[0] == 'vtkLookupTable':
        r = vtk.vtkLookupTable()
        r.SetNumberOfTableValues(arg[1]['GetNumberOfTableValues'])
        r.SetTableRange(arg[1]['GetTableRange'])
        r.SetBelowRangeColor(arg[1]['GetBelowRangeColor'])
        r.SetAboveRangeColor(arg[1]['GetAboveRangeColor'])
        r.SetUseBelowRangeColor(arg[1]['GetUseBelowRangeColor'])
        r.SetUseAboveRangeColor(arg[1]['GetUseAboveRangeColor'])
        for i in range(arg[1]['GetNumberOfTableValues']):
            r.SetTableValue(i, arg[1]['GetTableValue'][i])
        return r
    raise TypeError(arg[0])


if __name__ == '__main__':
    f = vtk.vtkPiecewiseFunction()
    f.Point = {}
    f.AddPoint(-1024, 1)
    f.Point[-1024] = 1

    import shelve
    from pickle import HIGHEST_PROTOCOL

    with shelve.open('db', 'n', HIGHEST_PROTOCOL) as db:
        db['l'] = dumps(f)
        f = loads(db['l'])
        print(f)
    sys.exit()

    reader = vtk.vtkSTLReader()
    reader.SetFileName('C:/Users/Medraw/Desktop/1.stl')
    reader.Update()

    loads(dumps(reader.GetOutput())[1])

    from time import sleep

    sleep(5)
    print('EXIT_SUCCESS')

    # with shelve.open('db', 'n', HIGHEST_PROTOCOL) as db:
    #     db['w'] = tempfile.TemporaryFile( )
