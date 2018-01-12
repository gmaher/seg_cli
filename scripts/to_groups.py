import argparse
import json
import numpy as np
from tqdm import tqdm

def save_json(fn, data):
    with open(fn, 'w') as outfile:
        json.dump(data, outfile)

def load_json(fn):
    with open(fn) as f:
        return json.load(f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_files', nargs="+")
    parser.add_argument('output_directory')
    args = parser.parse_args()

    paths = [f.split('/')[-1] for f in args.input_files]
    paths = list(set([p.split('.')[0]+'.'+p.split('.')[1] for p in paths]))

    for path in paths:
        f = open(args.output_directory+'/'+path,'w')

        path_files = [i for i in args.input_files if path+'.' in i]
        path_files = sorted(path_files, key = lambda x: int(x.split('.')[-2]))
        print path_files

        for p in path_files:
            path_number = p.split('.')[-2]
            path_name   = p.split('/')[-1].split('.')[0]
            d = load_json(p)
            c = d['contour_3d']

            f.write('/group/{}/{}\n'.format(path_name, path_number))
            f.write('{}\n'.format(path_number))

            for point in c:
                f.write("{} {} {}\n".format(point[0], point[1], point[2]))
            f.write('\n')

        f.close()
