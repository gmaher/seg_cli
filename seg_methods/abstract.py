class AbstractSegmenter(object):
    def __init__(self,args_dict, output_directory, output_file_type):
        self.args_dict        = args_dict
        self.output_directory = output_directory
        self.output_file_type = output_file_type
    def run(sv_image, sv_path):
        raise RuntimeError("Abstract not implemented")
