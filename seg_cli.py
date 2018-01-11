import os
import sys
import importlib
import argparse

from seg_modules.util import args_to_dict, convert_to_json_list
from seg_modules.image import SVImage
from seg_modules.path import SVPath
#from modules.segment import SVSeg

parser = argparse.ArgumentParser()
parser.add_argument('jsons', nargs="+", help="json files to run on")
parser.add_argument('-o', default=".", help="output directory")
parser.add_argument('-a', help="algorithm to use")
parser.add_argument('--m',nargs="*", help="algorithm arguments")
args = parser.parse_args()

args.o = os.path.abspath(args.o)

#TODO: vtkExtractVOI to extract 2d/3d slices

#TODO: plugin framework? http://martyalchin.com/2008/jan/10/simple-plugin-framework/
print args.m
if args.m == None:
    args.m = {}

else:
    if not len(args.m)%2 == 0:
        raise RuntimeError("Uneven number of --m arguments provided: {}".format(args.m))
    args.m = args_to_dict(args.m)

# if not ".txt" in args.points_list:
#     raise RuntimeError("must supply a .txt file with point files in it as paths argument")

sv_path  = SVPath(args.jsons)

#Get method
method = args.a
print "Using method {}".format(method)
Segmenter_class = importlib.import_module(method).Segmenter
segmenter = Segmenter_class(args.m,args.o)

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
