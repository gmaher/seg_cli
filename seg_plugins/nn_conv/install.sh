#!/bin/bash

rm -rf dl_template

git clone https://github.com/gmaher/dl_template.git

cd dl_template

git checkout deeplofting

cp -rv ~/projects/dl_template/results .
