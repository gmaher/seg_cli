import os
import sys
import importlib
import argparse

from seg_modules.util import args_to_dict, convert_to_json_list
from seg_modules.image import SVImage
from seg_modules.path import SVPath
#from modules.segment import SVSeg

parser = argparse.ArgumentParser()
parser.add_argument('image')
parser.add_argument('paths')
parser.add_argument('output_directory')
parser.add_argument('method')
parser.add_argument('output_file_type')
parser.add_argument('--m',nargs="*")
args = parser.parse_args()

#TODO: Split into two scripts, one that processes paths file/directory
# other just assumes list of jsons passed

#TODO: Slice (2D and 3D) and Oblique mode

#TODO: Segmenters can output numpy arrays and use standard storage,
#otherwise they must implement their own

#TODO: Essentially need image class with extraction methods, wrapper for vtk

#TODO: vtkExtractVOI to extract 2d/3d slices

print args.m
if args.m == None:
    args.m = {}
elif len(args.m) == 1:
    #config file
    args.m = {"config_file":args.m[0]}
else:
    if not len(args.m)%2 == 0:
        raise RuntimeError("Uneven number of --m arguments provided: {}".format(args.m))
    args.m = args_to_dict(args.m)

sv_image = SVImage(args.image)

if not ".txt" in args.paths:
    args.paths = convert_to_json_list(args.paths, args.output_directory)

sv_path  = SVPath(args.paths)

#Get method
method = args.method
print "Using method {}".format(method)
Segmenter_class = importlib.import_module(method).Segmenter
segmenter = Segmenter_class(args.m,args.output_directory,args.output_file_type)
segmenter.run(sv_image, sv_path)
