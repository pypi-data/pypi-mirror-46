import tempfile
import pathlib
import itk
import itkTypes
import vtk
import vmi

UC = itkTypes.UC
SS = itkTypes.SS
F = itkTypes.F
D = itkTypes.D

ImageUC3 = itk.Image[UC, 3]
ImageS3 = itk.Image[SS, 3]
ImageF3 = itk.Image[F, 3]


def toITKType(t):
    return {vtk.VTK_UNSIGNED_CHAR: UC,
            vtk.VTK_SHORT: SS,
            vtk.VTK_FLOAT: F,
            vtk.VTK_DOUBLE: D}[t]


def toVTKType(t):
    return {UC: vtk.VTK_UNSIGNED_CHAR,
            SS: vtk.VTK_SHORT,
            F: vtk.VTK_FLOAT,
            D: vtk.VTK_DOUBLE}[t]


def toITKImage(image: vtk.vtkImageData, itktype=UC):
    if isinstance(image, vtk.vtkImageData):
        with tempfile.TemporaryDirectory() as p:
            p = pathlib.Path(p) / '.nii'
            w = vtk.vtkNIFTIImageWriter()
            w.SetFileName(str(p))
            w.SetInputData(image)
            w.Update()
            return itk.imread(str(p), itktype)
    else:
        with tempfile.TemporaryDirectory() as p:
            p = pathlib.Path(p) / '.nii'
            itk.imwrite(image, str(p))
            return itk.imread(str(p), itktype)


def toVTKImage(itkimage):
    with tempfile.TemporaryDirectory() as p:
        p = pathlib.Path(p) / '.nii'
        itk.imwrite(itkimage, str(p))
        r = vtk.vtkNIFTIImageReader()
        r.SetFileName(str(p))
        r.Update()
        return r.GetOutput()
    

def imOrigin(vtkimage):
    return list(vtkimage.GetOrigin())


def imBounds(vtkimage):
    return list(vtkimage.GetBounds())


def imCenter(vtkimage):
    return list(vtkimage.GetCenter())


def imDimensions(vtkimage):
    return list(vtkimage.GetDimensions())


def imExtent(vtkimage, bounds=None):
    if bounds is not None:
        ori, spc, ext = imOrigin(vtkimage), imSpacing(vtkimage), imExtent(vtkimage)
        first, last = [bounds[0], bounds[2], bounds[4]], [bounds[1], bounds[3], bounds[5]]
        for i in range(3):
            f = int((first[i] - ori[i]) / spc[i])
            l = int((last[i] - ori[i]) / spc[i] + 1)
            if f > ext[2 * i]:
                ext[2 * i] = f
            if l < ext[2 * i + 1]:
                ext[2 * i + 1] = l
        return ext
    return list(vtkimage.GetExtent())


def imSpacing(vtkimage, normal=None):
    if normal is not None:
        n3, spc = [abs(_) for _ in vmi.normalized3(normal)], imSpacing(vtkimage)
        return n3[0] * spc[0] + n3[1] * spc[1] + n3[2] * spc[2]
    return list(vtkimage.GetSpacing())


def imLength(vtkimage, normal=None):
    if normal is not None:
        n3, lth = [abs(_) for _ in vmi.normalized3(normal)], imLength(vtkimage)
        return n3[0] * lth[0] + n3[1] * lth[1] + n3[2] * lth[2]
    bnd = imBounds(vtkimage)
    return [bnd[1] - bnd[0], bnd[3] - bnd[2], bnd[5] - bnd[4]]


def imStencil(vtkimage, polydata):
    stencil = vtk.vtkPolyDataToImageStencil()
    stencil.SetInputData(polydata)
    stencil.SetOutputOrigin(imOrigin(vtkimage))
    stencil.SetOutputSpacing(imSpacing(vtkimage))
    stencil.SetOutputWholeExtent(imExtent(vtkimage))
    stencil.Update()
    return stencil.GetOutput()


def imIterator(vtkimage, ext=None, stencil=None):
    it = vtk.vtkImagePointIterator()
    it.Initialize(vtkimage, ext, stencil)
    return it


def imScalar(vtkimage, ijk=None, value=None, m=0):
    if value is not None:
        vtkimage.SetScalarComponentFromDouble(ijk[0], ijk[1], ijk[2], m, value)
        vtkimage.Modified()
    return vtkimage.GetScalarComponentAsDouble(ijk[0], ijk[1], ijk[2], m)


def imResample(vtkimage, origin, extent, spacing):
    resample = vtk.vtkImageReslice()
    resample.SetInputData(vtkimage)
    resample.SetInterpolationModeToCubic()
    resample.SetOutputOrigin(origin)
    resample.SetOutputExtent(extent)
    resample.SetOutputSpacing(spacing)
    resample.Update()
    return resample.GetOutput()


def imResampleIsotropic(vtkimage: vtk.vtkImageData):
    spc = imSpacing(vtkimage)
    isospc = (spc[0] * spc[1] * spc[2]) ** (1 / 3)

    itkimage = toITKImage(vtkimage, F)

    smooth = itk.RecursiveGaussianImageFilter[ImageF3, ImageF3].New()
    smooth.SetInput(itkimage)
    smooth.SetDirection(0)
    smooth.SetSigma(isospc)
    smooth.Update()
    itkimage = smooth.GetOutput()

    smooth = itk.RecursiveGaussianImageFilter[ImageF3, ImageF3].New()
    smooth.SetInput(itkimage)
    smooth.SetDirection(1)
    smooth.SetSigma(isospc)
    smooth.Update()
    itkimage = smooth.GetOutput()

    size = itkimage.GetLargestPossibleRegion().GetSize()
    dx = size[0] * spc[0] / isospc
    dy = size[1] * spc[1] / isospc
    dz = size[2] * spc[2] / isospc

    resample = itk.ResampleImageFilter[ImageF3, ImageF3].New()
    resample.SetInput(itkimage)
    resample.SetTransform(itk.IdentityTransform[D, 3].New())
    resample.SetInterpolator(itk.LinearInterpolateImageFunction[ImageF3, D].New())
    resample.SetDefaultPixelValue(-3071)
    resample.SetOutputSpacing([isospc, isospc, isospc])
    resample.SetOutputOrigin(itkimage.GetOrigin())
    resample.SetOutputDirection(itkimage.GetDirection())
    resample.SetSize([int(dx), int(dy), int(dz)])
    resample.Update()
    itkimage = resample.GetOutput()

    itkimage = toITKImage(itkimage, toITKType(vtkimage.GetScalarType()))
    return toVTKImage(itkimage)
