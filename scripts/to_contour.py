import argparse
import vtk
from vtk.util import numpy_support
import json
import numpy as np
from tqdm import tqdm

def save_json(fn, data):
    with open(fn, 'w') as outfile:
        json.dump(data, outfile)

def load_json(fn):
    with open(fn) as f:
        return json.load(f)

def denormalizeContour(c,p,t,tx):
    """
    uses simvascular path info to transform a contour from 2d to 3d

    args:
        c (np array, (num points x 2)) - contour to transform
        p (np array 1x3) - 3d origin of contour
        t (np array 1x3) - normal vector of 3d contour
        tx (np array 1x3) - vector in 3d contour plane

    returns:
        res (np array, (num points x 3)) - 3d contour
    """
    c = np.array(c)
    if c.shape[1] == 2:
        c = np.hstack((c, np.zeros((c.shape[0],1))))
    p = np.array(p)
    t = np.array(t)
    tx = np.array(tx)

    ty = np.cross(t,tx)
    ty = ty/np.linalg.norm(ty)

    res = np.array([p + k[0]*tx + k[1]*ty for k in c])
    return res[:-1]

def reorder_contour(c):
    N = len(c)
    if N <= 2:
        return c
    even_inds = np.arange(0,N,2)
    odd_inds = np.arange(1,N,2)

    even_points = np.asarray([c[i] for i in even_inds])
    odd_points = np.asarray([c[i] for i in odd_inds])

    N_even = len(even_points)
    ret = np.zeros_like(c)
    ret[:N_even] = even_points
    ret[N_even:] = np.flipud(odd_points)
    ret = ret[:-2]
    return ret.copy()

def VTKPDPointstoNumpy(pd):
	'''
	function to convert the points data of a vtk polydata object to a numpy array

	args:
		@a pd: vtk.vtkPolyData object
	'''
	return numpy_support.vtk_to_numpy(pd.GetPoints().GetData())

def VTKNumpytoSP(img_):
    img = img_.T

    H,W = img.shape

    sp = vtk.vtkStructuredPoints()
    sp.SetDimensions(H,W,1)
    sp.AllocateScalars(10,1)
    for i in range(H):
        for j in range(W):
            v = img[i,j]
            sp.SetScalarComponentFromFloat(i,j,0,0,v)

    return sp

def marchingSquares(img, iso=0.0, mode='center'):
    s = img.shape
    alg = vtk.vtkMarchingSquares()

    sp = VTKNumpytoSP(img)

    alg.SetInputData(sp)
    alg.SetValue(0,iso)
    alg.Update()
    pds = alg.GetOutput()

    a = vtk.vtkPolyDataConnectivityFilter()
    a.SetInputData(pds)

    if mode=='center':
        a.SetExtractionModeToClosestPointRegion()
        a.SetClosestPoint(float(s[0])/2,float(s[1])/2,0.0)

    elif mode=='all':
        a.SetExtractionModeToAllRegions()

    a.Update()
    pds = a.GetOutput()

    if pds.GetPoints() is None:
        return np.asarray([[0.0,0.0],[0.0,0.0]])
    else:
        pds = VTKPDPointstoNumpy(pds)
        if len(pds) <= 1:
            return np.asarray([[0.0,0.0],[0.0,0.0]])
        return pds[:,:2]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_files", nargs="+")
    parser.add_argument('output_directory')
    parser.add_argument('-i', default=0.5, type=float, help="marching cubes isovalue")
    args = parser.parse_args()
    print args

    for f in tqdm(args.input_files):
        d = load_json(f)
        image = np.array(d['image'])
        cont = marchingSquares(image, args.i)
        cont = reorder_contour(cont)
        d['contour'] = cont.tolist()
        d['contour_2d'] = (cont*d['spacing']).tolist()

        p = d['p']
        n = d['n']
        x = d['x']

        d['contour_3d'] = denormalizeContour(cont*d['spacing'],p,n,x).tolist()
        fn = d['name']+'.json'
        o_fn = args.output_directory+fn
        save_json(o_fn, d)
