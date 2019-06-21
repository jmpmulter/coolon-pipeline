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
            print("Detected Filtered .csv file with path:\t"+path)
            FO_csv_list.append(path)
    
    scan_runner(FO_csv_list,target)
            
            
def scan_runner(FO_csv_list,target):
    for file in FO_csv_list:
        out_path = "SCAN_"+target+"_"+file
        scan_FO(target,file,out_path)
        
def scan_FO(target,in_path,out_path):
    """Searches an in_path csv file for any of the genes in target. Escapes on the first instance. Only gives whether or not those genes exist, prints total number of hits/total

    """
    tfile = open(target, "r")
    infile = open(in_path,"r")
    outfile = open(out_path,"x")
    list_hits = []
    i = 0
    j = 0
    
    for line in tfile:
        Name = line.strip()#line.split(",")[0].strip()
        j+=1
        #skip header of infile #TODO URG
        infile.seek(0) #resets cursor to the beginning of the file.
        in_header = infile.readline().strip()
        #print(line)
        for l1 in infile:
            l1_name = l1.split(",")[6].strip()
            #print("CHECK")
            if Name == l1_name:
                #print("HIT")
                if (Name in list_hits):
                    pass
                    print("Hit already Detected")
                else:
                    list_hits.append(Name)
                    i+=1
                
                
    
    #get the info out of the dictionary, sort it, write it
    
    sorted_hits = sorted(list_hits)
    #print hits/target
    for hit in sorted_hits:
        outfile.write(hit+",\n")
            
    tfile.close()
    infile.close()
    outfile.close()
    print(str(i)+"/"+str(j)+"\t hits/targets in\t"+out_path)
    
if __name__ == "__main__": #sets up a main area. This will not work well if imported
    main()