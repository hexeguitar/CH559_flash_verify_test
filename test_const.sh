#! /bin/bash

# adjust the size so the resulting compiled bin file is 11312 or more bytes
size=24000


if [ -z "$1" ]; then
    echo "Please provide an 8bit value for the test_array"
    exit 1
fi
if (( "$1" < 0 || "$1" > 255 )); then
    echo "Value not in 0-255 range!"
    exit 1
fi

echo "Generating byte array of size $size bytes populated with $1"
python3 scripts/gen_data.py -v "$1" -l $size -o test_array.h
echo "Compiling test project ..."
./build.sh -f usb.log




