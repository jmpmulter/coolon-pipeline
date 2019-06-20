##Formats csv files output by the pipeline into more easily analyzeable files
import os
import sys

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__)) #to figure out where the program is being executed. This is home base
    os.chdir(dir_path)
    
    instr = process_runline()#instructions
    for item in instr:
        print(item) #Confirms input information
    
    
    runmode = instr[0]
    in_path = instr[1]
    out_path = instr[2]
    
    if(runmode !=4):
        if(in_path == ""):
            in_path = input("Enter the name of or relative path to the file to format:\t")
        if(out_path == ""):
            out_path = input("Enter the name of or relative path to the outputted File:\t")
        process_csv(runmode,in_path,out_path)
    else: #Run on all files in directory
        if in_path = "":
            pass
        else:
            os.chdir(in_path)
        all_paths = os.listdir()
        csv_list = []
        for path in all_paths: #filter so only the .csv files are being considered
            if (".csv" in path):
                print("Detected .csv file with path:\t"+path)
                csv_list.append(path)
        for csv in csv_list:
            out_path = "FO_"+csv
            print("Processing with inputs:\t4\t"+in_path+"\t"+out_path)
            process_csv(4,csv,out_path)
        
    
def process_csv(runmode,in_path,out_path):
    infile = open(in_path, 'r')
    outfile = open(out_path, 'x')
    buff_ln = "" #String which represents the next line to be written to outfile
    in_header = f.readline().strip()
    out_header = in_header+",Name,ID,nCounts,Ratio_Ref_div_Alt, Ratio_Alt_div_Ref\n"
    outfile.write(out_header)
    
    for line in infile:
        buff_ln = ""
        #no_ratio = False #flipped to true if 
        l0 = line
        l0s = l0.split(",")
        cRef = int(l0s[3].strip())
        cAlt = int(l0s[4].strip())
        nCounts = str(cRef+cAlt) #total number of counts
        info = l0s[5].strip().split(";")# information from geneinfo column
        ID = info[0].split(":")[1].strip() #Generally a FBGN Number
        Name = info[1].splint("=")[1].strip() #Generally GM......
        
        ratio_r_over_a = ""
        ratio_a_over_r = ""
        if((cRef==0)or(cAlt==0)): #TODO figure out how to get around dividing by 0 errors
        #    no_ratio = True
            ratio_r_over_a = "NA"
            ratio_a_over_r = "NA"  
        else:
            ratio_r_over_a = str(cRef/cAlt)
            ratio_a_over_r = str(cAlt/cRef)
        
        to_add = [Name,ID,nCounts,ratio_r_over_a,ratio_a_over_r]
        buff_ln = l0.strip()+",".join(to_add)+"\n"#TODO ADD ITEMS IN SAME ORDER AS HEADER
        
        outfile.write(buff_ln)

    infile.close()
    outfile.close()

def process_runline():
    """Reads sys.argv and recomposes it as a list. This list sets out what information the program has or will ask for from console input.
        Full input key:
        sys.argv[0]->The Script's name
        sys.argv[1]-> runmode. No arg or 1 == command line input, 2==input file path, 3 == output file path, 4 all CSV files in directory
        sys.argv[2]-> input file path. If runmode ==4, this can be a target directory; else the default is current directory
        sys.argv[3]-> output file path
    """
    runmode = 0
    in_path = ""
    out_path = ""
    if len(sys.argv) == 2:
        runmode = sys.argv[1]
    elif len(sys.argv)==3:
        runmode = sys.argv[1]#1== command line input, 2 == input path selected, 3 == output path selected
        in_path = sys.argv[2]#file_in_path   
    elif len(sys.argv)==4:
        runmode = sys.argv[1]#1== command line input, 2 == input path selected, 3 == output path selected
        in_path = sys.argv[2]#file_inpath
        out_path = sys.argv[3] #file_outpath
    else:
        print("No runline commands detected. Manual command entry mode")
        runmode = 1
    return [runmode,in_path,out_path]
    


if __name__ == "__main__": #sets up a main area. This will not work well if imported
    main()