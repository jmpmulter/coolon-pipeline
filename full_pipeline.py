import sys
import re
#import pandas as pd
#import numpy as np
#from functools import reduce
#from pandas import ExcelWriter
#from pandas import ExcelFile
#import matplotlib.pyplot as plt
#from scipy.stats import ttest_ind 

def vcf_filter1(vcf, filter_vcf):
    try:
        new_file = open(filter_vcf, 'x')
        open_vcf = open(vcf, 'r')
        open_vcf.seek(0)
        
        for line in open_vcf:
            vcf_line = line.split('\t')
            if "#" in line or vcf_line[0] == '/n' or vcf_line[3] != 'A' or vcf_line[4] != 'G':
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
            #print(line + '\t' + ':A=' + str(numA) + ',' + 'G=' + str(numG) + ',' + '\n')
                
            #print(n2)
    
    except FileExistsError:
        print(vcf + filter_vcf + ' already exists')

#vcf_filter1('C1.vcf','C1_filtered.txt')
#vcf_filter1('C2.vcf','C2_filtered.txt')
#vcf_filter1('C3.vcf','C3_filtered.txt')
#vcf_filter1('HA1.vcf','HA1_filtered.txt')
#vcf_filter1('HA2.vcf','HA2_filtered.txt')
#vcf_filter1('HA3.vcf','HA3_filtered.txt')

def vcf_filter(vcf, filter_vcf): try: new_file = open(filter_vcf, 'x') open_vcf = open(vcf, 'r') open_vcf.seek(0)

    for line in open_vcf:
        vcf_line = line.split('\t')
        if "#" in line:
            continue
        if vcf_line[0] == '\n':
            continue
        n1 = vcf_line[9].split(',')
        n2 = n1[0].split(':')[3] + n1[1] #this has the form 'A=*G=*'
        n3 = list(map(str, n2))
        if n3[-1] == '\n': #gets rid of \n on the end
            del n3[-1]
        i=0
        while(i < len(n3)):             
            if n3[i] == '=':
                del n3[i]
                i = i - 1 
            i = i + 1
        #print(n3)
        j = 1
        numRef = ''
        numAlt = ''
        if n3[0] == 'A': #this grabs the number of ref
            while(n3[j] != 'G'):
                numRef = numRef + n3[j] 
                j = j+1
            #print('A=',numRef)
        if n3[j] == 'G':
            j = j + 1 
            while(j < len(n3)): #this grabs the number of alt
                numAlt = numAlt + n3[j]
                j = j + 1
            #print('G=', numAlt)

        if numRef != '' and ((int(numRef) + int(numAlt)) > 10):
            new_file.write(line)
    open_vcf.seek(0)
    new_file.close()
    open_vcf.close()


except FileExistsError:
    print('the file ' + filter_vcf + ' already exists')
	

#u = unfiltered, f = filtered

#vcf_filter('Galaxy124u.txt', 'Galaxt124f.txt')

#vcf_filter('Galaxy125u.txt', 'Galaxy125f.txt')

#vcf_filter('Galaxy126u.txt', 'Galaxy126f.txt')

#vcf_filter('Galaxy127u.txt', 'Galaxy127f.txt')

#vcf_filter('Galaxy128u.txt', 'Galaxy128f.txt')

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
                    count_a_to_g = count_a_to_g + 1  
        

    print ("Number of A-to-I Editing Sites is:", count_a_to_g)
#count('data.vcf')

#count('C1_filtered.txt')
#count('C2_filtered.txt')
#count('C3_filtered.txt')
#count('HA1_filtered.txt')
#count('HA2_filtered.txt')
#count('HA3_filtered.txt')

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

'''takes the result of vcf_filter and gff3_filter
find_gene(vcf, gff3, file) takes a vcf file, a gff3 file and an out path (what you want your new file to be named) 
and will return a new file with the scaffold, vcf position and the gene ID. (can add more things by adding to line 38). 
must input the files into the function in this order or it will not work.'''

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
                                                new_file.write(vcf_scaffold + ' ' + vcf_pos + ' ' + gff3_id + ' ' +
                                                               'A = ' + num0[1] + ' G = ' + num1[1] + '\n')
                        open_gff3.seek(0) #stackoverflow told me to do this and it worked.. resets the cursor 
                                          #to the first for loop.. 
                        
                new_file.close()
                open_vcf.close()
                open_gff3.close()
                
        except FileExistsError:
                print('the file ' + file + ' already exist')

                
#find_gene('C1_filtered.txt','filt_dsechellia.gff3','C1_genes.txt')
#find_gene('C2_filtered.txt','filt_dsechellia.gff3','C2_genes.txt')
#find_gene('C3_filtered.txt','filt_dsechellia.gff3','C3_genes.txt')
#find_gene('HA1_filtered.txt','filt_dsechellia.gff3','HA1_genes.txt') 
#find_gene('HA2_filtered.txt','filt_dsechellia.gff3','HA2_genes.txt') 
#find_gene('HA3_filtered.txt','filt_dsechellia.gff3','HA3_genes.txt') 

'''comp_genes(f0, f1, new_file) = new_file with the SNPs that are
common to both f0 and f1'''


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
    #new_file = open(outpath, 'x')
    
    for line in compO:
        #print(line)
        l = line.split(' ')
        if len(l) != 2:
            continue
            
        scafC = l[0]
        posC = l[1]
        #print('========POS C========')
        #print(posC)
        
        #new_file.write(scafC + '\t' + posC)
        #print(scafC + '\t' + posC)
        
        for file in genes:
            f = open(file, 'r')
            print(f)
            for line0 in f:
                l0 = line0.split(' ')
                #print(l0)
                #print(l0)
                scafG = l0[0]
                posG = l0[1]
                if posG == 'A':
                    continue
                #print('=========POS G=======')
                #print(posG)
                
            
                
                if int(posC) == int(posG):
                    #print('TRUE')
                    if scafC == scafG:    
                        #find out how to get name of a file (f) 
                        #new_file.write('^' + '\t' + file + '\t' + next(f))
                        print('^' + '\t' + file + '\t' + next(f))
              
                        
genes = ['NVC_CL1_Galaxy29_genes.txt', 'NVC_CL2_Galaxy30_genes.txt', 'NVC_CL3_Galaxy31_genes.txt','NVC_OA1_Galaxy32_genes.txt','NVC_OA2_Galaxy33_genes.txt', 'NVC_OA3_Galaxy34_genes.txt']
make_pxl('compFinal.txt', genes, 'pxl.txt')

def makeCSV(pxl,outpath):
    pxl = open(pxl, 'r')
    new_file = open(outpath, 'x')
    new_file.write("Scaffold,Position,RunFileName,Ref,Alt\n")
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
            new_file.write(scaf+","+pos+","+splitcar[1]+","+splitspa[3]+","+splitspa[6])
            #print(scaf+","+pos+","+splitcar[1]+","+splitspa[3]+","+splitspa[6].strip())
         
            
makeCSV("pxl1.txt","csvOUT1.csv")
