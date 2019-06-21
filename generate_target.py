#generate_target.py
#Generates a list of target genes from a flybase output
import os
import sys

def main():
    in_path = sys.argv[1]
    out_path = sys.argv[2]
    infile = open(in_path, "r")
    outfile = open(out_path, "x")
    for l0 in infile:
        l0s = l0.split(",")
        for item in l0s:
            if "Dsec" in item:
                outfile.write(item.split("\\")[1]+"\n")

if __name__ == "__main__":
    main()