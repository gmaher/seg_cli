import os
import sys
import importlib
import argparse

from seg_modules.util import args_to_dict, convert_to_json_list
from seg_modules.image import SVImage
from seg_modules.path import SVPath
#from modules.segment import SVSeg

parser = argparse.ArgumentParser()
parser.add_argument('points_list')
parser.add_argument('output_directory')
parser.add_argument('method')
parser.add_argument('--m',nargs="*")
args = parser.parse_args()

args.output_directory = os.path.abspath(args.output_directory)

#TODO: vtkExtractVOI to extract 2d/3d slices

print args.m
if args.m == None:
    args.m = {}

else:
    if not len(args.m)%2 == 0:
        raise RuntimeError("Uneven number of --m arguments provided: {}".format(args.m))
    args.m = args_to_dict(args.m)

if not ".txt" in args.points_list:
    raise RuntimeError("must supply a .txt file with point files in it as paths argument")

sv_path  = SVPath(args.points_list)

#Get method
method = args.method
print "Using method {}".format(method)
Segmenter_class = importlib.import_module(method).Segmenter
segmenter = Segmenter_class(args.m,args.output_directory)

#get environment info
env_info = {}
env_info['calling_directory'] = os.getcwd()

this_file_path = __file__
this_file_name = this_file_path.split('/')[-1]
this_file_dir  = this_file_path.replace(this_file_name,'')
env_info['seg_cli_directory'] = this_file_dir

segmenter.process_arguments(args.m)

segmenter.setup(env_info, sv_path.get_path_points())

segmenter.run(sv_path.get_path_points())
