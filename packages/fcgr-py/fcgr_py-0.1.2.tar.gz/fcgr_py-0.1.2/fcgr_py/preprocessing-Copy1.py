#!/usr/bin/env python

import pandas as pd
import re 
from Bio import SeqIO

def get_barcode_info(barcode_file):
    '''Get information for barcode, species, PTID from barcode_names.txt file'''

    pool = pd.read_csv(barcode_file, sep='\t')
    barcodes_temp = pool["Oligo name"].tolist()
    
    PTIDs = pool["PTID"].tolist()
    
    barcodes = []
    species = []
    primers = []
    
    for code in barcodes_temp:
        s = str(code)
        
        barcodes_pattern = "\d{4}"
        barcodes_pattern = re.compile(barcodes_pattern)
        barcodes_match = re.search(barcodes_pattern,s)[0]
        barcodes.append(barcodes_match)
    
        species_pattern = "RhM{1}|Hu{1}"
        species_pattern = re.compile(species_pattern)
        species_match = re.search(species_pattern, s)[0]
        species.append(species_match)
    
        primer_pattern = "FCGR\d{1}[ABC_\s\.\d]+$"
        primer_pattern = re.compile(primer_pattern)
        primer_match = re.search(primer_pattern, s)[0]
        primer_match = primer_match.rstrip(' ')
        primer_match = re.sub('[_\s]+', 'v', primer_match)
        primer_match = primer_match.replace('.', '')
        primers.append(primer_match)
           
    barcodes = pd.DataFrame({"Species":species, 'PTID':PTIDs, "Barcode":barcodes, "Primer":primers})
    barcodes = barcodes.drop_duplicates(subset = "Barcode", keep='first')
    
    return(barcodes)

def get_seqs(seq_in, format="fastq"):
    '''Get sequence information to match with barcode, species, PTID info from fastq file'''
    
    seqs_temp = list(SeqIO.parse(seq_in, format))
    seq_barcodes = []
    seqs = []
    cluster = []
    phase = []
    num_reads = []
    
    for seqz in seqs_temp:
        
        match = re.search('\d{4}',seqz.id)
        seq_barcodes.append(match[0])
        seqs.append(str(seqz.seq))
    
        match_cluster = re.search('Cluster\d', seqz.id)[0]
        match_cluster2 = re.search('\d{1}', match_cluster)[0]
        cluster.append(match_cluster2)
    
        match_phase = re.search('Phase\d', seqz.id)[0]
        match_phase2 = re.search('\d+', match_phase)[0]
        phase.append(match_phase2)
    
        match_numreads = re.search('NumReads\d+', seqz.id)[0]
        match_numreads2 = re.search('\d+', match_numreads)[0]
        num_reads.append(match_numreads2) 
    
    seq_barcodes = pd.DataFrame({"Barcode":seq_barcodes, "Cluster":cluster, "Phase":phase, "Num Reads":num_reads, "Sequence": seqs})
    return(seq_barcodes)
    

def merge_barcodes(barcodes, seq_barcodes, order_num, pool_num):
    '''Combine barcode information with fastq information'''

    
    merged = pd.merge_ordered(barcodes, seq_barcodes,how="inner", on="Barcode")
    m_species = merged["Species"].tolist()
    m_PTID = merged["PTID"].tolist()
    m_barcode = merged["Barcode"].tolist()
    m_primer = merged["Primer"].tolist()
    m_cluster = merged["Cluster"].tolist()
    m_phase = merged["Phase"].tolist()

    new_barcodes = []
    for sp, ptid, bc, prm, cl, ph in zip(m_species, m_PTID, m_barcode, m_primer, m_cluster, m_phase):
        nb = str(order_num) + "_" + str(sp)+"_"+str(ptid)+"_P"+ str(pool_num) +'_'+str(bc)+"_"+str(prm)+"_C"+str(cl) + "_P" + str(ph)
        new_barcodes.append(nb)

    merged['Barcode'] = new_barcodes
    merged = merged[["Barcode", "Species", "Num Reads", "Sequence"]]

    return(merged)

def barcode_preprocessing(barcode_file, fastq_file, order_num, pool_num=1, format='fastq'):
    '''Peforms all preprocessing functions to output one dataframe with barcode and sequence info'''
    
    barcodes = get_barcode_info(barcode_file)
    print('Getting barcode information from ' + barcode_file)
    seq_barcodes = get_seqs(fastq_file, format)
    print('Getting sequences from ' + fastq_file)
    merged = merge_barcodes(barcodes, seq_barcodes, order_num, pool_num)
    print('Merging barcode and sequence information')
    
    return(merged)
