#generate_target.py
#Generates a list of target genes from a flybase output
def main():
    in_path = sysargv[1]
    out_path = sysargv[2]
    infile = open(in_path, "r")
    outfile = open(out_path, "x")
    for l0 in infile:
        l0s = l0.split(",")
        for item in l0s:
            if "Dsec" in item:
                outfile.write(l0s.split("\\")[1]+"\n")

if __name__ == "__main__":
    main()