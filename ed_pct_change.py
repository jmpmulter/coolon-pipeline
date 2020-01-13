#ed_pct_change.py
#This program needs to isolate the unique Identifiers, then find percent editing in CL, find pct editing in other conditions, show change in percent editing.
#Things to consider: There will be some where the edit does not pop up
#I'm using the PXL's as sources of info because their formatting will make this easier, at least i think
#Current plan is to construct a CSV of all the info. Then to tack that info on to the original spreadsheet.

#A second script will merge the info

import sys
import os
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
    
    f_in = open(inpath,"r")
    f_out = open(outpath,"w")
    f_in.seek(0)
    
    
    all_paths = os.listdir()
    SCAN_list = []
    for path in all_paths: #filter so only the Filtered files are being considered
        if ("PXL" in path): #TODO Confirm this edit worked TODO edit this to only look at the PXL and other relevant files
            print("Detected PXL file with path:\t"+path)
            SCAN_list.append(path)
    
    compile_stats(SCAN_list,inpath, outpath) #ADD INPATH, ED Type in command line
    
def compile_stats(SCAN_list,inpath, outpath, ed_type):
    #TODO Write header line
    #header format: "uniqueID, CL_delta, FIG_delta, HA_delta, LDOPA_delta, NONI_delta, OAHA_delta, OA_delta, CL_avg, FIG_avg, HA_avg, LDOPA_avg, NONI_avg, OAHA_avg, OA_avg"
    #header puts most relevant information up front, but more detailed work a bit futher back
    #Vars:
    type_avg = [-1,-1,-1,-1,-1,-1] #An array to hold the average of each type's values
    #NB: Tpye avg should use ordering F0_CL_vs_FIG	F1_CL_vs_HA	F2_CL_vs_LDOPA	F3_CL_vs_NONI	F4_CL_vs_OAHA	F5_CL_vs_OA to agree with convention used earlier
    cl_avg = -1
    #for each line in input CSV:
        #if line == 1
            #Read (and pop?) the first line of the csv to ignore the headers there
        cl_avg_found = False
        #else:
            scaf_pos = parse_unique_ID(line)#Get unique ID
            to_write = "" #TODO write this line later
            #Make a matching line in outpath
            #Look through all 6 PXLs
            for pxl in SCAN_list:
                Open_PXL = open(pxl,"r")
                for ln in Open_PXL:
                    if ln.split(",")[0]==">":
                        continue
                    else:
                    #If edit in ln:
                        if ln.split(",")[0]==scaf_pos[0]:
                            if ln.split(",")[1]==scaf_pos[1]:
                                if cl_avg_found==False:
                                #if CL values not yet found:
                                    #Grab CL values from the next 3 lines
                                    #average these values and set cl_val to them
                                    cl_avg_found= True
                                #Grab Type Values
                                    #Average type_values and set appropriate spot in type_avg to them.
                            #If edit not in PXL:
                                #Set type_avg == -1 at appropriate spot.
                #Close PXL
        #Once all the files have been looked at, line everything up and write them to the outfile.
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




 