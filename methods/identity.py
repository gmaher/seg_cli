from abstract import AbstractSegmenter
class Segmenter(AbstractSegmenter):
    def run(sv_image, sv_path):
        for d in sv_path.path_points:
            fn = d['name']
