'''Nailah Wade 2016'''
import sys, getopt
seq_read=open('p2dsuccess.fst')
nucs={'A':'U','C':'G','G':'C','U':'A', 'W':'W', 'S':'S', 'R':'Y', 'Y':'R', 'K':'M', 'M':'K', 'B':'V', 'D':'H', 'H':'D', 'V':'B', 'N':'N', 'X':'X'}
#anti_nucs=[, , , ]
altvs={'GCG':'GCC', 'UGC':'UGU', 'GAU':'GAC', 'GAA':'GAG', 'UUU':'UUC', 
'GGC':'GGU', 'CAU':'CAC', 'AUU':'AUC', 'AAA':'AAG', 'CUG':'UUG', 
'CGU':'CGC', 'CCG':'CCA', 'CAG':'CAA', 'CGU':'CGC', 'AGC':'UCU', 'ACC':'ACA', 
'GUG':'GUU', 'UAU':'UAC'}
matchscore={'A':2, 'C':4, 'G':4, 'U':2, 'W':2, 'S':4, 'R':3, 'Y':3, 'K':3, 'M':3, 'B':3, 'D':3, 'H':3,'V':3, 'N':3, 'X':0}


def complement(query):
	rev_query=''
	for i in range(len(query)):
		if query[i] in nucs:
			rev_query+=nucs[query[i]]
		else:
			rev_query+=query[i]

	return rev_query

def alternate(og_seq, start, window):
	codonstartposits=[]
	for mutsite in range(window):
		mut_site=start+mutsite
		if mut_site%3==0:
			mut_cdon=og_seq[mut_site:mut_site+3]
			if mut_cdon in altvs:
				codonstartposits.append(mut_site)
		

	if len(codonstartposits)==0:
		for unmutsite in range(window):
			unmut_site=start+unmutsite
			if unmut_site%3==0:
				unmut_cdon=og_seq[unmut_site:ummut_site+3]
				for a in altvs:
					if unmut_site== altvs[a]:
					codonstartposits.append(unmut_site)
	#make codonstartposits #skip those not in alts

	hiscore=0
	mod_pos=0

	for x in codonstartposits:
		codon_score=0
		for n in range(3):
			codon_score+=matchscore[og_seq[x+n]]
		if codon_score>hiscore:
			hiscore=codon_score
			mod_pos=x

	new_seq=og_seq[:mod_pos]+altvs[og_seq[mod_pos:mod_pos+3]]+og_seq[mod_pos+3:]

	if len(new_seq)!=len(og_seq):
		print "Something replaced wrong. The length of the new sequence is %u and the length of the old sequence is %u" %(len(new_seq), len(og_seq))
		print og_seq
		print new_seq
		sys.exit(1)
	print 'Success at', mod_pos, '!!!?\nold sequence\n', og_seq, '\nnew sequence:\n', new_seq

	return new_seq

def misprimer(seq, window, identity):
	#generate reverse
	unacceptable=identity*2*window
	rev_seq=complement(seq)


	worst_misprime=0
	for f_nt in range(len(seq)-window):
		for r_nt in reversed(range(window, len(rev_seq))):
			score=0
			for w_itr in range(window):
				if (seq[f_nt+w_itr]==nucs[rev_seq[r_nt-w_itr]]):
					try:
						score+=matchscore[seq[f_nt+w_itr]]
					except:
						print "Unknown character %c found, Program recognizes X as gaps." %(seq[f_nt+w_itr])
						sys.exit(1)
			if score>worst_misprime:
				worst_misprime=score
				worst_fwdpos=f_nt
				worst_revpos=r_nt
	if worst_misprime<unacceptable:
		#write seq to outfile
		print seq
		return "Misprimes Resolved"
	seq=alternate(seq, worst_fwdpos, window)

	return misprimer(seq, window, identity)




def demis_main():
	'''if len(argv)==0:
		argv.append('-h')
	try:
		opts, args=getopt.GetOpt(argv, "hi:l:")
	except getopt.GetoptError():
		print "\n\nUsage: NW_deMisprime.py -i <inputfile>"
		sys.exit()

	for opt, arg in opts:
		if opt=='-h':
			#help
			print "\n\nUsage: NW_deMisprime.py -i <inputfile>\n"
			print "HELP:\n<inputfile>: Nucleotide sequence file"
			print "<outputfile>: Output DNA sequence file in fasta or sequence format."
		sys.exit()
	if opt=='-i':
		try:
			seq=open(arg, 'w+')
		except IOError:
			print "\n\nCould not open input file. Please input valid file name in sequence format (.fst, .seq, etc.)"
			print "Usage: NW_deMisprime.py -i <inputfile> -l minimum length"
			sys.exit()
	if opt=='-l':
		if arg.isdigit():
				
		else:
			print "\n\nThe variable you entered was not a number. Please input an integer for minimum misprime length"
			print "Usage: NW_deMisprime.py -i <inputfile> -l minimum length"
			sys.exit()'''

	seq=''
	window=12
	identity=0.8
	for line in seq_read:
		if line[0]!='>':
			seq+=line
			
	seq=seq.replace('\n', '')
	print misprimer(seq, window, identity)
	print seq
	return 0

print demis_main()
'''
#new functions, structures:




'''