import sys
def main():
    test2()

def test2():
    file_list_3 = ["./intermeds/NVC_a_type0_CL_Galstep87_ON_DATA_22_86_FILT_GENES.txt","./intermeds/NVC_a_type0_CL_Galstep91_ON_DATA_22_90_FILT_GENES.txt","./intermeds/NVC_a_type0_CL_Galstep95_ON_DATA_22_94_FILT_GENES.txt","./intermeds/NVC_a_type1_OA_Galstep103_ON_DATA_22_102_FILT_GENES.txt","./intermeds/NVC_a_type1_OA_Galstep107_ON_DATA_22_106_FILT_GENES.txt","./intermeds/NVC_a_type1_OA_Galstep99_ON_DATA_22_98_FILT_GENES.txt"]
    pxl_name = "PXL_OUT.txt"
    ed_type = 'a'
    make_pxl("./intermeds/COMP_4.txt", file_list_3, pxl_name, ed_type)
    
def make_pxl(compOutput, genes, outpath, ed_type):
    compO = open(compOutput, 'r')
    new_file = open(outpath, 'x')
    ref = ""
    alt = ""
    if(ed_type =="a"):
        ref = "A"
        alt = "G"
    elif(ed_type=="c"):
        ref = "C"
        alt = "T"
    
    for line in compO:
        #print("Print attempting to find line\t"+line)
        l0 = line.split(' ')
        if len(l0) != 3:
            continue
            
        scafC = l0[0] #scaffold of comparison location
        posC = l0[1] #position of comparison location on scaffold
        giC =l0[2]
        #print('========POS C========')
        #print(posC)
        
        new_file.write(scafC + '\t' + posC+'\t'+giC) #Writes the scaffold and position to the PXL
        #print(scafC + '\t' + posC)
        
        for file in genes:
            print("checking file\t"+file)
            f = open(file, 'r')
            #print(f)
            for line1 in f:
                l1 = line1.split(' ')
                scafG = l1[0] # For matching to scafC
                posG = l1[1] #For matching to posC
                giG = l1[2] #Potentially fixed an error here
                if posG == 'A': #if it's not a full data line (format of gene has an enter in it beofre A and G counts)
                    continue #Unless some weirdness occurs in processing, this condition should never trigger. The comment to the left may be wrong.
                if posG == 'C':
                    continue #TODO See if this fixes the bug for only comp C runs.
                #print('=========POS G=======')
                #print(posG)

                if int(posC) == int(posG): #If the lines' posiitons do match: #TODO CONFIRM FIXES WORKED
                    #print('TRUE')
                    print("POS Match")
                    if scafC == scafG:    #If the lines' scaffolds do match:
                        #find out how to get name of a file (f) 
                        print("SCAF MATCH")
                        if giC==giG: #If the genes at the positions are the same
                            print("gi_s Match")
                            new_file.write('^' + '\t' + file + '\t' + next(f).strip()+'\t'+l0[-1].strip()+"\n") #TODO for some reason, a \n is being added by next(f). This is a problem, causes maek_pxl to bug out. tried to fix with .strip()
                            break #skips to the next file
                        #print('^' + '\t' + file + '\t' + next(f))
                        
 
def test1():
    line1 = "scaffold_0 12752558 ID=gene:FBgn0178973;Name=GM24109;biotype=protein_coding;gene_id=FBgn0178973;logic_name=flybase"
    l1 = line1.split(' ')

    print(l1)

    scafC = l1[0] #scaffold of comparison location
    posC = l1[1] #position of comparison location on scaffold
    giC =l1[2]
    print(scafC)
    print(posC)
    print(giC)


    line2 = "scaffold_0 12752558 ID=gene:FBgn0178973;Name=GM24109;biotype=protein_coding;gene_id=FBgn0178973;logic_name=flybase"
    l2 = line2.split(' ')
    print(l2)

    scafG = l2[0] #scaffold of comparison location
    posG = l2[1] #position of comparison location on scaffold
    giG =l2[2]
    print(scafG)
    print(posG)
    print(giG)

    if scafC == scafG:
        print("SCAF_OK")


    if posC == posG:
        print("POS_OK")

    if giC == giG:
        print("GI_OK")

    print(l1[-1])
    print(l2[-1])

main()