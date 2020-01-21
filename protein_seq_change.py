#protein_seq_change.py
#takes the specific edits and their associated FBGN numbers.
# gets genomic sequence from FASTAs for before/after edits
#translates sequence and returns edited and unedited translates.

import sys
import os
import bio



#take the specific edit position, and the FBGN/GMNUM from unique Identifier
#use GMNUM/FBGN to get start/end of the genomic sequence
#find if the gene goes forward or backward
#find start and end points in FASTA, and edit point within this range
#If backward, do next steps with reverse complement
#store Unedited and edited transcript
#translate the transcripts

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__)) #to figure out where the program is being executed. This is home base
    os.chdir(dir_path)
    outpath = ""
    try:
        inpath= sys.argv[1]
    except IndexError:
        inpath = input("Input file name not entered in command line. Enter name of Input file")
    try:
        outpath= sys.argv[2]
    except IndexError:
        outpath = input("Output file name not entered in command line. Enter name of output file")
    try:
        ed_type= sys.argv[3]
    except IndexError:
        ed_type = input("ed_type not entered in command line. Enter ed_type")
        
        
    if ((inpath=="")or(outpath == "")or(ed_type=="")):
        print("inpath or outpath or ed_type not entered. Aborting program")
        sys.exit()
    SCAN_list = assemble_SCAN_list(ed_type)
    
    process_data(inpath,outpath,ed_type)#TODO fill in with correct commands

def process_data(inpath, outpath,ed_type):
    in_file = open(inpath,"r")
    in_file.seek(0)
    out_file = open(outpath,"w")
    out_header= "uniqueID,SCAF,POS,START,END,SENSE,unedited_DNA,edited_DNA,unedited_RNA,edited_RNA,unedited_protein,edited_protein,unedited_AA,edited_AA,Coding_AA"
    out_file.write(out_header+"\n")
    for line in in_file:
        scaf_pos_FBGN_GMNUM = parse_unique_ID(line)#Get unique ID [scaf,pos]
        if(scaf_pos_FBGN_GMNUM==[]):
            continue
        
    
def parse_unique_ID(line):
    #takes in a string of the line, returns an array with the unique ID elements
    #Returns [scaf,pos,FBGN,GMNUM]
    #TODO: Potential problem that this erases some datalines when two edits occur at the same point. this was an issue in the past requiring several fixes.
    #As long as the quantities can be duplicated in the output file, the above should not pose a serious problem.
    #raw_id format scaffold_0_1004752_FBgn0179780_GM24918
    #raw_spl = [scaffold,0,1004752,FBgn0179780,GM24918]
    raw_id = line.split(",")[0]
    raw_spl = raw_id.split("_")
    return raw_spl[1:]
    

def get_gene_details(FBGN_GMNUM):
    #Extracts start point, endpoint, and sense using the FBGN or GMNUM
    #Returns start,end,FBGN
    return False #TODO edit this
    
def assemble_SCAN_list(ed_type):
    all_paths = os.listdir()
    SCAN_list = []
    for path in all_paths: #filter so only the Filtered files are being considered
        #ETODO DIT STARTING HERE and BELOW
        if ("PXL" in path): #TODO Confirm this edit worked TODO edit this to only look at the PXL and other relevant files
            print("Detected PXL file with path:\t"+path)
            if (ed_type=="a"):
                if("A_to_I" in path):
                    SCAN_list.append(path)
                    print("Added file to SCAN_list because ed_type matches mode: a")
                else:
                    print("Ignored file because ed_type does not match mode: a")
            if (ed_type=="c"):
                if("C_to_U" in path):
                    SCAN_list.append(path)
                    print("Added file to SCAN_list because ed_type matches mode: c")
                else:
                    print("Ignored file because ed_type does not match mode: c")  
    return SCAN_list



if __name__ == "__main__": #sets up a main area. This will not work well if imported
    main()
    
