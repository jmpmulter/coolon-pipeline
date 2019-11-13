#point_edits_to_changed_product.py
import os
import sys
#import shutil

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__)) #to figure out where the program is being executed. This is home base
    os.chdir(dir_path)

    inputs = get_input() #[outpath,ed_type,p_cutoff,src_dir]
    outpath = inputs[0] #blah.csv
    ed_type = inputs[1] #a|c
    
    
    #pseudo code:
    #Get input
    #translate the specific gene locus notation from the xlsx files into a scaffold and position and gmnum for each line
    
        #incoming formats
            #scaffold_0_20105182_FBgn0178391_GM23525
            #scaffold_3754_342_FBgn0255867_18SrRNA:GM27734
    
    #use the GMNUM to look up the gene coordinates of the whole gene in the gff3
        #skipping lines that begin with #
        #use the filt_GFF3 from the pipeline (from any run of it)
        #Make sure to consider strand! Need the reverse transcript of the strand if -.
    #Use coordinates to pull that section of the genome from FASTA

    
    #COPY/PASTED Code below this; ignore.
    #all_paths = os.listdir()
    
    #ed_type_ok = []
    #path_filter(all_paths,ed_type_ok,ed_type)
    #print("Number of files which passed ed_type filter:\t"+ str(len(ed_type_ok)))
    #legend = generate_legend(ed_type_ok)
    #header = gen_header(legend)
    #genes = generate_keys(legend)
    #gene_data = fill_dict(genes,legend,p_cutoffs)
    #make_csv(header,gene_data,outpath)
    
    
    #take in ed_type,string sig filter cutoff, target folder (otherwise runs in its current folder)
    #makes a list of all the files in the directory with "A_to_I" or "C_to_U"
    #make a list of name_headers for the sheet
    #S -> in and significant
    #N -> in and and non-significant
    #O-> out

def get_input(): #input entered----> point_edits_to_changed_product.py [outpath] [a|c]
    outpath = "point_edits_products.csv"
    ed_type = "" # a or c
    
    if len(sys.argv)==1:
        return -1
    elif len(sys.argv)==3:
        outpath = sys.argv[1].strip()
        ed_type = sys.argv[2].strip()
    else:
        print("No runline commands detected. Returning an error")
        return -1
    return [outpath,ed_type]