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
    print("python3 gen_data.py -l <length in bytes> -o <filename.h>")

def gen_rand(start, end, num): 
    res = [] 
  
    for j in range(num): 
        res.append(rnd.randint(start, end)) 
    return res 


def main(argv):
    output_file = ''
    length = 0
    try:
        opts, args = getopt.getopt(argv, "hl:o:")
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
        else:
            assert False, "unhandled option"
    
    with open(output_file, "w") as out_file:
        inc_name = os.path.basename(output_file).split(".")[0]
        print("#ifndef __{name}_H_".format(name=inc_name.upper()), file=out_file)
        print("#define __{name}_H_".format(name=inc_name.upper()), file=out_file)
        print("#include \"sdcc_int.h\"", file=out_file)
        print("const uint8_t data[{len}] = {{".format(len=length), file=out_file)
        table = gen_rand(0, 255, length)
        for i in range(length):
            value = table[i]
            print("{v:3}".format(v=value), file=out_file, end='')
            if i < length:
                print(", ", file=out_file, end='')
            if (i % 10) == 9:
                print("\n", file=out_file, end='')
        print("};\n", file=out_file)            
        print("#endif", file=out_file)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print('Error: too few arguments!')
        sys.exit(2)
    else:
        main(sys.argv[1:])

