from abstract import AbstractSegmenter
from image import SVImage

class Segmenter(AbstractSegmenter):
    def process_arguments(self,args_dict):
        self.image    = args_dict['image']
        self.sv_image = SVImage(self.image)
        self.spacing  = float(args_dict['spacing'])
        self.ext      = int(args_dict['ext'])
    def setup(self,env_info, meta_data_list):
        pass

    def process_image(self, image, meta_data):
        p = meta_data['p']
        n = meta_data['n']
        x = meta_data['x']

        return self.sv_image.get_reslice(self.ext, p, n, x, self.spacing)
