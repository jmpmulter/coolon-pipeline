#protein_seq_change.py
#takes the specific edits and their associated FBGN numbers.
# gets genomic sequence from FASTAs for before/after edits
#translates sequence and returns edited and unedited translates.

import sys
import os


#take the specific edit position, and the FBGN/GMNUM from unique Identifier
#use GMNUM/FBGN to get start/end of the genomic sequence
#find if the gene goes forward or backward
#find start and end points in FASTA, and edit point within this range
#If backward, do next steps with reverse complement
#store Unedited and edited transcript
#translate the transcripts
