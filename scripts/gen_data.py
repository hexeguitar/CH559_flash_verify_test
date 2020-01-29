#!/usr/bin/env python3
'''
    script to generate random uint8_t arrays
    at desired length
    (c) 2020 by Piotr Zapart

'''

import sys
import os
import getopt
import random as rnd

def usage():
    print("-------------------------------------------------------------------")
    print("8 bit array generator for testing purposes, creates a C header file\r\n")
    print("python3 gen_data.py <method> -l <length in bytes> -o <filename.h>\r\n")
    print("Parameters:")
    print("\tmethod:")
    print("\t\t--rnd\t- populates the array with random 8bit values")
    print("\t\t--lst\t- populates the array with increasing 8bit values")
    print("\t-v\t-populates the array with the provided 8bit values") 
    print("\t-l\t-length of the array, 0 to 0xFFFF range")
    print("\t-o\t- output file name\r\n")
    print("Example: generate an array in size of 8192 bytes, populated with random values")
    print("and save it as array.h file")
    print("python3 gen_data.py --rnd -l 8192 -o array.h")
    print("-------------------------------------------------------------------")

def gen_rand(start, end, num): 
    res = [] 
  
    for j in range(num): 
        res.append(rnd.randint(start, end)) 
    return res 


def main(argv):
    output_file = ''
    length = 0
    mode = 'lst'
    value = 0
    try:
        opts, args = getopt.getopt(argv, "hl:o:v:", ["rnd", "lst"] )
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for opt, arg in opts:
        if opt in '-o':
            output_file = str(arg)
        elif opt in '-l':
            length = int(arg)
        elif opt in '-h':
            usage()
            sys.exit(0)
        elif opt in  '--lst':
            mode = 'lst'
        elif opt in '--rnd':
            mode = 'rnd'
        elif opt in '-v':
            mode = 'val'
            value = int(arg)
        else:
            assert False, "unhandled option"
    
    with open(output_file, "w") as out_file:
        inc_name = os.path.basename(output_file).split(".")[0]
        print("#ifndef __{name}_H_".format(name=inc_name.upper()), file=out_file)
        print("#define __{name}_H_".format(name=inc_name.upper()), file=out_file)
        print("#include \"sdcc_int.h\"", file=out_file)
        print("const uint8_t data[{len}] = {{".format(len=length), file=out_file)
        if mode == 'rnd':
            table = gen_rand(0, 255, length)
        elif mode == 'lst':
            table = range(0, length+1)
        elif mode == 'val':
            table = [value] * (length+1)
        for i in range(length):
            value = table[i] & 0xFF
            print("{v:3}".format(v=value), file=out_file, end='')
            if i < length:
                print(", ", file=out_file, end='')
            if (i % 10) == 9:
                print("\n", file=out_file, end='')
        print("};\n", file=out_file)            
        print("#endif", file=out_file)
    print("Array of " + str(length) + " bytes created in file " + out_file.name)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print('Error: too few arguments!')
        sys.exit(2)
    else:
        main(sys.argv[1:])

