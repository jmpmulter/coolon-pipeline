import sys
import re
import os
import shutil
#import pandas as pd
#import numpy as np
#from functools import reduce
#from pandas import ExcelWriter
#from pandas import ExcelFile
#import matplotlib.pyplot as plt
#from scipy.stats import ttest_ind 

## init gets user input for paramaters of the program.
##0== hardcoded test info for OA/CL set. 1== user popup/console input. 2== read input from text file. File structure may already be established, and maybe reading names from text fie

def main():

##TODO CALL PRE_CHECK AT THE APPROPRIATE LOCATION
    
    header = ["0: .gff3 and Settings","1: *.vcf","2: *FILT_NVC","3: Findgene Output","4: compgene outputs","5: Final Outputs"]
    filelist = [["","",""],[],[],[],[],[]] #filelist is a list of all inputted and logged files.
    
    dir_path = os.path.dirname(os.path.realpath(__file__)) #to figure out where the program is being executed. This is home base
    os.chdir(dir_path) #move the cwd to the dir_path
    cwd = os.getcwd() #This will be useful for doing things within the current directory
    #0=[.gff3,filt.gff3, setup_file], 1=*.vcf, 2=*filt_vcf, 3= *findgene output, 4=compgene outputs, 5= OUTPUTS [make_pxl output, make_csv Output, filelist_output]
    
    ##INITIALIZE
    #make sure settings file is searched for and added to filelist
    runmode=0 #mode in which the program will be operated TODO MAKE THIS USER INPUT
    types = get_types(runmode) #the names of the different types of conditions (control, OA, HA, ...)
    ed_type = get_ed_type(runmode)# are we looking for A/I or C/U?
    init(types, runmode) #test mode init(0)
    #init(1) # User input mode
    #init(2, "INPATH")# Read in from file mode
    ##USER LOADS FILES
    loaded = ""
    #ADD: ability to read loaded from input
    while(loaded!="c"):
        print(types)
        loaded=input("Load Input files into their appropriate folders. Enter \'c\' to Continue, or \'e\' to Exit the program.").strip().lower()
        if loaded=="e":
            break
    if loaded =="e":
        sys.exit() #exit before data intensive steps
    #RUN pre_check()
    sys.stdout.write("\n Running    pre_check")
    
    run_pre_check(dir_path, cwd)
    sys.stdout.write("\n Completed  pre_check")
    
    ##Add all to file list
    sys.stdout.write("\n Running   Standardize")
    standardize(filelist, types, dir_path, cwd)#add correct inputs
    sys.stdout.write("\n Completed Standardize")
    #VCF Filter
    sys.stdout.write("\n Running   VCF_Filter")
    run_vcf_filter(filelist, dir_path)
    sys.stdout.write("\n Completed VCF_Filter")
    #GFF3 Filter
    sys.stdout.write("\n Running   GFF3_Filter")
    run_gff3_filter(filelist, dir_path)
    sys.stdout.write("\n Completed GFF3_Filter")
    #Findgene
    sys.stdout.write("\n Running   FINDGENE")
    run_findgene(filelist, dir_path)
    sys.stdout.write("\n Completed FINDGENE")
    #COMPGENE
    sys.stdout.write("\n Running   COMPGENE")
    run_compgene(filelist, dir_path)
    sys.stdout.write("\n Completed COMPGENE")
    #MakePXL
    sys.stdout.write("\n Running MakePXL")
    os.chdir(dir_path)
    pxl_name = "./outputs/PXL.txt" #can modify for more flexibility later
    make_pxl(filelist[4][-1], filelist[3], pxl_name)
    filelist[5][0] = pxl_name
    #make_pxl(filelist[4][-1]) #store in outputs and filelist[5][0]
    #MakeCSV
    csv_name = "./outputs/CSV.txt" #can modify for more flexibility later
    make_csv(filelist[5][0], csv_name) #store in outputs and filelist[5][1]
    filelist[5][1] = csv_name
    #Output filelist for confirmation that all files were correctly processed
    filelist_name = "./outputs/filelist_output.txt"
    filelist[5][2] = filelist_name
    output_files_used(filelist, header, dir_path)
    sys.stdout.write("\n Execution Completed, Ending Program")


def get_ed_type(runmode):
    ed_type = ""
    if (runmode == 0 | runmode == 1):
        while(ed_type!="a"& ed_type!="c"):
            ed_type = input("Run for A-to-I or C-to-U editing? Enter a or c").lower().strip() #note: incorrect inputs will just trigger the loop to repeat.
            
        return ed_type
    elif runmode ==2:
        #MAKE ABLE TO READ INPUT FROM A FILE
        return 
    else:
        sys.stdout.write("\n ERROR in get_ed_type. runmode-based error. Exiting program")
        sys.exit()

def clear_pipe(dir_path, cwd):
    folder = dir_path+"/intermeds"
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def run_pre_check(dir_path, cwd):
    pre_check_meanings = {1:"pre_check passed",2:"pre_check failed in inputs",3:"pre_check failed in intermeds",4:"pre_check failed in outputs"}
    pre_check_val = pre_check(dir_path, cwd)
    if pre_check_val!=1:
        sys.stdout.write("\n"+pre_check_meanings[pre_check_val])
        quit_in_pre = input("pre_check detected errors. Proceed anyway? c to continue, r to clear intermeds and outputs, n to quit program. c/r/n ").lower().strip()
        if(quit_in_pre=="n"):
            sys.stdout.write("Exiting. Goodbye")
            sys.exit()
        elif(quit_in_pre=="r"):
            clear_pipe(dir_path, cwd)
            run_pre_check(dir_path, cwd) #Recursively runs the pre_check to try to fix errors. quits when no error detected OR when y is input
        elif(quit_in_pre =="c"):
            sys.stdout.write("\n pre_check process bypassed (with command c)")
            return
    else:
        sys.stdout.write("\n"+pre_check_meanings[pre_check_val])
        return
        
def pre_check(dir_path, cwd):
    """Checks if files are correctly set up. Returns 1 if files correctly set up. returns 2 if error in inputs, 3 if error in intermeds, 4 if error in outputs.
    
    pre_check processes inputs then intermeds then outputs, and returns on the first potential error detected.
    An error in inputs may preclude detecting an issue in intermeds or outputs. intermeds error could preclude detecting in outputs"""
    sys.stdout.write("\n Performing Pre-Check of file setup")
    sys.stdout.write("\n Checking "+dir_path+"/inputs")
    #check that inputs are not formatted to processed name format
    #get list of directories beginning with t
    dirs = os.listdir(dir_path+"/inputs")

    for dir in dirs:
        if dir[0]=="o":
            continue
        elif(dir[0]=="t"):
            files = os.listdir(dir_path+"/inputs/"+dir)
            for file in files:
                if "Galstep" in file:
                    sys.stdout.write("Error: File Names already standardized at: "+dir_path+"/inputs/"+dir+"/"+file)
                    sys.stdout.write("Input issue -- FAIL")
                    return 2
        else:
            sys.stdout.write("unexpected directory detected. potential issue at: "+dir_path+"/inputs/"+dir)
            sys.stdout.write("Input issue -- FAIL")
            return 2
    #check each file for "Galstep." If Match: return 2, print input fail
    sys.stdout.write("\n inputs unformatted - PASS")
        
    
    #check that intermediates empty
    sys.stdout.write("\n Checking "+dir_path+"/intermeds")
    if not os.listdir(dir_path+"/intermeds"):
        print(dir_path+"/intermeds\t is empty - PASS")
        pass
    else:
        print(dir_path+"/intermeds\t is NOT empty - FAIL") 
        return 3
    #check that outputs empty
    sys.stdout.write("\n Checking "+dir_path+"/outputs")
    if not os.listdir(dir_path+"/outputs"):
        print(dir_path+"/outputs\t is empty - PASS")
        pass
    else:
        print(dir_path+"/outputs\t is NOT empty - FAIL") 
        return 4
    return 1


def init(types, runmode=1, in_path="",):
    if(runmode == 0): #condition to skip re-placing the files for test mode
        skip_init = input("skip init? y/n")
        if (skip_init=="y"):
            return
    os.mkdir("inputs") #for raw input files
    #note: when testing, make sure that the current path is still . and is NOT ./inputs
    #if necessary, reset cursor
    os.mkdir("intermeds") #files produced internally (filtered versions, etc) that end user is not expected to see
    os.mkdir("outputs") #files that the end user would want to see (comparison files, pxl, excel)
    numtypes=0 #number of types of files to be compared. For example, 2 types is control and experimental. 3 skips init entirely
    #types_raw =[] #input variable #maybe extra, delete soon
    typenames =[] #List of touples patterned (typenumber, verbal name) #return
    #ed_type = ""
    #already_init = False
    #If/elif conditions to get the info. create stuff after the info is recorded.
    #if (False): """INPUT FOLDER ALREADY EXISTS. This conditional must be edited"""
    #   already_init = True
    #make flexible for if init performed or not already
    if runmode == 3: #escape
        return
    elif runmode==0:
    #hardcoded test info
        print("Standard CL/OA test mode selected. 2 types")
        numtypes=2
        #typenames=[("type1","CL"),("type2","OA")] 
        #ed_type = "AG"
        #already_init = False #Make this true if the file tree is already initialized in mode ==2
        
    elif runmode ==1:
        #user input
        print("Manual Input Selected.")
        numtypes=input("Number of types (integer, 2 is standard for control and experimental)")
#       """raw_types=raw_input("In Order, what are the names of these types (separated by commas)").split(",").strip()
#       for i in range(0,len(raw_types)):
#           typenames.append(("type{}"format(str(i)),raw_types[i]))
#       ed_type=raw_input("What type of editing to look for ? A/G or C/U? Enter A or C").strip()
#       #add an input checker to make sure this can take only a,A,c,C
#       if(ed_type.islower()): #checks if the edtype is lower case
#           ed_type=ed_type.upper()#changes it to upper case if necessary
        
    elif runmode ==2: #TODO: MAKE EXECUTABLE FROM A FILE
        print("Input from text file mode selected")
        #from inpath
        
        # read input from a text file at in_path
        #be ready for the file structure to already be initialized. If this is the case, just get the names and editing type and 
            #already_init = True
        
    else:
        #print error and exit       
        print("Error in init. Exiting Init component.")
        return
    
    
    for i in range(0,numtypes): #make sure this works, flexibly
        dirname = "./inputs/type{}_{}".format(str(i),types[i])
        os.mkdir(dirname)
    os.mkdir("./inputs/other")
def get_types(runmode):
    types = []
    if runmode == 3: #Input of a new runmode
        runmode = input("input new mode (0 for standard test, 1 for manual entry, 2 for document entry")
    if runmode == 0: #test
        types =["CL","OA"]
    elif runmode == 1: #user input
        types=raw_input("In Order, what are the names of these types (separated by commas)").split(",").strip()
    elif runmode == 2: #read from file
        #read types from file
        pass
    return types

def standardize(filelist, types, dir_path, cwd):
    directories = os.listdir(dir_path+"/inputs") 
    for directory in directories:
        if directory != ("other"):
            standardize_NVCs(filelist, types, dir_path, cwd, directory)
    other_contents = os.listdir(dir_path+"/inputs/other")
    for item in other_contents:
        if(".gff3" in item):
            filelist[0][0]="./inputs/other/"+item 
        elif("settings" in item):
            print("settings document detected. Previously added to filelist")
            continue #TODO make this work from the settings document
        else:
            print("Unrecognized input format. Excluded from filelist:\t"+ item)
        
def standardize_NVCs(filelist, types, dir_path, cwd, directory):
    for filename in os.listdir("./inputs/"+directory): #TODO Confirm the ./ not needed.
        os.chdir(dir_path)
        oldname = filename #Format: Galaxy34-[Naive_Variant_Caller_(NVC)_on_data_19_and_data_26].vcf
        #sys.stdout.write("\noldname\t"+oldname) #debug
        type_info = directory.split("/")[-1].strip()
        
        gal_num = oldname.split("-")[0].split("y")[1].strip() #isolate the number
        fasta_step = oldname.split("_")[6].strip()
        #sys.stdout.write("\noldname\t"+oldname) #debug
        #sys.stdout.write("\n\nbam_step = oldname.split(_)[9]") #debug
        #sys.stdout.write(str(oldname.split("_"))) #debug
        
        bam_step = oldname.split("_")[9].split(".")[0].strip()
        newname = "NVC_"+type_info+"_Galstep"+gal_num+"_ON_DATA_"+fasta_step+"_"+bam_step+".vcf"#New Format: NVC_TYPE#_TYPE_GALAXY STEP NUMBER_ON_DATA_FASTASTEP#_BAMSTEP#.vcf
        os.chdir("./inputs/"+directory)
        os.rename(oldname, newname)
        filelist[1].append("./inputs/"+directory+"/"+newname)#make sure the path gets in here
    os.chdir(dir_path)
        
def run_vcf_filter(filelist,dir_path): #Helper function to run several calls of VCF_filter1
    for vcf_file in filelist[1]:
        os.chdir(dir_path)
        #print(vcf_file)
        clean_name = vcf_file.split("/")[3].split(".")[0].strip()
        outpath = "./intermeds/"+clean_name+"_FILT.txt"
        vcf_filter1(vcf_file, outpath)
        filelist[2].append(outpath)#make sure the path gets in here
        
def run_gff3_filter(filelist, dir_path):
    os.chdir(dir_path)
    clean_name = filelist[0][0].split("/")[3].split(".")[0].strip()
    outpath = "./intermeds/"+clean_name+"_FILT_gff3.txt"
    gff3_filter(filelist[0][0], outpath)
    filelist[0][1] = outpath #make sure the path gets in here

def run_findgene(filelist, dir_path):
    for filt_vcf in filelist[2]:
        os.chdir(dir_path)
        clean_name = filt_vcf.split("/")[2].split(".")[0].strip()
        outpath = "./intermeds/"+clean_name+"_GENES.txt"
        sys.stdout.write("\n RUNNING find_gene of "+outpath)
        find_gene(filt_vcf, filelist[0][1],outpath)
        filelist[3].append(outpath)#make sure the path gets in here
        sys.stdout.write("\n COMPLETED find_gene of "+outpath)

def run_compgene(filelist, dir_path):
    for i in range(0,len(filelist[3])-1): #1 fewer comparison than there are items in the list
        if(i==0):
            outpath = "./intermeds/COMP_0.txt"
            comp_gene(filelist[3][0],filelist[3][1],outpath)#compare First 2 files
            filelist[4][0] = outpath
        else:
            #compare filelist[4][-1] to filelist[3][i] #TODO potentially to i+1?
            outpath = "./intermeds/COMP_{}.txt".format(str(i))
            comp_gene(filelist[4][-1],filelist[3][i+1],outpath)#compare most recent comparison file with next file on filelist
            filelist[4].append(outpath)
        
def output_files_used(filelist, header, dir_path):
    new_file = open(filelist[5][2], 'x')
    for i in range(0,len(header)):
        new_file.write(header[i]+": ")
        for j in range(0,len(filelist[i])):
            new_file.write(filelist[i][j]+"\t")
        new_file.write("\n")
    
def vcf_filter1(vcf, filter_vcf):
    try:
        new_file = open(filter_vcf, 'x')
        open_vcf = open(vcf, 'r')
        open_vcf.seek(0)
        
        for line in open_vcf:
            vcf_line = line.split('\t')
            if "#" in line or vcf_line[0] == '/n' or vcf_line[3] != 'A' or vcf_line[4] != 'G': #Changes here for C/U
                continue
            #print(line)  
            n1 = vcf_line[9].split(':')[-1]
            n2 = n1.split(',')[0:-1]
            numA = 0
            numG = 0
            for x in n2:
                num = int(x.split('=')[-1])
                if 'A' in x:
                    numA += num
                elif 'G' in x:
                    numG += num
                else:
                    print("WRONG BASE SOMETHING WRONG AHHH")
            
            new_file.write(line + '\t' + ':A=' + str(numA) + ',' + 'G=' + str(numG) + ',' + '\n')
#           Sample Output into filtered file
#           scaffold_0  26626   .   A   G   .   .   AC=1;AF=0.00833333333333;SB=2.79069767442   GT:AC:AF:SB:NC  0/0:1:0.00833333333333:2.79069767442:+A=77,-A=42,-G=1,
#           :A=119,G=1,
            #print(line + '\t' + ':A=' + str(numA) + ',' + 'G=' + str(numG) + ',' + '\n')
                
            #print(n2)
    
    except FileExistsError:
        print(vcf + filter_vcf + ' already exists')

#vcf_filter1('C1.vcf','C1_filtered.txt')


#def vcf_filter(vcf, filter_vcf): try: new_file = open(filter_vcf, 'x') open_vcf = open(vcf, 'r') open_vcf.seek(0):
#
#    for line in open_vcf:
#        vcf_line = line.split('\t')
#        if "#" in line:
#            continue
#        if vcf_line[0] == '\n':
#            continue
#        n1 = vcf_line[9].split(',')
#        n2 = n1[0].split(':')[3] + n1[1] #this has the form 'A=*G=*'
#        n3 = list(map(str, n2))
#        if n3[-1] == '\n': #gets rid of \n on the end
#            del n3[-1]
#        i=0
#        while(i < len(n3)):             
#            if n3[i] == '=':
#                del n3[i]
#                i = i - 1 
#            i = i + 1
#        #print(n3)
#        j = 1
#        numRef = ''
#        numAlt = ''
#        if n3[0] == 'A': #this grabs the number of ref
#            while(n3[j] != 'G'):
#                numRef = numRef + n3[j] 
#                j = j+1
#            #print('A=',numRef)
#        if n3[j] == 'G':
#            j = j + 1 
#            while(j < len(n3)): #this grabs the number of alt
#                numAlt = numAlt + n3[j]
#                j = j + 1
#            #print('G=', numAlt)
#
#        if numRef != '' and ((int(numRef) + int(numAlt)) > 10):
#            new_file.write(line)
#    open_vcf.seek(0)
#    new_file.close()
#    open_vcf.close()
#
#
#except FileExistsError:
#    print('the file ' + filter_vcf + ' already exists')
#
    

#u = unfiltered, f = filtered
#vcf_filter('Galaxy129u.txt', 'Galaxy129f.txt')

#counts num of a-to-g events 
def count(file):
    count_a_to_g = 0
    test = 0
    with open(file, 'r') as open_file:  #'r' is opening the file in read mode
        for line in open_file:          #loops through all lines in file
            if "A\tG" in line:
                if "AC=1" in line:      
                    count_a_to_g = count_a_to_g
                else: 
                    count_a_to_g = count_a_to_g + 1  #change to +=1?
        

    print ("Number of A-to-I Editing Sites is:", count_a_to_g)
#count('data.vcf')

#count('C1_filtered.txt')


#filter out so only get genes IN GFF3
def gff3_filter(gff3, filter_gff3):
    try:
        new_file = open(filter_gff3, 'x')
        open_gff3 = open(gff3, 'r')
        open_gff3.seek(0)

        for line in open_gff3:
            gff3_line = line.split('\t')
            if len(gff3_line) > 8:
                #print(gff3_line)
                gff3_id = gff3_line[8]
                id_check = gff3_id.split(':')
                if id_check[0] == 'ID=gene':
                    new_file.write(line)

        open_gff3.seek(0)
        new_file.close()
        open_gff3.close()

    except FileExistsError:
        print('the file ' + filter_gff3 + ' already exists')

#gff3_filter('dsechellia.gff3', 'filt_dsechellia.gff3')

#takes the result of vcf_filter and gff3_filter
#find_gene(vcf, gff3, file) takes a vcf file, a gff3 file and an out path (what you want your new file to be named) 
#and will return a new file with the scaffold, vcf position and the gene ID. (can add more things by adding to line 38). 
#must input the files into the function in this order or it will not work.'''

def find_gene(vcf, gff3, file):
    try:
        new_file= open(file, 'x')
        open_vcf = open(vcf, 'r')
        open_gff3 = open(gff3, 'r')
        open_vcf.seek(0) #see line 39
        open_gff3.seek(0) #see line 39
        for line0 in open_vcf:
            vcf_line = line0.split('\t')
            if vcf_line[0] == '\n': #if line is empty (just white space) skip to next line in vcf file
                continue
            #vcf_line[-1].split(':') 
            get_nums = vcf_line[-1].split(':')
            num = get_nums[-1].strip()
            num_strip = num.split(',')
            num0 = num_strip[0].split('=')
            num1 = num_strip[1].split('=')
            if len(num0) < 2: #no ref
                continue 
            if len(num1) < 2: #no alts
                continue
            #print(len(num0))
            #print(len(num1))
            refA = int(num0[1])
            altG = int(num1[1])
            if refA == 0: #if no ref obs then throw out
                continue
            if refA + altG < 10: #if num ref + num alt is < 10 throw out 
                continue
            vcf_scaffold = vcf_line[0]
            vcf_pos = vcf_line[1]
            for line1 in open_gff3:
                gff3_line = line1.split('\t')
                #print(gff3_line)
                gff3_scaffold = gff3_line[0]
                if vcf_scaffold == gff3_scaffold: #checking scaffolds against each other
                    #print(vcf_scaffold)
                    gff3_initial = gff3_line[3]
                    gff3_final = gff3_line[4]
                    gff3_id = gff3_line[8]
                    id_check = gff3_id.split(':')
                    if id_check[0] != 'ID=gene':
                        continue
                    if int(vcf_pos) >= int(gff3_initial) and int(vcf_pos) <= int(gff3_final):
                        #print(gff3_line)
                        new_file.write(vcf_scaffold + ' ' + vcf_pos + ' ' + gff3_id + ' ' +'A = ' + num0[1] + ' G = ' + num1[1] + '\n')
            open_gff3.seek(0) #stackoverflow told me to do this and it worked.. resets the cursor 
                              #to the first for loop.. 
                
        new_file.close()
        open_vcf.close()
        open_gff3.close()
            
    except FileExistsError:
        print('the file ' + file + ' already exist')

                
#find_gene('C1_filtered.txt','filt_dsechellia.gff3','C1_genes.txt')

#comp_genes(f0, f1, new_file) = new_file with the SNPs that are
#common to both f0 and f1


def comp_gene(f0, f1, file):
    new_file = open(file, 'x')
    open_f0 = open(f0, 'r')
    open_f1 = open(f1, 'r')
    open_f0.seek(0)
    open_f1.seek(0)
    
    for line0 in open_f0:
        l0 = line0.split(' ')
        #print(l0)
        scaffold0 = l0[0]
        if scaffold0 == '' or scaffold0 == 'A' or scaffold0 == '\n':
            continue
        pos0 = l0[1]
        #print(pos0)

        for line1 in open_f1:
            l1 = line1.split(' ')
            #print(l1)
            #print(l1[0] + ' ' + l1[1])
            scaffold1 = l1[0]
            if scaffold1 == '' or scaffold1 == 'A' or scaffold1 == '\n':
                continue
            pos1 = l1[1]
            #print(scaffold1 + 'ONE') 

            if scaffold0 == scaffold1 and pos0 == pos1:
                new_file.write(scaffold0 + ' ' + pos0 + '\n')
        open_f1.seek(0)

    new_file.close()
    open_f0.close()
    open_f1.close()
        
#comp_gene('C1_genes.txt', 'C2_genes.txt', 'comp_C1_2.txt')
#comp_gene('C1_genes.txt', 'C3_genes.txt', 'comp_C1_3.txt')
#comp_gene('comp_C1_2.txt', 'comp_C1_3.txt', 'repC_genes.txt')
#comp_gene('HA1_genes.txt', 'HA2_genes.txt', 'comp_HA1_2.txt')
#comp_gene('HA1_genes.txt', 'HA3_genes.txt', 'comp_HA1_3.txt')
#comp_gene('comp_HA1_2.txt', 'comp_HA1_3.txt', 'repHA_genes.txt')
#comp_gene("comp_CL_1_2_3_All.txt","comp_OA_1_2_3_All.txt","compFinal.txt")

def make_pxl(compOutput, genes, outpath):
    compO = open(compOutput, 'r')
    new_file = open(outpath, 'x')
    
    for line in compO:
        #print(line)
        l = line.split(' ')
        if len(l) != 2:
            continue
            
        scafC = l[0] #scaffold of comparison location
        posC = l[1] #position of comparison location on scaffold
        #print('========POS C========')
        #print(posC)
        
        new_file.write(scafC + '\t' + posC) #Writes the scaffold and position to the PXL
        #print(scafC + '\t' + posC)
        
        for file in genes:
            f = open(file, 'r')
            #print(f)
            for line0 in f:
                l0 = line0.split(' ')
                #print(l0)
                #print(l0)
                scafG = l0[0] # For matching to scafC
                posG = l0[1] #For matching to posC
                if posG == 'A': #if it's not a full data line (format of gene has an enter in it beofre A and G counts)
                    continue #Unless some weirdness occurs in processing, this condition should never trigger
                #print('=========POS G=======')
                #print(posG)
                
            
                
                if int(posC) == int(posG): #If the lines' posiitons do match:
                    #print('TRUE')
                    if scafC == scafG:    #If the lines' scaffolds do match:
                        #find out how to get name of a file (f) 
                        new_file.write('^' + '\t' + file + '\t' + next(f)+'\t'+l0[-1]) #TODO MAKE SURE THIS CHANGE WORKS
                        #print('^' + '\t' + file + '\t' + next(f))
                        
def make_csv(pxl, outpath):

    pxl = open(pxl, 'r')
    new_file = open(outpath, 'x')
    new_file.write("Scaffold,Position,RunFileName,Ref,Alt,GeneInfo\n") #TODO ADD GENEINFO INTO HERE
    scaf=""
    pos=""
    for line in pxl:

        if(line[0]!="^"):
            #print(line)
            splittab = line.split("\t")
            #print(splittab)
            scaf = splittab[0]
            pos = splittab[1].strip("\n")
        elif(line[0]=="^"):
            splitcar = line.split("\t")
            splitspa = splitcar[2].split(" ")
            #print(splitspa)
            new_file.write(scaf+","+pos+","+splitcar[1]+","+splitspa[3]+","+splitspa[6]+spiltcar[3]) #TODO Confirm this works.
            #print(scaf+","+pos+","+splitcar[1]+","+splitspa[3]+","+splitspa[6].strip())
if __name__ == "__main__": #sets up a main area. This will not work well if imported
    main()
