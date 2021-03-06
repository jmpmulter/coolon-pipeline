##Formats csv files output by the pipeline into more easily analyzeable files
import os
import sys

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__)) #to figure out where the program is being executed. This is home base
    os.chdir(dir_path)
    
    instr = process_runline()#instructions
    #for item in instr:
    #    print(item) #Confirms input information
    
    
    runmode = instr[0]
    in_path = instr[1]
    out_path = instr[2]
    
    if(runmode !="4"):
        if(in_path == ""):
            in_path = input("Enter the name of or relative path to the file to format:\t")
        if(out_path == ""):
            out_path = input("Enter the name of or relative path to the outputted File:\t")
        process_csv(runmode,in_path,out_path)
    else: #Run on all files in directory
        if in_path == "":
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
    in_header = infile.readline().strip()
    out_header = in_header+",Name,ID,nCounts,Ratio_Ref_div_Alt, Ratio_Alt_div_Ref\n"
    outfile.write(out_header)
    
    for line in infile:
        
        buff_ln = ""
        ID = ""
        #no_ratio = False #flipped to true if 
        l0 = line
        l0s = l0.split(",")
        cRef = int(l0s[3].strip())
        cAlt = int(l0s[4].strip())
        nCounts = str(cRef+cAlt) #total number of counts
    
        info = l0s[5].strip().split(";")# information from geneinfo column
    
        try:
            for item in info: #TODO COPY this flexible model for all info fields
                if("gene_id" in item):
                    ID = item.strip().split("=")[1] #Generally a FBGN Number
            if ID == "":
                ID = "NA"
        except:
            ID = "NA"
            print("Non-standard ID field")
        
        
        try:
            for item in info: #TODO COPY this flexible model for all info fields
                if("Name" in item):
                    Name = item.strip().split("=")[1] #Generally a FBGN Number
            if Name == "":
                Name = "NA"
            #Name = info[1].split("=")[1].strip() #Generally GM......
        except:
            Name = "NA"
            print("Non-standard Name Field")
            
            
            
        ratio_r_over_a = ""
        ratio_a_over_r = ""
        
        if((cRef==0)or(cAlt==0)): #TODO figure out how to get around dividing by 0 errors. Not a problem for right now but could be in the future.
            ratio_r_over_a = "NA"
            ratio_a_over_r = "NA"  
        else:
            rda = cRef/cAlt
            adr = cAlt/cRef
            ratio_r_over_a = str(format(rda,'.4f'))
            ratio_a_over_r = str(format(adr,'.4f'))
        
        #print(Name)
        #print(ID)
        
        to_add = [Name,ID,nCounts,ratio_r_over_a,ratio_a_over_r]
        #for item in to_add:
        #    print(item)
        buff_ln = l0.strip()+","+",".join(to_add)+"\n"#TODO ADD ITEMS IN SAME ORDER AS HEADER
        #print(buff_ln)
        #print("\n\n")
        outfile.write(buff_ln)
    
        
#scaffold_3174,1865,./intermeds/NVC_a_type1_OA_Galstep99_ON_DATA_22_98_FILT_GENES.txt,79,13,ID=gene:FBgn0171184;Name=GM16268;biotype=protein_coding;gene_id=FBgn0171184;logic_name=flybaseGM16268,FBgn0171184,92,6.076923076923077,0.16455696202531644
    infile.close()
    outfile.close()

def process_runline():
    """Reads sys.argv and recomposes it as a list. This list sets out what information the program has or will ask for from console input.
        Full input key:
        sys.argv[0]->The Script's name
        sys.argv[1]-> runmode. Default mode is 4, or 1 == user input, 2== command line has file path, 3 == command line has output file path, 4 all CSV files in directory
        sys.argv[2]-> input file path. If runmode ==4, this can be a target directory; else the default is current directory
        sys.argv[3]-> output file path
    """
    runmode = 4
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