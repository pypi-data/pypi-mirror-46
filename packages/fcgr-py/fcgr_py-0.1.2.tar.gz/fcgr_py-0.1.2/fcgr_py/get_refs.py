#!/usr/bin/env python

import re 
from Bio import SeqIO
from Bio.Alphabet import IUPAC


def get_human_ref(path = human_ref):
    '''Get reference sequences for humans then convert to uppercase (if not already) and get reverse complements'''
    
    from Bio import SeqIO, Seq
    import re
    
    human_refs_temp = list(SeqIO.parse(path, "fasta"))
    name_pattern = "FCGR.+$"
    
    human_refs = []
    for seqz in human_refs_temp:
        human_refs.append(seqz)
        seqz.seq = seqz.seq.upper()
        add = seqz.reverse_complement()
        add.id = seqz.id + "_reverse_complement"
        name_match = re.search(name_pattern, seqz.name)[0]
        seqz.name= name_match + "_Hu"
        add.name = name_match + "_Hu"
        human_refs.append(add)
        
    return(human_refs)
        
        
def get_rhesus_ref(path = rhesus_ref):
    '''Get reference sequences for rhesus then convert to uppercase (if not already) and get reverse complements'''
    
    from Bio import SeqIO, Seq
    import re

    rhesus_refs_temp = list(SeqIO.parse(path, "fasta"))
    name_pattern = "FCGR.+$"
    
    rhesus_refs = []
    for seqz in rhesus_refs_temp:
        rhesus_refs.append(seqz)
        seqz.seq = seqz.seq.upper()
        add = seqz.reverse_complement()
        add.id = seqz.id + "_reverse_complement"
        name_match = re.search(name_pattern, seqz.name)[0]
        seqz.name = name_match + "_RhM"
        add.name = name_match + "_RhM"
        rhesus_refs.append(add)
    
    return(rhesus_refs)



