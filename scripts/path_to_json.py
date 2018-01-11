import os
import argparse
import json
import numpy as np

def save_json(fn, data):
    with open(fn, 'w') as outfile:
        json.dump(data, outfile)

def convert_to_json_list(paths_file, output_directory,interval=1):
    if ".paths" in paths_file:
        d = parsePathFile(paths_file)
        d = convert_path_dict(d)
    else:
        raise RuntimeError("Unsupported paths_file type".format(paths_file))

    #files_file = output_directory+"/path_files.txt"
    #f = open(files_file,'w')
    dir_ = output_directory

    for i in range(0,len(d),interval):
        fn = os.path.abspath(dir_+'/{}.json'.format(i))
        save_json(fn, d[i])
    #    f.write(fn+"\n")
    #f.close()
    return files_file

def parsePathFile(fn):
    """
    parses a simvascular 2.0 path file
    """
    f = open(fn).readlines()

    paths={}

    expr1 = ['set ', 'gPathPoints', '(',')','{','}',',name','\n']
    expr2 = ['{','}','p ','t ', 'tx ', '(', '\\\n',' ']

    for i in range(len(f)):
        if ',name' in f[i]:
            s = f[i]
            s = multi_replace(s,expr1)

            s = s.split(' ')
            if not paths.has_key(s[0]):
                paths[s[0]] = {}
                paths[s[0]]['name'] = s[1]
            else:
                paths[s[0]]['name'] = s[1]

        if ',splinePts' in f[i]:
            j = i+1
            key = multi_replace(f[i],expr1).split(',')[0]
            if not paths.has_key(key):
                paths[key] = {}
                paths[key]['points'] = []
            else:
                paths[key]['points'] = []

            while 'tx' in f[j]:
                s = f[j]
                s = multi_replace(s,expr2).replace(')',',').split(',')[:-1]
                s = [float(x) for x in s]
                paths[key]['points'].append(s)

                j = j+1
            paths[key]['points'] = np.array(paths[key]['points'])

    return paths

def multi_replace(s,exprlist):

    for e in exprlist:
        s = s.replace(e,'')
    return s

def convert_path_dict(path_dict):
    points = []
    for p_id in path_dict.keys():
        p_name = path_dict[p_id]['name']
        p_points = path_dict[p_id]['points']
        for i in range(len(p_points)):
            v = p_points[i]
            d = {"name":p_name+"."+p_id+"."+str(i), "p":list(v[:3]),
                "n":list(v[3:6]),"x":list(v[6:]), "image":None}
            points.append(d)
    return points

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path_file")
    parser.add_argument('output_directory')
    parser.add_argument('-i', default=1, type=int, help="interval to sample paths at")
    args = parser.parse_args()
    print args
    path_file = os.path.abspath(args.path_file)
    convert_to_json_list(path_file,args.output_directory, args.i)
