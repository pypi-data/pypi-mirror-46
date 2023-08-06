import vtk
import vmi


def add3(a, b):
    return [a[i] + b[i] for i in range(3)]


def addm3(scalars, vectors, origin=(0, 0, 0)):
    aa = [*origin]
    n = min(len(scalars), len(vectors))
    for j in range(n):
        for i in range(3):
            aa[i] += scalars[j] * vectors[j][i]
    return aa


def subtract3(a, b):
    return [a[i] - b[i] for i in range(3)]


def distance3(a, b):
    return norm3(subtract3(a, b))


def dot3(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross3(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def sign3(a, b):
    return 1 if dot3(a, b) > 0 else (-1 if dot3(a, b) < 0 else 0)


def norm3(a):
    return (a[0] ** 2 + a[1] ** 2 + a[2] ** 2) ** 0.5


def signNorm3(a, b):
    return sign3(a, b) * norm3(a)


def normalized3(a):
    norm = norm3(a)
    if norm > 0:
        return [_ / norm for _ in a]
    return [0, 0, 0]


def trsfLandmark(pts0, pts1, mode='rigidbody'):
    if len(pts0) > 2 and len(pts1) > 2:
        pts = [vtk.vtkPoints(), vtk.vtkPoints()]
        for pt in pts0:
            pts[0].InsertNextPoint(pt)
        for pt in pts1:
            pts[1].InsertNextPoint(pt)

        modes = {'rigidbody': vtk.VTK_LANDMARK_RIGIDBODY,
                 'similarity': vtk.VTK_LANDMARK_SIMILARITY,
                 'affine': vtk.VTK_LANDMARK_AFFINE}
        ts = vtk.vtkLandmarkTransform()
        ts.SetSourceLandmarks(pts[0])
        ts.SetTargetLandmarks(pts[1])
        if mode in modes:
            ts.SetMode(modes[mode])
        else:
            ts.SetModeToRigidBody()
        ts.Update()
        return ts


def ptOnPlane(pt, origin, normal):
    t = dot3([pt[i] - origin[i] for i in range(3)], normal)
    return [pt[i] - t * normal[i] for i in range(3)]


def ptsOBB(pts):
    if pts.GetNumberOfPoints() > 0:
        args = {'origin': [0, 0, 0], 'axis': [[0, 0, 0], [0, 0, 0], [0, 0, 0]], 'size': [0, 0, 0]}
        vtk.vtkOBBTree().ComputeOBB(pts, args['origin'], args['axis'][0], args['axis'][1], args['axis'][2],
                                    args['size'])

        args['center'] = args['origin']
        for j in range(3):
            args['axis'][j] = normalized3(args['axis'][j])
            args['center'] = [args['center'][i] + 0.5 * args['size'][j] * args['axis'][j][i] for i in range(3)]
        return args


def vtOnPlane(vt, normal):
    n2 = dot3(normal, normal)
    n2 = n2 if n2 != 0 else 1
    t = dot3(vt, normal)
    return [vt[i] - t * normal[i] / n2 for i in range(3)]


def vtOnVector(vt, vector):
    dot = dot3(vector, vector)
    if dot == 0:
        return [0, 0, 0]

    dot = dot3(vt, vector) / dot
    return [dot * vector[i] for i in range(3)]
