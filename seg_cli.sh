#!/bin/bash

python seg_cli.py ./test/output/small.txt ./test/output/out_1 seg_modules.reslice \
      --m ext 128 spacing 0.03 image ./test/cabg11-image.mha
