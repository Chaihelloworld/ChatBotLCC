#!/bin/bash

for py_file in $(find ./src -name *.py)
do
    python $py_file
done