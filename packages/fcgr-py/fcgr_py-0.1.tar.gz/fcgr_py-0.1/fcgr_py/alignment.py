from Bio import Align
import pandas as pd
import re

aligner = Align.PairwiseAligner()
aligner.match = 3
aligner.mismatch = -1
aligner.internal_open_gap_score = -1
aligner.internal_extend_gap_score = -1
aligner.left_gap_score = 0
aligner.right_gap_score = 0

def get_top_hit(input_seq, ref):
    '''Find best alignment given species'''
    
    pattern = "FCGR\d{1}[ABC]{0,1}"
    ref_pattern = "NM{1}_?[\.0-9]+"

    scores = []
    
    for refz in ref:
        score = aligner.score(refz.seq,input_seq)
        scores.append(score)
        
    best = scores.index(max(scores))
    align_id = ref[best].id
    ref_seq = re.search(ref_pattern, align_id)[0]
    top_hit = re.search(pattern, align_id)[0]
    if align_id[-18:] == "reverse_complement":
        reverse_complement = 1
    else:
        reverse_complement = 0  
    gap, gapless = get_identity_percents(input_seq, best, ref)
          
    out = [top_hit, ref_seq, reverse_complement, gap, gapless, best]
    return(out)  


def find_alignments(merged_seqs, human_ref, rhesus_ref):
    '''Get top hit for each sequence in preprocessed sequences'''
    
    alignments = []
    seq_names = []
    for row in merged_seqs.itertuples(index=False):
        species = getattr(row, "Species")
        if species == "RhM":
            ref = rhesus_ref
        if species == "Hu":
            ref = human_ref
        input_seq = getattr(row, "Sequence")
        seq_names.append(getattr(row, "Barcode"))
        alignments.append(get_top_hit(input_seq, ref))
    out = pd.DataFrame(alignments,columns = ["Top Hit", "Reference Sequence", "Reverse Complement", "Gapped Identity", "Gapless Identity", "Best"])
    out["Barcode"] = seq_names
    return(out)

def get_identity_percents(input_seq, best,ref):
    '''Find gapped and gapless identity percents given best alignment'''
    
    alignment = str(aligner.align(ref[best].seq, input_seq)[0])
    alignment = alignment.split("\n")[1]
    alignment = alignment.lstrip("-")
    alignment = alignment.rstrip("-")
    count = 0
    for char in alignment:
        if char == "|":
            count += 1
    gapped_ident=(count/len(alignment))
    gapped_ident = round(gapped_ident, 4)
    count = 0
    count2 = 0
    for char in alignment:
        if char == "|":
            count += 1
        if char == "X":
            count2 += 1
    gapless_ident=(count/(count+count2))
    gapless_ident = round(gapless_ident,4)
    return(gapped_ident, gapless_ident)


def merge_barcodes_alignments(merged, alignments_out, how="inner"):
    '''Merge alignments with barcode information'''
    
    out_full = pd.merge_ordered(merged, alignments_out, on="Barcode" )
    sp = out_full["Species"].tolist()
    th = out_full["Top Hit"].tolist()
    types = []
    for x, y in zip(th, sp):
        types.append(str(x+"_"+y))
    out_full["Types"] = types
    out_subset = out_full[["Barcode", "Num Reads", "Top Hit", "Reference Sequence", "Reverse Complement", "Gapped Identity", "Gapless Identity" ]]
 
    return(out_full, out_subset)

def get_alignment_output(merged_seq, human_ref, rhesus_ref, order_num, out_path, pool_num = 1):
    '''Perform all alignment functions and output alignment info in dataframe and output'''
    
    alignments_out = find_alignments(merged_seq, human_ref, rhesus_ref)
    print('Getting top hit for each sequence')

    out_full, out_subset = merge_barcodes_alignments(merged_seq, alignments_out)
    
    #out_name = str(order_num) + "_P" + str(pool_num) + "_" + "alignments.csv"
    
    #out_subset.to_csv(out_path 'output/'+ out_name, index = False )
    
    return(out_full)
    
    


    