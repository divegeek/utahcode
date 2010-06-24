#!/usr/bin/env python

"""
A trivial utility to wrap text files.
"""

import sys
import textwrap

wrapper = textwrap.TextWrapper(width=78)
def wrap_file_contents(in_file, out_file):
    
    for line in in_file:
        out_file.write(line+'\n')

def wrap_file(in_path, out_path):
    in_file  = open(in_path, "rt")
    out_file = open(out_path, "wt+")
    wrap_file_contents(in_file, out_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: wrap_text <in_path> <out_path>"
    
    wrap_file(sys.argv[1], sys.argv[2])
