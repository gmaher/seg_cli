from util import parsePathFile, convert_path_dict, load_json
class SVPath(object):
    def __init__(self,filename):
        self.filename = filename

        self.path_files = open(self.filename,'r').readlines()
        self.path_files = [f.replace('\n','') for f in self.path_files]

        self.path_points = [self.load(f) for f in self.path_files]

    def load(self,filename):
        if ".json" in filename:
            return load_json(filename)
        else:
            raise RuntimeError("Unsupported file type {}".format(filename))
