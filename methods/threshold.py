import sys
import os
sys.path.append(os.path.abspath('..'))
from abstract import AbstractSegmenter
from modules.util import save_output, threshold
import numpy as np
class Segmenter(AbstractSegmenter):
    def run(self, sv_image, sv_path):

        ext     = int(self.args_dict['ext'])
        spacing = float(self.args_dict['spacing'])
        interval = int(self.args_dict['interval'])
        threshold_value = float(self.args_dict['threshold'])

        for i in  range(0,len(sv_path.path_points), interval):
            d = sv_path.path_points[i]
            fn = d['name']

            p = d['p']
            n = d['n']
            x = d['x']

            im = sv_image.get_reslice(ext,p,n,x,spacing)
            im = threshold(im, threshold_value)

            filename = self.output_directory+"{}{}".format(fn,self.output_file_type)
            print filename
            save_output(im,filename)
