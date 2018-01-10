from util import save_output, save_json, load_input_image, mkdir
import numpy as np

class AbstractSegmenter(object):
    def __init__(self, args_dict, output_directory, output_file_type):
        self.args_dict        = args_dict
        if output_directory[-1] == "/"
            self.output_directory = output_directory
        else:
            self.output_directory = output_directory+'/'

        self.output_file_directory = self.output_directory+'output/'
        mkdir(self.output_file_directory)

    def run(self, path_points):
        f = open(self.output_directory+'output_files.txt','w')

        for d in path_points:

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

            filename = self.store_output(output, d, self.output_file_directory)

            f.write(filename+'\n')

        f.close()

    def process_arguments(self,args_dict):
        raise RuntimeError("Abstract not implemented yet")

    def setup(self, env_info, meta_data_list):
        raise RuntimeError("Abstract not implemented yet")

    def process_image(self, image, meta_data):
        raise RuntimeError("Abstract not implemented yet")

    def store_output(self, output, meta_data, output_file_directory):
        if not d.has_key('name'):
            raise RuntimeError("meta_data must specify a name string but didn't"\
                .format(d))

        name = d['name']
        meta_filename = output_file_directory+name+".json"
        d['image'] = output.tolist()
        save_json(meta_filename, d)
        return meta_filename
