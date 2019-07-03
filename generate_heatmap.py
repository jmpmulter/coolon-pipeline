#generate_heatmap
import os
#import shutil
import sys

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__)) #to figure out where the program is being executed. This is home base
    os.chdir(dir_path)

    inputs = get_input() #[outpath,ed_type,p_cutoff,src_dir]
    outpath = inputs[0]
    ed_type = inputs[1]
    p_cutoffs = float(inputs[2]) #so that it can be compared against
    src_dir = inputs[3]
        
    all_paths = os.listdir()
    
    ed_type_ok = []
    path_filter(all_paths,ed_type_ok,ed_type)
    print("Number of files which passed ed_type filter:\t"+ str(len(ed_type_ok)))
    legend = generate_legend(ed_type_ok)
    header = gen_header(legend)
    genes = generate_keys(legend)
    gene_data = fill_dict(genes,legend,p_cutoffs)
    make_csv(header,gene_data,outpath)
    
    
    #take in ed_type,string sig filter cutoff, target folder (otherwise runs in its current folder)
    #makes a list of all the files in the directory with "A_to_I" or "C_to_U"
    #make a list of name_headers for the sheet
    #S -> in and significant
    #N -> in and and non-significant
    #O-> out

def get_input(): #input entered----> generate_heatmap.py [outpath] [a|c] [p_cutoff] [src_dir]
    outpath = "heatmap_01.csv"
    ed_type = "" # a or c
    p_cutoff = ".05"
    src_dir = ""
    if len(sys.argv)==1:
        return -1
    elif len(sys.argv)==3:
        outpath = sys.argv[1].strip()
        ed_type = sys.argv[2].strip()
        p_cutoff = ".05"
        src_dir = 0
    elif len(sys.argv)==4:
        outpath = sys.argv[1].strip()
        ed_type = sys.argv[2].strip()
        p_cutoff = sys.argv[3].strip()
        src_dir = 0
    elif len(sys.argv)==4:
        outpath = sys.argv[1].strip()
        ed_type = sys.argv[2].strip()
        p_cutoff = sys.argv[3].strip()
        src_dir = sys.argv[4] .strip()
        
    else:
        print("No runline commands detected. Returning an error")
        return -1
    return [outpath,ed_type,p_cutoff,src_dir]

def path_filter(all_paths,ed_type_ok,ed_type):
    key_phrase = ""
    if ed_type.lower().strip() == "a":
        key_phrase = "A_to_I"
    elif ed_type.lower().strip() == "c":
        key_phrase = "C_to_U"
    else:
        print("ed_type entered incorrectly") 
        return ["-1"]
    for path in all_paths: #filter so only the Filtered files are being considered
        if (key_phrase in path):
            print("Detected ed_type compliant file with path:\t"+path)
            ed_type_ok.append(path)
    ed_type_ok = sorted(ed_type_ok) #should make it more deterministic of the order
    
def generate_legend(ed_type_ok):
    legend = [[None]*len(ed_type_ok),[None]*len(ed_type_ok)]
    for i in range(0,len(ed_type_ok)):
        legend[0][i] = ed_type_ok[i]
        
        treatment_block = ed_type_ok[i].split("[")[1].split("]")[0].strip() #Expected: "CL,OA"
        #print(treatment_block)
        
        try:
            spl = treatment_block.split(",")
            crl = spl[0]
            trt = spl[1]
            legend[1][i] = "F"+str(i)+"_"+crl+"_vs_"+trt
        except(IndexError):
            legend[1][i] = "F"+str(i)+"_"+treatment_block
        
        #if (len(treatment_block)==2): #only applies for control only or dsechellia only trials
        #    legend[1][i] = "F"+str(i)+"_"+treatment_block
        #else:   
        #    spl = treatment_block.split(",")
        #    crl = spl[0]
        #    trt = spl[1]
        #    legend[1][i] = "F"+str(i)+"_"+crl+"_vs_"+trt
            
    return legend
        
def gen_header(legend):
    #print(legend)
    header = "Scaf_num_Pos_Fbgn_Gmnum"
    for i in range(0,len(legend[1])):
        header = header+","+legend[1][i]
    #print("Header")
    #print(header)
    return header

def generate_keys(legend):
    genes = {}
    for file in legend[0]:
        f_in = open(file,"r")
        group_position = get_group_column(f_in)
        f_in.seek(0)
        f_in.readline() #skips the now-processed header line
        for ln in f_in:
            #print(ln)
            identifier = ln.split(",")[group_position].strip()
            #print(identifier)
            if identifier in genes:
                continue
            else:
                genes[identifier] = [None]*len(legend[0])
        f_in.close()
    return genes
    
def fill_dict(genes,legend,p_cutoffs):
    ids = sorted(genes.keys())
    for id in ids:
        for i in range(0,len(legend[0])):
            file = legend[0][i]
            gene_found = False
            f_in = open(file,"r")
            p_column = get_p_column(f_in)
            f_in.seek(0) #possibly delete in the future
            f_in.readline() #possibly delete in the future
            
            for ln in f_in:
                if id in ln:
                    gene_found = True
                    p_val = ln.split(",")[p_column].strip()
                    if(float(p_val)<=p_cutoffs):
                        genes[id][i] = "S" #TODO confirm this line works, it may not
                    else:
                        genes[id][i] = "N" #TODO confirm this line works, it may not
            if(gene_found is False):
                genes[id][i] = "O"
    return genes
    
def get_p_column(f_in):
    f_in.seek(0)
    pval_column = -1
    in_header = f_in.readline().strip().split(",")
    for i in range(0,len(in_header)):
        if "p.value" in in_header[i]:
            pval_column = i
            break
        else:
            continue
    f_in.seek(0)
    return pval_column

def get_group_column(f_in):
    f_in.seek(0)
    group_column = -1
    in_header = f_in.readline().strip().split(",")
    for i in range(0,len(in_header)):
        if "group" in in_header[i]:
            group_column = i
            break
        else:
            continue 
    return group_column

def make_csv(header, gene_data, outpath):
    print("Generating output file with path\t"+outpath)
    gene_keys = sorted(gene_data.keys())
    f_out = open(outpath,"w")
    f_out.write(header+"\n")
    for key in gene_keys:
        f_out.write(key.strip())
        for i in range(0,len(gene_data[key])):#confirm no -1 error
            #print(gene_data[key])
            f_out.write(","+gene_data[key][i])
        f_out.write("\n")
    f_out.close()
    print("File\t"+outpath+"\t sucessfully generated. Goodbye.")

if __name__=="__main__":
    main()
