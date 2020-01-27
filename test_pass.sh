#! /bin/bash

size=6297

echo "Generating random byte array of size $size bytes"
python3 scripts/gen_data.py -l $size -o rndata.h
echo "Compiling test project ..."
./build.sh -f

