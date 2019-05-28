


# Sam Linde, Lauren Connoly, Jake Multer 10/16/18
# need to figure out how to feed files into eachother - like output of vcf_filt into find_gene etc.. 
# added self to 
# python3 <file.vcf> <file.gff3> <A/C> 

class Edit():

	def __init__(self, vcf, gff3, edit_type):
		self.vcf = vcf
		self.gff3 = gff3
		self.edit_type = 'A'

	def vcf_filter1(self, vcf, filter_vcf, edit_type):
	    try:
	        new_file = open(filter_vcf, 'x')
	        open_vcf = open(self.vcf, 'r')
	        open_vcf.seek(0)
	        
	        for line in open_vcf:
	            vcf_line = line.split('\t')
	            if self.edit_type = 'A':
	            	if "#" in line or vcf_line[0] == '/n' or vcf_line[3] != 'A' or vcf_line[4] != 'G':
	                	continue
	            if self.edit_type == 'C':
	            	if '#' in line or vcf_line[0] == '/n' or vcf_line[3] != 'C' or vcf_line[4] != 'T':
	            		continue 
	        
	            n1 = vcf_line[9].split(':')[-1]
	            n2 = n1.split(',')[0:-1]
	            numA = 0
	            numG = 0
	            for x in n2:
	                num = int(x.split('=')[-1])
	                if 'A' in x or 'C' in x:
	                    numA += num
	                elif 'G' in x or 'T' in x:
	                    numG += num
	                else:
	                    print("WRONG BASE SOMETHING WRONG AHHH")
	            
	            new_file.write(line + '\t' + ':A=' + str(numA) + ',' + 'G=' + str(numG) + ',' + '\n')
	            #print(line + '\t' + ':A=' + str(numA) + ',' + 'G=' + str(numG) + ',' + '\n')
	            
	    except FileExistsError:
	        print(vcf + filter_vcf + ' already exists')



	def gff3_filter(self, gff3, filter_gff3):
	    try:
	        new_file = open(filter_gff3, 'x')
	        open_gff3 = open(self.gff3, 'r')
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


	def find_gene(self, vcf, gff3, outpath):
	        try:
	                new_file= open(outpath, 'x')
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

	                return new_file
	                
	        except FileExistsError:
	                print('the file ' + file + ' already exist')




	def comp_gene(self, f0, f1, out_path):
	        new_file = open(outpath, 'x')
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


	def make_pxl(self, compOutput, genes, outpath):
	    compO = open(compOutput, 'r')
	    new_file = open(outpath, 'x')
	    
	    for line in compO:
	        #print(line)
	        l = line.split(' ')
	        if len(l) != 2:
	            continue
	            
	        scafC = l[0]
	        posC = l[1]
	        #print('========POS C========')
	        #print(posC)
	        
	        new_file.write(scafC + '\t' + posC)
	        #print(scafC + '\t' + posC)
	        
	        for file in genes:
	            f = open(file, 'r')
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
	                        new_file.write('^' + '\t' + file + '\t' + next(f))
	                        #print('^' + '\t' + file + '\t' + next(f))


	    def main():
	    	vcf = sys.argv[1]
	    	gff3 = sys.argv[2]
	    	edit_type = sys.argv[3]

	    	edit = Edit(vcf, gff3, edit_type)

	    if __name__ = '__main__':
	    	main()

