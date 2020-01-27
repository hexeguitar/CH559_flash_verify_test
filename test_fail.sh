#! /bin/bash

# adjust the size so the resulting compiled bin file is 11312 or more bytes
size=6375

echo "Generating random byte array of size $size bytes"
python3 scripts/gen_data.py -l $size -o rndata.h
echo "Compiling test project ..."
./build.sh -f

