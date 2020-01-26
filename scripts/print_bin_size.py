#!/usr/bin/env python3
import sys
import os
import getopt

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "i:")
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for opt, arg in opts:
        if opt in '-i':
            input_file = arg
        else:
            assert False, "unhandled option"

        size = os.path.getsize(input_file)
        print("--------------------------------------------")
        print("Output file size = "+str(size)+" bytes")
        print("--------------------------------------------")

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print('Error: too few arguments!')
        sys.exit(2)
    else:
        main(sys.argv[1:])

