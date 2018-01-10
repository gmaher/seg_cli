import sys
import os

#get location of current file
call_dir = os.getcwd()
file_dir = os.path.abspath(__file__)
file_name = file_dir.split('/')[-1]
file_dir = file_dir.replace(file_name,'')
os.chdir(file_dir)
print "Running from {}".format(file_dir)
from tqdm import tqdm
sys.path.append(os.path.abspath(file_dir+'dl_template'))
print sys.path
from modules import vascular_data, io
from experiments import I2INet

sys.path.append(os.path.abspath(file_dir+"../.."))

import numpy as np

from seg_methods.abstract import AbstractSegmenter
from seg_modules.util import save_output
def norm(x):
    x = (1.0*x-np.mean(x))/(np.std(x)+1e-5)
    x = x.reshape([1]+list(x.shape)+[1])
    return x

def build_window(center,window):
    print center, window
    def window_func(x):
        x = vascular_data.window_image(x,center,window)
        x = x.reshape([1]+list(x.shape)+[1])
        return x
    return window_func

class Segmenter(AbstractSegmenter):
    def run(self, sv_image, sv_path):
        os.chdir(file_dir+'dl_template')
        print os.getcwd()
        nn_type   = self.args_dict['nn_type']

        spacing   = float(self.args_dict['spacing'])

        threshold = float(self.args_dict['threshold'])

        global_config = io.load_yaml("./config/global.yaml")
        ext = global_config["CROP_DIMS"]
        if nn_type == "norm":
            config = io.load_yaml("./config/case1_perturb15.yaml")
            normalize = norm

        if nn_type == "window":
            config = io.load_yaml("./config/i2i_window.yaml")
            center = int(self.args_dict['center'])
            window = int(self.args_dict['window'])

            normalize = build_window(center, window)

        net = I2INet.Model(global_config, config)
        net.load()

        path_points = sv_path.get_path_points()
        for i in tqdm(range(len(path_points))):
            d = path_points[i]

            fn = d['name']

            p = d['p']
            n = d['n']
            x = d['x']

            im = sv_image.get_reslice(ext,p,n,x,spacing)

            im = normalize(im)

            out = net.predict(im)[0,:,:,0]
            out[out >= threshold] = 1
            out[out < threshold] = 0

            filename = self.output_directory+"{}{}".format(fn,self.output_file_type)
            filename = call_dir + filename[1:]
#            print filename
            save_output(out,filename)
