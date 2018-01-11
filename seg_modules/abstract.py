from util import save_output, save_json, mkdir
import numpy as np
from tqdm import tqdm

class AbstractSegmenter(object):
    def __init__(self, args_dict, output_directory):
        self.args_dict        = args_dict
        if output_directory[-1] == "/":
            self.output_directory = output_directory
        else:
            self.output_directory = output_directory+'/'

    def run(self, path_points):

        for d in tqdm(path_points):

            #either d has the image or references it
            if d.has_key("image"):
                #check if algorithm wants to skip image (e.g. for extracting from
                #larger image)
                if d['image'] == None:
                    image = []
                else:
                    image = np.array(d['image'])
            else:
                raise RuntimeError("image data missing image key {}".format(d))

            #output is a numpy array
            output = self.process_image(image, d)

            filename = self.store_output(output, d, self.output_directory)


    def process_arguments(self,args_dict):
        raise RuntimeError("Abstract not implemented yet")

    def setup(self, env_info, meta_data_list):
        raise RuntimeError("Abstract not implemented yet")

    def process_image(self, image, meta_data):
        raise RuntimeError("Abstract not implemented yet")

    def store_output(self, output, meta_data, output_directory):
        if not meta_data.has_key('name'):
            raise RuntimeError("meta_data must specify a name string but didn't"\
                .format(d))

        name = meta_data['name']
        meta_filename = output_directory+name+".json"
        meta_data['image'] = output.tolist()
        save_json(meta_filename, meta_data)
        return meta_filename
