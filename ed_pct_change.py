#ed_pct_change.py
#This program needs to isolate the unique Identifiers, then find percent editing in CL, find pct editing in other conditions, show change in percent editing.
#Things to consider: There will be some where the edit does not pop up
#I'm using the PXL's as sources of info because their formatting will make this easier, at least i think
#Current plan is to construct a CSV of all the info. Then to tack that info on to the original spreadsheet.

#A second script will merge the info

import sys
import os
import math
from statistics import mean 
import copy
from decimal import *

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
    
    compile_stats(SCAN_list,inpath, outpath, ed_type)
    
    
def compile_stats(SCAN_list,inpath, outpath, ed_type):
    in_file = open(inpath,"r")
    in_file.seek(0)
    out_file = open(outpath,"w")
    
    
    out_header= "uniqueID, CL_delta, FIG_delta, HA_delta, LDOPA_delta, NONI_delta, OAHA_delta, OA_delta, CL_avg, FIG_avg, HA_avg, LDOPA_avg, NONI_avg, OAHA_avg, OA_avg"
    out_file.write(out_header+"\n")
    
    #out_header format: "uniqueID, CL_delta, FIG_delta, HA_delta, LDOPA_delta, NONI_delta, OAHA_delta, OA_delta, CL_avg, FIG_avg, HA_avg, LDOPA_avg, NONI_avg, OAHA_avg, OA_avg"
    #header puts most relevant information up front, but more detailed work a bit futher back
    
    #Vars:
    type_avg = [-1,-1,-1,-1,-1,-1,-1] #An array to hold the average of each type's values
    #NB: Tpye avg should use ordering CL, F0_CL_vs_FIG	F1_CL_vs_HA	F2_CL_vs_LDOPA	F3_CL_vs_NONI	F4_CL_vs_OAHA	F5_CL_vs_OA to agree with convention used earlier
    cl_avg = -1

    in_header = in_file.readline()
    #if line == 1
            #Read (and pop?) the first line of the csv to ignore the headers there

        
    for line in in_file:
    #for each line in input CSV:
        #cl_avg_found = False
        scaf_pos = parse_unique_ID(line)#Get unique ID [scaf,pos]
        
        if(scaf_pos==[]):
            #attempting to fix the balnk item bug
            continue
        
        print(scaf_pos) #DEBUG
        to_write = line.split(",")[0]#+"," #Starts off with the unique ID and ,
        
        #Make a matching line in outpath
        #Look through all 6 PXLs
        for pxl in SCAN_list:
            vals = scan_pxl(pxl, scaf_pos)
            if((vals[0]==-1)and(vals[1]==-1)):
                continue
                #skips if no match was found.
                
            elif("FIG" in pxl):           
                type_avg[1] = vals[1]
            elif(("HA" in pxl)and ("OA"not in pxl)):
                type_avg[2] = vals[1]
            elif("LDOPA" in pxl):
                type_avg[3] = vals[1]
            elif("NONI" in pxl):
                type_avg[4] = vals[1]
            elif("OAHA" in pxl):
                type_avg[5] = vals[1]
            elif(("OA" in pxl)and ("HA" not in pxl)):
                type_avg[6] = vals[1] 
            type_avg[0]=vals[0] #this will trigger in any condition where val is found. it is overwritten a few times but this shouldn't matter because it's the same value in all cases
        
        deltas = calc_deltas(type_avg)
        for item in deltas:
            to_write+=","
            to_write+=str(item)
        for item in type_avg:
            to_write+=","
            to_write+=str(item)
        to_write = to_write.replace("-1","NA")
            #to_write.append(","+item) #OLD, DELETE 
        to_write+="\n"
        out_file.write(to_write)
        to_write = ""
        type_avg = [-1,-1,-1,-1,-1,-1,-1]
    in_file.close()
    out_file.close()
    print("Output File constructed successfully -- closing program.")    
        
        #Once all the files have been looked at, line everything up and write them to the outfile.
        #reset_temps(type_avg, cl_avg, cl_avg_found, to_write)
        #reset all vars
        
        
def parse_unique_ID(line):
    #takes in a string of the line, returns an array with the unique ID elements
    #Returns [scaf,pos]
    #TODO: Potential problem that this erases some datalines when two edits occur at the same point. this was an issue in the past requiring several fixes.
    #As long as the quantities can be duplicated in the output file, the above should not pose a serious problem.
    raw_id = line.split(",")[0]
    raw_spl = raw_id.split("_")
    return raw_spl[1:3]
    #raw_id format scaffold_0_1004752_FBgn0179780_GM24918
    #raw_spl = [scaffold,0,1004752,FBgn0179780,GM24918]

def reset_temps(type_avg, cl_avg, cl_avg_found, to_write):
    #Resets the temporary variables for the next interation
    type_avg = [-1,-1,-1,-1,-1,-1]
    cl_avg = -1
    cl_avg_found = False
    to_write = ""
    
def assemble_SCAN_list(ed_type):
    all_paths = os.listdir()
    SCAN_list = []
    for path in all_paths: #filter so only the Filtered files are being considered
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

def scan_pxl(pxl, scaf_pos):
    vals = [-1,-1] #CL, avg
    #Debug:
    #print("Looking at pxl:\t", pxl)
    Open_PXL = open(pxl,"r")
    Open_PXL.seek(0)
    for ln in Open_PXL:
        if ln.split("\t")[0]=="^":
            continue
        if ln=="\n":
            continue #there is a trailing \n at the end of the PXL files
        else:
        #If edit in ln:
            #DEBUG BLOCK
            #print("\n\n\nscaf_pos\t")
            #print(scaf_pos)
            #print("ln\t")
            #print(ln)
            #print("ln.split('t')\t")
            #print(ln.split("\t"))
            #print("ln.split('t')[0]\t")
            #print(ln.split("\t")[0])
            #print("ln.split('t')[0].split('_')\t")
            #print(ln.split("\t")[0].split("_"))
            #print("ln.split('t')[0].split('_')[1]\t")
            #print(ln.split("\t")[0].split("_")[1])
            #print("\n\n\n")
            
            if ln.split("\t")[0].split("_")[1]==scaf_pos[0]:
                #DEBUG BLOCK
                #print("scaf match")
                #print("\nln_pos: ")
                #print(ln.split("\t")[1])
                #print("pos: ")
                #print(scaf_pos[1])
                if str(ln.split("\t")[1]).strip()==str(scaf_pos[1]).strip():
                    print("Match found!")
                    cl_ed_pct = ed_pct_of_next_3_lines(Open_PXL)
                    tmnt_ed_pct = ed_pct_of_next_3_lines(Open_PXL)
                    
                    vals = [cl_ed_pct,tmnt_ed_pct]
                    Open_PXL.close()
                    return vals
                    
                    #if cl_avg_found==False:
                    #if CL values not yet found:
                        #Grab CL values from the next 3 lines
                        #average these values and set cl_val to them
                        #cl_avg_found= True
                    #Grab Type Values
                        #Average type_values and set appropriate spot in type_avg to them.
                #If edit not in PXL:
                    #Set type_avg == -1 at appropriate spot.
    #Close PXL
    Open_PXL.close()
    return vals
    
def ed_pct_of_next_3_lines(Open_PXL):
    #meat of this script. Pulls the ref and alt values from the next 3 lines, calculates 
    lines_3 = []
    vals_3 = []
    ref_alt_3 = []
    ref_sum = 0
    alt_sum = 0
    ed_pct = 0
    #just going to hardcode getting the next 3 lines of info
    
    for i in range(0,3):
        lines_3.append(Open_PXL.readline().strip())
        #line format: ^	./intermeds/NVC_a_type0_CL_Galstep87_ON_DATA_22_86_FILT_GENES.txt	A = 41 G = 8	ID=gene:FBgn0179780;Name=GM24918;biotype=protein_coding;gene_id=FBgn0179780;logic_name=flybase
    for ln in lines_3:
        #print(ln.split("\t")) #debug
        vals_3.append(ln.split("\t")[2])
        
    for val in vals_3:
        #val: A = 41 G = 8
        val_sep = val.split(" ")
        #val_sep: [A,=,41,G,=,8]
        ref_alt = [val_sep[2],val_sep[5]]
        ref_alt_3.append(ref_alt)
        
    for ra_pair in ref_alt_3:
        #ra_pair = ["41","8"]
        ref_sum+=int(ra_pair[0]) #sum all the ref counts
        alt_sum+=int(ra_pair[1])
        
    ed_pct = ((alt_sum)/(ref_sum+alt_sum))
    
    return "{0:.5f}".format(ed_pct) #So that it's not a crazy long product of division
    #NOTE: the return in the line above may cause bugs.
    
    #return ed_pct

def calc_deltas(type_avg):
    #calculates the change in editing percent at the given sites. Formula is (treatment ed pct)-(control ed pct)
    
    raw = copy.deepcopy(type_avg)
    for i in range(0,len(raw)):
        raw[i]=str(raw[i])
        
    deltas = [0,0,0,0,0,0,0]
    #type_avg = [-1,-1,-1,-1,-1,-1,-1] #An array to hold the average of each type's values
    #NB: Tpye avg should use ordering CL, FIG, HA, LDOPA, NONI,OAHA,OA to agree with convention used earlier
    #CL = raw[0]
    for i in range(1,len(raw)):
        if(raw[i]=="-1"):
            deltas[i]= "NA"
        else:
            deltas[i]="{0:+.5f}".format(Decimal(raw[i])-Decimal(raw[0]))
        
    return deltas
    
    
if __name__ == "__main__": #sets up a main area. This will not work well if imported
    main()