import os
import sys
import argparse

from modules.image import SVImage
from modules.path import SVPath
#from modules.segment import SVSeg

parser = argparse.ArgumentParser()
parser.add_argument('image')
parser.add_argument('paths')
parser.add_argument('output_directory')

args = parser.parse_args()

sv_image = SVImage(args.image)
sv_path  = SVPath(args.paths)
