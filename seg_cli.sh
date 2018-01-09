#!/bin/bash

# python seg_cli.py ./test/cabg11-image.mha ./test/cabg11_all.paths \
#   ./test/output/ identity .jpg --m ext 100 spacing 0.05 interval 5

python seg_cli.py ./test/cabg11-image.mha ./test/cabg11_all.paths \
   ./test/output/ threshold .jpg --m ext 100 spacing 0.05 interval 5 threshold 200
