from abstract import AbstractSegmenter
class Segmenter(object):
    def run(sv_image, sv_path):
        for d in sv_path.path_points:
            fn = d['name']
            
