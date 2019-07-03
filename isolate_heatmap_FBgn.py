#Isolate_heatmap_FBgn

#Load in Heatmap
#Isolate FBGNs, place at end of line
def main():
    inpath = ""
    outpath = ""
    inpath = sys.argv[1]
    outpath = sys.argv[2]
    
    if ((inpath=="")or(outpath == "")):
        print("inpath or outpath not entered. Aborting program")
        sys.exit()
    f_in = open(inpath,"r")
    f_out = open(outpath,"w")
    
    f_in.seek(0)
    header = f_in.readline().strip()
    header+=",Sig Hitts,Non-Sig Hits,Total Hits,Total Omits,Dmel Ortholog,FBgn_num,GM_num\n"
    f_out.write(header)
    gm_num = ""
    FBgn = ""
    id_split = ""
    for ln in f_in:
        lns = ln.split(",")
        for item in lns:
            if "FBgn" in item:
                id_split = id.split("_")
                break
        try:
            for i in range(0,len(id_split)):
                if "FBgn" in id_split[i]:
                    FBgn = id_split[i]
                    gm_num = id_split[i+1]
                    break
            f_out.write(ln+",,,,,,"+FBgn+","+gm_num+"\n")
        except(IndexError):
            print("Error: GM_num format is likely non-standard. skipping this line")
            f_out.write(ln+",,,,,,,\n")
            #skip to the next line in f_in #this should happen automatically

    f_in.close()
    f_out.close()
    
    
if __name__ == "main":
    main()