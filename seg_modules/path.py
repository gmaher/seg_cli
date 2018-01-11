from util import parsePathFile, convert_path_dict, load_json
class SVPath(object):
    def __init__(self,jsons):
        self.jsons = jsons
        self.path_points = [self.load(f) for f in self.jsons]

    def load(self,filename):
        if ".json" in filename:
            return load_json(filename)
        else:
            raise RuntimeError("Unsupported file type {}".format(filename))

    def get_path_points(self):
        return self.path_points[:]
