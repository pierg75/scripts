#!/usr/bin/env python

import argparse

def clean_ascii(block):
    # Take only the ASCII letters and NL line feed 
    line = ''
    for i in block:
        if (ord(i) < 127 and ord(i) > 31) or ord(i) == 10:
            line += i
    return line

def main():

    parser = argparse.ArgumentParser(description='Print only ASCII caracters of a file')
    parser.add_argument('file', help='File to process')
    args = parser.parse_args()
    
    with open(args.file, 'rb') as f:
        block = f.read(2**9)
        while block != "":
            # Set the block size
            block = f.read(2**9)
            print("{0}").format(clean_ascii(block))


if __name__ == "__main__":
    main()

