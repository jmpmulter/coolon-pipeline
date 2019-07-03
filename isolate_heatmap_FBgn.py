#Isolate_heatmap_FBgn
#Load in Heatmap
#Isolate FBGNs, GM_num, place at end of line,
#format header to be ready for excel heatmaps
import sys
import os
def main():
    inpath = ""
    outpath = ""
    inpath = sys.argv[1]
    outpath = sys.argv[2]
    
    #print(sys.argv)
    
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
                id_split = item.split("_")
                break
        try:
            for i in range(0,len(id_split)):
                if "FBgn" in id_split[i]:
                    FBgn = id_split[i]
                    gm_num = id_split[i+1].split("\"")[0]
                    break
            f_out.write(ln.strip()+",,,,,,"+FBgn+","+gm_num+"\n")
        except(IndexError):
            print("Error: GM_num format is likely non-standard. skipping this line")
            f_out.write(ln+",,,,,,,\n")
            #skip to the next line in f_in #this should happen automatically

    f_in.close()
    f_out.close()
    
    
if __name__ == "__main__":
    #print("running program")
    main()