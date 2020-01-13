#point_edits_to_changed_product.py
import os
import sys
#import shutil

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__)) #to figure out where the program is being executed. This is home base
    os.chdir(dir_path)

    inputs = get_input() #[inpath,outpath,ed_type]
    inpath = inputs[0]
    outpath = inputs[1] #blah.csv
    ed_type = inputs[2] #a|c
    
    separate_uniqueID(inputs)
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

def separate_uniqueID(inputs): #takes in a line, reads the unique ID from the first column. in the outfile, it spreads that into its elements
    #set cursor to 0 in infile
    #set cursor to 0 in outfile
    for line in inputs[0]:
        #wite uniqueID to the ln in outfile
        #get the first term in the line
        strspl = #split the first term by "_"
        
        for item in strspl:
            #write item to a new spot on the line in outfile
            #go to next line in outfile
    
    #split by "_"


def get_input(): #input entered----> point_edits_to_changed_product.py [outpath] [a|c]
    outpath = "point_edits_products.csv"
    ed_type = "" # a or c
    
    if len(sys.argv)==1:
        return -1
    elif len(sys.argv)==4:
        inpath = sys.argv[1].strip()
        outpath = sys.argv[2].strip()
        ed_type = sys.argv[3].strip()
    else:
        print("No runline commands detected. Returning an error")
        return -1
    return [inpath,outpath,ed_type]