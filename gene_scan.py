#gene_scan.py
#Scans formatted csv files for chosen genes of interest from a target file

#

# #NOTE: This could be optomized by reading every nth line, where n is the number of types per file. For now I'm writing it slow just to make writing easier.
# #NOTE: To do this speedup I would need to infer the number of types from a quick initial read, OR read some former filelist file.

#prepare infile and outfile paths
#Looks at every csv in the folder
#for each csv:
#counter = 0
#for each line in targets:
#for each line in csv:
#if gene ==Name:
#add Name to a dictionary
#then export the dictionary to a list
#sort the list
#write the list to a SCAN file

import os
import sys

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__)) #to figure out where the program is being executed. This is home base
    os.chdir(dir_path)
    target = ""
    try:
        target= sys.argv[1]
    except IndexError:
        target = input("Target file not entered in command line. Enter name of target file")
    
    all_paths = os.listdir()
    FO_csv_list = []
    for path in all_paths: #filter so only the Filtered files are being considered
        if ("FO" in path):
            print("Detected .csv file with path:\t"+path)
            csv_list.append(path)
        for csv in csv_list:
            out_path = "FO_"+csv
            print("Processing with inputs:\t4\t"+in_path+"\t"+out_path)
            process_csv(4,csv,out_path)
    
    
if __name__ == "__main__": #sets up a main area. This will not work well if imported
    main()