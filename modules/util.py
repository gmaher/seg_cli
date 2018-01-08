import vtk
import os
from vtk.util import numpy_support
import numpy as np
import json

def mkdir(fn):
    if not os.path.exists(os.path.abspath(fn)):
        os.mkdir(os.path.abspath(fn))

def load_json(fn):
    with open(fn) as f:
        return json.load(f)

def save_json(fn, data):
    with open(fn, 'w') as outfile:
        json.dump(data, outfile)

def args_to_dict(args):
    keys = args[::2]
    vals = args[1::2]
    d = {}
    for k,v in zip(keys,vals): d[k] = v
    return d

def convert_to_json_list(paths_file, output_directory):
    if ".paths" in paths_file:
        d = parsePathFile(paths_file)
        d = convert_path_dict(d)
    else:
        raise RuntimeError("Unsupported paths_file type".format(paths_file))

    files_file = output_directory+"/path_files.txt"
    f = open(files_file,'w')
    dir_ = output_directory+'/path'
    mkdir(dir_)
    for i in range(len(d)):
        fn = os.path.abspath(dir_+'/{}.json'.format(i))
        save_json(fn, d[i])
        f.write(fn+"\n")
    f.close()
    return files_file

def load_mha(filename):
    reader = vtk.vtkMetaImageReader()
    return read_vtk_image(reader, filename)

def load_vti(filename):
    reader = vtk.vtkXMLImageDataReader()
    return read_vtk_image(reader, filename)

def load_dcm(filename):
    reader = vtk.vtkDICOMImageReader()
    if ".dcm" in filename:
        filename = filename.replace(filename.split('/')[-1],"")
    reader.SetDirectoryName(filename)
    reader.Update()

    return reader.GetOutput()

def read_vtk_image(reader, filename):
    reader.SetFileName(filename)
    reader.Update()

    im = reader.GetOutput()
    return im

def resample_image(vtk_im, min_=0.025):
    resample = vtk.vtkImageResample();
    spacing = vtk_im.GetSpacing()
    origin_ = vtk_im.GetOrigin()

    resample.SetInputData(vtk_im)
    for i in range(3):
        resample.SetAxisOutputSpacing(i,min_)
    resample.Update()
    o = resample.GetOutput()
    return resample.GetOutput()

def multi_replace(s,exprlist):

    for e in exprlist:
        s = s.replace(e,'')
    return s

def parsePathFile(fn):
    """
    parses a simvascular 2.0 path file
    """
    f = open(fn).readlines()

    paths={}

    expr1 = ['set ', 'gPathPoints', '(',')','{','}',',name','\n']
    expr2 = ['{','}','p ','t ', 'tx ', '(', '\\\n',' ']

    for i in range(len(f)):
        if ',name' in f[i]:
            s = f[i]
            s = multi_replace(s,expr1)

            s = s.split(' ')
            if not paths.has_key(s[0]):
                paths[s[0]] = {}
                paths[s[0]]['name'] = s[1]
            else:
                paths[s[0]]['name'] = s[1]

        if ',splinePts' in f[i]:
            j = i+1
            key = multi_replace(f[i],expr1).split(',')[0]
            if not paths.has_key(key):
                paths[key] = {}
                paths[key]['points'] = []
            else:
                paths[key]['points'] = []

            while 'tx' in f[j]:
                s = f[j]
                s = multi_replace(s,expr2).replace(')',',').split(',')[:-1]
                s = [float(x) for x in s]
                paths[key]['points'].append(s)

                j = j+1
            paths[key]['points'] = np.array(paths[key]['points'])

    return paths

def convert_path_dict(path_dict):
    points = []
    for p_id in path_dict.keys():
        p_name = path_dict[p_id]['name']
        p_points = path_dict[p_id]['points']
        for i in range(len(p_points)):
            v = p_points[i]
            d = {"name":p_name+"."+p_id, "point":i, "p":list(v[:3]),
                "n":list(v[3:6]),"x":list(v[6:])}
            points.append(d)
    return points

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

def smoothContour(c, num_modes=10):
    if len(c) < 3:
        return np.array([[0.0,0.0],[0.0,0.0]]).T
    x = c[:,0]
    y = c[:,1]
    mu = np.mean(c,axis=0)

    x = x-mu[0]
    y = y-mu[1]

    xfft = np.fft.fft(x)
    yfft = np.fft.fft(y)

    xfft[num_modes:] = 0
    yfft[num_modes:] = 0

    sx = 2*np.fft.ifft(xfft)+mu[0]
    sy = 2*np.fft.ifft(yfft)+mu[1]

    return np.array([np.real(sx),np.real(sy)]).T

def threshold(x,value):
	'''
	sets all values below value to 0 and above to 1

	args:
		@a x: the array to threshold
		@a value: the cutoff value
	'''
	inds = x < value
	y = np.copy(x)
	y[x < value] = 0
	y[x >= value] = 1
	return y

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
        return pds

def VTKPDPointstoNumpy(pd):
	'''
	function to convert the points data of a vtk polydata object to a numpy array

	args:
		@a pd: vtk.vtkPolyData object
	'''
	return numpy_support.vtk_to_numpy(pd.GetPoints().GetData())

def VTKSPtoNumpy(vol):
    '''
    Utility function to convert a VTK structured points (SP) object to a numpy array
    the exporting is done via the vtkImageExport object which copies the data
    from the supplied SP object into an empty pointer or array

    C/C++ can interpret a python string as a pointer/array

    This function was shamelessly copied from
    http://public.kitware.com/pipermail/vtkusers/2002-September/013412.html
    args:
    	@a vol: vtk.vtkStructuredPoints object
    '''
    exporter = vtkImageExport()
    exporter.SetInputData(vol)
    dims = exporter.GetDataDimensions()
    if np.sum(dims) == 0:
        return np.zeros((1,64,64))
    if (exporter.GetDataScalarType() == 3):
    	dtype = UnsignedInt8
    if (exporter.GetDataScalarType() == 4):
    	dtype = np.short
    if (exporter.GetDataScalarType() == 5):
    	dtype = np.int16
    if (exporter.GetDataScalarType() == 10):
    	dtype = np.float32
    if (exporter.GetDataScalarType() == 11):
    	dtype = np.float64
    a = np.zeros(reduce(np.multiply,dims),dtype)
    s = a.tostring()
    exporter.SetExportVoidPointer(s)
    exporter.Export()
    a = np.reshape(np.fromstring(s,dtype),(dims[2],dims[0],dims[1]))
    return a[0]

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

def getImageReslice(img, ext, p, n, x, spacing, asnumpy=False):
    """
    gets slice of an image in the plane defined by p, n and x

    args:
        @a img: vtk image (3 dimensional)
        @a ext: extent of the reslice plane [Xext,Yext]
        @a p ((x,y,z)): origin of the plane
        @a n ((x,y,z)): vector normal to plane
        @a x ((x,y,z)): x-axis in the plane

    returns:
        ret (itk image): image in the slice plane
    """
    reslice = vtk.vtkImageReslice()
    reslice.SetInputData(img)
    reslice.SetInterpolationModeToLinear()

    #Get y axis and make sure it satisfies the left hand rule
    tr = vtk.vtkTransform()
    tr.RotateWXYZ(-90,n)
    y = tr.TransformPoint(x)

    reslice.SetResliceAxesDirectionCosines(
        x[0],x[1],x[2],y[0],y[1],y[2],n[0],n[1],n[2])
    reslice.SetResliceAxesOrigin(p[0],p[1],p[2])

    px = spacing*ext[0]
    py = spacing*ext[1]

    reslice.SetOutputSpacing((spacing,spacing,spacing))
    reslice.SetOutputOrigin(-0.5*px,-0.5*py,0.0)
    reslice.SetOutputExtent(0,ext[0],0,ext[1],0,0)

    reslice.Update()
    if asnumpy:
         return VTKSPtoNumpy(reslice.GetOutput())
    else:
        return reslice.GetOutput()
