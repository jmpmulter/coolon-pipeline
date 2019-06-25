#unite_scans
#Takes all the csv SCAN files in the folder and turns them into USCAN (United Scan) List of all the files hits on targets
import os
import sys

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__)) #to figure out where the program is being executed. This is home base
    os.chdir(dir_path)
    outpath = ""
    try:
        outpath= sys.argv[1]
    except IndexError:
        outpath = input("Target file not entered in command line. Enter name of target file")
    
    all_paths = os.listdir()
    SCAN_list = []
    for path in all_paths: #filter so only the Filtered files are being considered
        if ("SCAN" in path):
            print("Detected SCAN file with path:\t"+path)
            SCAN_list.append(path)
    
    unite_scan(SCAN_list,outpath)
            
            
def unite_scan(path):
    scans = []
    for file in FO_csv_list:
        out_path = "SCAN_"+target+"_"+file
        scans.append(u_scan(file))
    return scans
        
def u_scan(inpath):
    infile = open(inpath,"r")
    
    list_hits = []
    
    infile.seek(0) #resets cursor to the beginning of the file.
    for line in infile:
        list_hits.append(line.strip())#line.split(",")[0].strip()
    infile.close()
    return list_hits
 aaaa#TODO CONTINUE WORKING HERE
    
if __name__ == "__main__": #sets up a main area. This will not work well if imported
    main()