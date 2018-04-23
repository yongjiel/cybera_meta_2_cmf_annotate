#!/usr/bin/pytion
import sys
import os

def get_args(program):
    if not len(sys.argv) in [3,4]:
        print >> sys.stderr, "Usage: python {0} <input_file> [-e|-p|-n] <[-d]>".format(program)
        sys.exit(1)
    input_file = sys.argv[1]
    category = sys.argv[2]
    if not category in ['-n', '-p', '-e']:
        print >> sys.stderr, "Usage: python {0} <input_file> [-e|-p|-n] <[-d]>".format(program)
        sys.exit(1)
    if len(sys.argv) == 4:
        der_arg = sys.argv[-1]
    else:
       der_arg = '' 
    if not os.path.isfile(input_file):
        print "Error: Input file not exist"
        sys.exit(1)
    return der_arg, input_file, category

def split_input_file(input_file, default_pieces):
    line_count = count(input_file);
    pieces = get_pieces(line_count, default_pieces)
    print "Pieces: {0}".format(pieces)
    split_into_pieces(input_file, pieces)
    return pieces

def count(input_file):
    count = 0
    with open(input_file, "r") as f:
        for i in f:
            count += 1
    return count

def get_pieces(line_count, default_pieces):
    if line_count / default_pieces > 0:
        pieces =  default_pieces
    else:
        pieces = line_count
    return pieces

def split_into_pieces(input_file, pieces):
    count = 0;
    for i in range(1, pieces+1):
        o_file = "{0}_{1}".format(input_file, i)
        if os.path.isfile(o_file):
            os.remove(o_file)
    with open(input_file, "r") as f:
        for line in f:
            count += 1
            file_suffix = count % pieces
            if file_suffix == 0:
                file_suffix = pieces
            o_file = "{0}_{1}".format(input_file, file_suffix)
            fo = open(o_file, 'a')
            fo.write(line)
            fo.close()
    print "Splitting files done!"
