'''NW_prf2dna Nailah Wade 2016.Takes in profile file, looks for profile information. gatheres represented amino acids at each postions in the sequence
based on rate of occurance and obtains corresponding codon from E.coli codon usage table. Codons are then added to final DNA sequence that
signifies the variability in the protein sequences given'''

import sys, getopt

ueorder=['R', 'L', 'S', 'T', 'P', 'A', 'G', 'V','K', 'N', 'G', 'H', 'E', 'D',
'Y', 'C', 'F', 'I', 'M', 'W', ]
aa_cdns={'A':['GCA', 'GCC', 'GCU'], 'C':['UGC'], 'D':['GAU'], 'E':['GAA'], 'F':['UUU'],
'G':['GGC'], 'H':['CAU'], 'I':['AUU'], 'K':['AAA'], 'L':['CUG'], 'M':['AUG'],
'N':['CGU'], 'P':['CCG'], 'Q':['CAG'], 'R':['CGU'], 'S':['AGC'], 'T':['ACC'],
'V':['GUG'], 'W':['UGG'], 'Y':['UAU'], 'X':['XXX']}

aa_cdns2={'A':'GCG', 'C':'UGC', 'D':'GAU', 'E':'GAA', 'F':'UUU',
'G':'GGC', 'H':'CAU', 'I':'AUU', 'K':'AAA', 'L':'CUG', 'M':'AUG',
'N':'CGU', 'P':'CCG', 'Q':'CAG', 'R':'CGU', 'S':'AGC', 'T':'ACC',
'V':'GUG', 'W':'UGG', 'Y':'UAU', 'X':'XXX'}

degen_ntkey={'A':'A', 'C':'C', 'G':'G', 'U':'U', 'AC':'M', 'AG':'R',
'AU':'W', 'CG':'S', 'CU':'Y', 'GU':'K', 'ACG':'V', 'ACU':'H', 'AGU':'D',
'CGU':'B', 'ACGU':'N'}

poss_aas="start"
start= False
cutoff=0.00001



def find_poss_aas(prf_line):
	poss_aas=""
	if (prf_line[0]).isalpha():
		poss_aas='X'
	else:
		for prbs in range(20):
			if float(prf_line[prbs]) >cutoff:
				aa_list=aa_cdns2.keys()
				#list(aa_list)
				aa_list.sort()
				aa_list.remove('X')
				poss_aas+=aa_list[prbs]
				#print prbs
	#print aa_list
	return poss_aas

place=0
def make_codon(repped_aa):
	codon=""
	if len(repped_aa)==1:
		#get preferred codon from dictionary
		codon=repped_aa
	else:
		#create degenerate cdn from aa list
		for it_r in range(3):
			# For each aa collect preferred nt and add to collection if
			#not already there
			nts=""
			for aa in repped_aa:

				if aa_cdns2[aa][it_r] not in nts:
					nts+=aa_cdns2[aa][it_r]
			nts=''.join(sorted(nts))
			nts= nts.replace('X', '')
			codon+=degen_ntkey[nts]
		codon='['+codon+']'
	return codon


def prf2dna(argv):
	#arg l
	if len(argv)==0:
		argv.append('-h')
	##read prf (one res perline)
	#usage line, throws exception
	try:
		opts, args= getopt.getopt(argv, "hi:o:")
	except getopt.GetoptError:
			print "\n\nUsage: NW_prf2dna.py -i <inputfile> -o <outputfile>"
			sys.exit()

	for opt, arg in opts:
		if opt=='-h':
			#help
			print "\n\nUsage: NW_prf2dna.py -i <inputfile> -o <outputfile>\n"
			print "HELP:\n<inputfile>: Input profile file with .prf suffix."
			print "<outputfile>: Output DNA sequence file in fasta or sequence format."
			sys.exit()
		if opt=='-i':
			try:
				prf=open(arg)
			except IOError:
				print "\n\nCould not open input file. Please input valid file name in profile format (.prf)"
				print "Usage: NW_prf2dna.py -i <inputfile> -o <outputfile>"
				sys.exit()
		if opt=='-o':
			try:
				out_file=open(arg, "w")
			except IOError:
				print "\n\nCould not open output file. Please input valid file name in sequence format (.fst, .seq, etc.)"
				print "Usage: NW_prf2dna.py -i <inputfile> -o <outputfile>"
				sys.exit()



	degen_seq=""
	aa_seq=''
	start=False
	for line in prf:
		if "PROFILE:" in line:
			start=True
			out_file.write('>\n')
			continue
		if start==True:
			line=line.split()
			poss_aas=find_poss_aas(line[2:])
			aa_seq+=line[1]+'  '
			degen_seq+=make_codon(poss_aas)
		#make ending profile? -->expasy translate confirmation

	tag="tag"
	for tab in range(len(degen_seq)):
		#print degen_seq[tab]
		if tag!="\n#nucleotide\n" and degen_seq[tab]=='[':
			tag="\n#nucleotide\n"
			out_file.write(tag+degen_seq[tab+1:tab+4])
			tab+=5
		elif tag!="\n#protein\n"  and degen_seq[tab]!='[':
			tag="\n#protein\n"
			out_file.write(tag+degen_seq[tab])

		elif degen_seq[tab]=='[':
			out_file.write(degen_seq[tab+1:tab+4])
			tab+=5
		else:
			out_file.write(degen_seq[tab])
	out_file.close()
	return 0

if __name__=="__main__":
	prf2dna(sys.argv[1:])
