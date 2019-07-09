#Isolate_heatmap_FBgn
#Load in Heatmap
#Isolate FBGNs, GM_num, place at end of line,
#format header to be ready for excel heatmaps
import sys
import os
def main():
    inpath = ""
    outpath = ""
    inpath = sys.argv[1]
    outpath = sys.argv[2]
    
    #print(sys.argv)
    
    if ((inpath=="")or(outpath == "")):
        print("inpath or outpath not entered. Aborting program")
        sys.exit()
    f_in = open(inpath,"r")
    f_out = open(outpath,"w")
    
    f_in.seek(0)
    header = f_in.readline().strip()
    #NOTE- changed group definitions below
    grp_toxins =["OA","HA","NONI","OAHA"] 
    grp_fruit = ["FIG","LDOPA"]

    columns = align_columns(header,grp_toxins,grp_fruit)
    searcher = set_searcher(columns)
    header+=",Sig Hits,Non-Sig Hits,Total Hits,Total Omits,Dmel Ortholog,FBgn_num,GM_num,COLR,Reason\n"
    f_out.write(header)
    
    gm_num = ""
    FBgn = ""
    id_split = ""
    for ln in f_in:
        lns = ln.split(",")
        for item in lns:
            if "FBgn" in item:
                id_split = item.split("_")
                break
        try:
            for i in range(0,len(id_split)):
                if "FBgn" in id_split[i]:
                    FBgn = id_split[i]
                    gm_num = id_split[i+1].split("\"")[0]
                    break
            color = choose_color(ln,searcher,columns)
            f_out.write(ln.strip()+",,,,,,"+FBgn+","+gm_num+","+color[0]+","+color[1]+"\n")
        except(IndexError):
            print("Error: GM_num format is likely non-standard. skipping this line")
            color = choose_color(ln,searcher,columns)
            f_out.write(ln+",,,,,,,,"+color[0]+","+color[1]+"\n")
            #skip to the next line in f_in #this should happen automatically
        
    f_in.close()
    f_out.close()
    
    
#Scaf_num_Pos_Fbgn_Gmnum,F0_CL_vs_FIG,F1_CL_vs_HA,F2_CL_vs_LDOPA,F3_CL_vs_NONI,F4_CL_vs_OAHA,F5_CL_vs_OA,F6_CL,F7_DSECH,Sig Hitts,Non-Sig Hits,Total Hits,Total Omits,Dmel Ortholog,FBgn_num,GM_num,COLR



def set_searcher(columns): #Searcher format: [[fruit list[index,label]],[toxin list[index,label]]]
    output = [[],[]]
    for item in columns:
        if(item[2]==0): #Fruit
            output[0].append([item[0],item[1]])
        elif(item[2]==1): #Toxin
            output[1].append([item[0],item[1]])
        else:
            print("ERROR IN TYPEING -- More than 2 types")
    return output
            
    

def choose_color(ln,searcher,columns):
    by_grps = process_line(searcher,ln) #Expected format: [["N","O"],["S","S","N","O"]]
    
    is_red = red_test(by_grps)#(TRUE/FALSE, "reason if TRUE, NA if False")
    if is_red[0] == True:
        return ("red",is_red[1])
    is_green = green_test(by_grps)
    if is_green[0]==True:
        return ("green",is_green[1])
    is_yellow = yellow_test(by_grps)
    if is_yellow[0]==True:
        return ("yellow",is_yellow[1])
    #if nothing else works    
    return(("white","Else_logic"))
    #is it green?
        #all same in groups, but groups are different from each other
        #all same in groups (w/ 1 variability), but groups are different from each other
        
    #is it yellow?
        #all same in groups (w/ 2 variability), but groups are different from each other. 1 different in group 1/
    #is it red?
        #everything is the same
        #all the same, with 1 omit
    #is it white?
        #everything leftover
    
    
def align_columns(header,grp_toxins,grp_fruit):
    columns = []
    hs = header.split(",")
    for i in range(0,len(hs)):
        for thing in grp_fruit:
            if thing in hs[i].strip():
                columns.append((i,item,0))
        for item in grp_toxins:
            if item in hs[i].strip():
                columns.append((i,item,1)) #(index,item_at_index,group#) #0 = nontoxin, 1=toxin
    return columns  
def process_line(searcher,ln):
    by_grps = [[],[]]
    lns = ln.split(",")
    for i in range(0,len(searcher)):
        for item in searcher[i]:
            by_grps[i].append(lns[item[0]])
    return by_grps
    
def red_test(by_grps):
    red = False
    reason = "NA"
    all_same = r_same_test(by_grps)
    if(all_same):
        red = True
        reason = "r_same_test positive - all reads are the same"
    all_same_less_1 = r_same_less1_test(by_grps)
    if(all_same_less_1):
        red = True
        reason = "r_same_less1_test positive - all reads same with one deviance"    
    return((red,reason))

def r_same_test(by_grps):
    first_letter = by_grps[0][0]
    for i in range(0,len(by_grps)):
        for item in by_grps[i]:
            if item ==first_letter:
                pass
            else:
                print("False response for r_same_test: at least 1 entry different from others")
                return False
    print("True response for r_same_test: all target entries are the same")
    return True
def r_same_less1_test(by_grps):
    first_letter = by_grps[0][0]
    num_deviations = 0
    responses = ["S","N","O"]
    for resp in responses:
        deviancy = 0
        for grp in by_grps:
            for item in grp:
                if item == resp:
                    pass
                else:
                    deviancy+=1
                    if(deviancy>1):
                        break
        if deviancy ==1:
            print("True response for r_same_less1_test- all same with one exception")
            return True
    print("False response for r_same_less1_test- more than 1 difference for all possible responses")
    return False
    #for item in responses:
        #see if all same with maximum 1 deviancy
        #if deviancy >1, try next letter
        #if deviancy==1 for any, return True at that point.
        #else return false
def green_test(by_grps):
    green = False
    reason = "NA"
    
    grps_diff_itnl_cons = g_ideal(by_grps)
    if(grps_diff_itnl_cons):
        green=True
        reason = "Ideal diff pattern"
    
    grps_diff_1_deviance = g_ideal_1_dev(by_grps)
    if(grps_diff_1_deviance):
        green = True
        reason = "Ideal diff pattern with 1 deviance"    
    return((green,reason))
def g_ideal(by_grps):
    grp_vals = ["",""]
    for i in range(0,len(by_grps)):
        grp_vals[i] = by_grps[i][0]
    if grp_vals[0]==grp_vals[1]:
        print("initial grp_vals are the same, therefore cannot be fully different")
        return False
    else:
        for i in range(0,len(by_grps)):
            for item in by_grps[i]:
                if item == grp_vals[i]:
                    pass
                else:
                    print("Groups vary internally, g_ideal test failed")
                    return False
                    
        print("Groups are internally consistent, g_ideal test passed")
        return True
            #look at each value in each group to see if it matches the grp_vals value for the group:
            #if yes pass, if no print message and return False.
            #if it gets to the end and it has passed, print message and return True
def g_ideal_1_dev(by_grps):
    is_condition = False
    t1 = g_majority_1_dev(by_grps)
    t2 = g_minority_1_dev(by_grps) 
    if(t1):
        print("True Groups are mostly internally consistent, variance in Toxin")
        return True
    if(t2):
        print("True Groups are mostly internally consistent, variance in Fruit")
        return True
    else:
        print("False groups are not consistent enough to pass ideal with 1 deviance")
        return False
    
    #inconsist_bigger
    #inconsist_smaller
    
def g_majority_1_dev(by_grps):
    if by_grps[0][0] != by_grps[0][1]:
        print("Failed g_1dev_t1 -- no small group consistency")
        return False
    
    cts = 0
    ctn = 0
    cto = 0
    majority = ""
    
    for item in by_grps[1]:
        if item=="S":
            cts+=1
        if item=="N":
            ctn+=1    
        if item=="O":
            cto+=1
    if(cts or ctn or cto ==3):
        pass
    else:
        print("Failed g_1dev_t1 -- no majority of large group")
        return False
    if(cts>ctn and cts>cto):
        majority = "S"
    if(cto>ctn and cto>cts):
        majority = "O"
    if(ctn>cts and ctn>cto):
        majority = "N"
    if majority == by_grps[0][0]:
        print("Faield g_1dev_t1 -- small group and large group majority are the same")
        return False
    print("Confirmed g_1dev_t1 -- small group and large group majority are different")
    return True
    
    #Find majority of larger block
        #exit if no majority -1
    #Find makeup of smaller block:
        #if inconsistency, exit


def g_minority_1_dev(by_grps):
"""Passed if large group is fully consistent, and both small group items are different to each other and the large group letter
    Examples:
    Large - all S, small O,N -> TRUE
    Large - all S, small S,N -> False
    Large - all S, small N,N -> False
    
    This behavior is because the second test case is already picked up by Red test, and I want to avoid confilcts of these labels.
    The third case is because this is already picked up by the first green test.
"""
    if by_grps[0][0]==by_grps[0][1]:
        print("Failed g_1dev_t2 -- small groups match")
        return False
    
    big_cts = 0
    big_ctn = 0
    big_cto = 0
    big_letter= ""
    
    for item in by_grps[1]:
        if item=="S":
            cts+=1
        if item=="N":
            ctn+=1    
        if item=="O":
            cto+=1
    if(cts or ctn or cto ==4):
        pass
    else:
        print("Failed g_1dev_t2 -- no large group consistency")
        return False
    
    if(cts==4):
        big_letter = "S"
    if(cto==4):
        big_letter = "O"
    if(ctn == 4):
        big_letter = "N"
    
    for item in by_grps[0]:
        if(item==big_letter):
            print("Faield g_1dev_t2 -- a small group member and large group letter are the same")
            return False
    print("Confirmed g_1dev_t2 -- small group with 1 deviancy and large group are different")
    return True 

def yellow_test(by_grps):
    yellow = False
    reason = "NA"
    t1 = y_minority_con_majority_211(by_grps)
    t2 = y_minority_con_majority_220(by_grps)
    t3 = y_minority_11_majority_310(by_grps)
    #True conditions:
        #small consistent, large has 2 consistent and 1 and 1
        #small consistent, large has 2 consistent and 2 consistent. -> automatically mark as yellow, regardless of pattern
        #small has 1 deviancy, large has 3 consistent
        
        
    
if __name__ == "__main__":
    #print("running program")
    main()