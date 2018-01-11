import sys
import os
sys.path.append(os.path.abspath('..'))
from abstract import AbstractSegmenter
from util import save_output, threshold

class Segmenter(AbstractSegmenter):
    def process_arguments(self,args_dict):
        self.threshold = float(self.args_dict['threshold'])

    def setup(self, env_info, meta_data_list):
        pass

    def process_image(self, image, meta_data):
        image[image > self.threshold]  = 1
        image[image <= self.threshold] = 0
        return image
