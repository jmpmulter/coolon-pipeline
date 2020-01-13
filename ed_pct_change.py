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
        outpath= sys.argv[1]
    except IndexError:
        outpath = input("Output file name not entered in command line. Enter name of output file")
    
    all_paths = os.listdir()
    SCAN_list = []
    for path in all_paths: #filter so only the Filtered files are being considered
        if ("SCAN" in path): #TODO edit this to only look at the PXL and other relevant files
            print("Detected SCAN file with path:\t"+path)
            SCAN_list.append(path)
    
    compile_stats(SCAN_list,inpath, outpath) #ADD INPATH, ED Type in command line
    
def compile_stats(SCAN_list,inpath, outpath, ed_type):
    #TODO Write header line
    #Vars:
    type_avg = [-1,-1,-1,-1,-1,-1] #An array to hold the average of each type's values
    cl_avg = -1
    #for each line in input CSV:
        #Get unique ID
        #Make a matching line in outpath
        #Look through all 6 PXLs
            #If edit in PXL:
                #if CL values not yet found:
                    #Grab CL values
                    #average these values and set cl_val to them
                #Grab Type Values
                    #Average type_values and set appropriate spot in type_avg to them.
            #If edit not in PXL:
                #Set type_avg == -1 at appropriate spot.
        #Once all the files ahve been looked at, line everything up and write them to the outfile.
            