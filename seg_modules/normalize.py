from abstract import AbstractSegmenter
import numpy as np

def window_image(image,center,window):
    start_ = center-float(window)/2
    end_   = center+float(window)/2
    x = image.copy()

    x = (1.0*x)/window + (0.5-float(center)/window)
    x[image <= start_] = 0.0
    x[image > end_] = 1.0
    return x

class Segmenter(AbstractSegmenter):
    def process_arguments(self,args_dict):
        self.type = args_dict['type']

    def setup(self,env_info, meta_data_list):
        pass

    def process_image(self, image, meta_data):
        if self.type == "normal":
            image = (1.0*image - np.mean(image))/(np.std(image)+1e-5)
        elif self.type == "max":
            image = (1.0*image - np.amin(image))/(np.amax(image)-np.amin(image))
        elif self.type == "window":
            center = self.args_dict['center']
            window = self.args_dict['window']
            image  = window_image(image,center,window)
        else:
            raise RuntimeError("Unsupported normalization type {}".format(self.type))

        return image
