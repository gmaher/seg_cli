from util import parsePathFile, convert_path_dict
class SVPath(object):
    def __init__(self,filename):
        self.filename = filename

        self.path_points = self.load(self.filename)

    def load(self,filename):
        if ".paths" in filename:
            d = parsePathFile(filename)
            return convert_path_dict(d)
        else:
            raise RuntimeError("Unsupported file type {}".format(filename))
