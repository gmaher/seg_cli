import argparse
from scipy.misc import imsave
import os
import json
import numpy as np

def load_json(fn):
    with open(fn) as f:
        return json.load(f)

parser = argparse.ArgumentParser()
parser.add_argument('input_folder')
parser.add_argument('output_folder')

args = parser.parse_args()

input_folder  = os.path.abspath(args.input_folder)
output_folder = os.path.abspath(args.output_folder)

for f in os.listdir(input_folder):
    inf = input_folder+"/"+f
    d   = load_json(inf)
    im  = np.array(d['image'])

    output_file = output_folder+"/"+d['name']+'.jpg'
    imsave(output_file,im)
