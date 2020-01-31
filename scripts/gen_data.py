#!/usr/bin/env python3
"""
    script to generate random uint8_t arrays
    at desired length
    (c) 2020 by Piotr Zapart
"""

import sys
import os
import getopt
import random as rnd
import argparse


example_text = '''--------------------------------------------------------------------------------
Example:

 generate an array in size of 8192 bytes, populated with random values
 and save it as array.h file
 
 python3 gen_data.py --rnd -l 8192 -o array.h
 
 generate am array of 512 zeros:
 
 python3 gen_data_py --val 0x00 -l 512 -o array_of_zeros.h
'''


def __uint8_t(x):
    x = int(x, 0)
    if x > 0xFF or x < 0:
        print("Value not in allowed range!")
        return None
    else:
        return x


def __gen_rand(start, end, num):
    res = []
    for j in range(num): 
        res.append(rnd.randint(start, end)) 
    return res 


def __gen_array(mode, length, value, filename):

    with open(filename, "w") as out_file:
        inc_name = os.path.basename(filename).split(".")[0]
        print("#ifndef __{name}_H_".format(name=inc_name.upper()), file=out_file)
        print("#define __{name}_H_".format(name=inc_name.upper()), file=out_file)
        print("\r\n#include \"sdcc_int.h\"\r\n", file=out_file)
        print("const uint8_t data[{len}] = {{".format(len=length), file=out_file)
        if mode == 'rnd':
            table = __gen_rand(0, 255, length)
        elif mode == 'lst':
            table = range(0, length+1)
        elif mode == 'val' and value:
            table = [value] * (length+1)
        for i in range(length):
            value = table[i] & 0xFF
            print("0x{v:02x}".format(v=value), file=out_file, end='')
            if i < length-1 :
                print(", ", file=out_file, end='')
            else:
                print("\r\n", file=out_file, end='')
            if (i % 10) == 9:
                print("\n", file=out_file, end='')
        print("};\n", file=out_file)
        print("#endif", file=out_file)
    print("Array of " + str(length) + " bytes created in file " + out_file.name)


def __main(argv):

    parser = argparse.ArgumentParser(description="const uint8_t array generator.",
                                     epilog=example_text,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--rnd', action='store_true', help="Generate random values")
    group.add_argument('--lst', action='store_true', help="Generate 0x00-0xFF increasing vealues")
    group.add_argument('--val', type=__uint8_t, help="Populate array with one value.")
    parser.add_argument('-l', '--length', default=0, required=True, type=int, help="Length of the array in bytes.")
    parser.add_argument('-o', '--out', required=True, type=str, help="Output file name.")
    args = parser.parse_args()

    if args.rnd:
        __gen_array('rnd', args.length, None, args.out)
    if args.lst:
        __gen_array('lst', args.length, None, args.out)
    if args.val is not None:
        __gen_array('val', args.length, args.val, args.out)


if __name__ == "__main__":
    __main(sys.argv[1:])

