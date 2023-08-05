#!/usr/bin/python

import pandas as pd
import numpy as np
from fcgr_py import alignment
from fcgr_py import preprocessing
from fcgr_py import get_refs 
from fcgr_py import postprocessing
from fcgr_py import variation
import os 
import subprocess

def fcgr_pipeline(input_dir, fastq_name, output_dir, order_num, pool_num=1, barcode_names = 'barcode_names.txt', threshold = .99, rhesus_ref, human_ref):
    '''Put all pipeline steps together'''
    
    subprocess.run(['mkdir', output_dir + '/output' ], check = False)
    subprocess.run(['mkdir', output_dir + '/output/fasta_output/'], check = False)
    subprocess.run(['mkdir', output_dir + '/output/alignments/'], check = False)
    subprocess.run(['mkdir', output_dir + '/output/excluded/'], check = False)
    
    pre_df = preprocessing.barcode_preprocessing(input_dir + barcode_names, input_dir + fastq_name, order_num=order_num)
    
    human_ref = get_refs.get_human_ref(human_ref)
    rhesus_ref = get_refs.get_rhesus_ref(rhesus_ref)
    
    out_full= alignment.get_alignment_output(pre_df, human_ref, rhesus_ref, order_num = order_num, out_path = output_dir)
    
    postprocessing.get_fasta_output(out_full, human_ref, rhesus_ref, output_dir)
    postprocessing.trim(out_full, output_dir)
    out_trim_trans=postprocessing.trim_translate(out_full, output_dir)
    
    out_trim_trans = variation.get_nt_subs(out_trim_trans,output_dir)
    out_trim_trans = variation.get_aa_subs(out_trim_trans, output_dir)
    
    out_trim_trans = variation.get_AA_read_lengths(out_trim_trans, output_dir)
    out_trim_trans = variation.get_NT_read_lengths(out_trim_trans, output_dir)
    
    postprocessing.final_output(out_trim_trans, output_dir, order_num, pool_num)
    
    subprocess.run(['rm', '-r', output_dir + 'output/temp/'], check = False)
    
    