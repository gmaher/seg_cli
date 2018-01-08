from util import load_mha, load_vti, load_dcm, getImageReslice
class SVImage(object):
    def __init__(self,filename):
        self.filename = filename

        self.vtk_image = self.load_image(filename)
        self.spacing = self.vtk_image.GetSpacing()
        self.dimensions = self.vtk_image.GetExtent()[1::2]

    def load_image(self,filename):
        if ".dcm" in filename:
            return load_dcm(filename)
        elif ".vti" in filename:
            return load_vti(filename)
        elif ".mha" in filename:
            return load_mha(filename)
        else:
            raise RuntimeError("Unsupported image type {}".format(filename))

    def get_reslice(p,n,x,spacing):
        """
        p: 3d point in space
        n: normal vector to the reslice
        x: x-axis vector of the reslice
        """
        return getImageReslice(self.vtk_image, p, n, x, spacing, asnumpy=True)
