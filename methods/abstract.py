class AbstractSegmenter(object):
    def __init__(self,args_dict, output_directory):
        self.args_dict        = args_dict
        self.output_directory = output_directory
    def run(sv_image, sv_path):
        raise RuntimeError("Abstract not implemented")
