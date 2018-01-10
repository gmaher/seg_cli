#!/bin/bash

# python seg_cli.py ./test/cabg11-image.mha ./test/cabg11_all.paths \
#   ./test/output/ methods.identity .jpg --m ext 100 spacing 0.05 interval 5

# python seg_cli.py ./test/cabg11-image.mha ./test/cabg11_all.paths \
#    ./test/output/ methods.threshold .jpg --m ext 100 spacing 0.05 interval 5 threshold 200

# python seg_cli.py ./test/cabg11-image.mha ./test/cabg11_all.paths \
#       ./test/output/ seg_plugins.nn_conv .jpg \
#       --m spacing 0.03 nn_type norm threshold 0.1

python seg_cli.py ./test/cabg11-image.mha ./test/cabg11_all.paths \
      ./test/output/ seg_plugins.nn_conv .jpg \
      --m spacing 0.03 nn_type window threshold 0.1 center 200 window 500
