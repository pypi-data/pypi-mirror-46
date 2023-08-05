from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Align.Applications import MafftCommandline
import numpy as np
import pandas as pd

def get_types(data_frame_in):
    '''Gets species and FCGR combination present in dataset for later output'''
    
    types = list(set(data_frame_in["Types"].tolist()))
    
    return(types)


def get_fasta_output(data_frame_in, human_ref, rhesus_ref, output_dir, threshold = .99):
    '''Filters and writes fasta and mafft fasta/txt file for each species and FCGR combination'''

    data_frame_in["Excluded?"] = np.where(data_frame_in['Gapless Identity']< threshold, "NT Gapless Identity < " + str(threshold), '')
    filtered = data_frame_in[data_frame_in["Gapless Identity"]>=threshold]
    
    types = list(set(filtered["Types"].tolist()))
    
    # fasta output - not aligned
    for hit in types:
        if hit[-2:] =="hM":
            ref = rhesus_ref
        else:
            ref = human_ref
        ref_seqs_fasta = []
        for seqzz in ref[:int(len(ref)):2]:
            if seqzz.name == hit:
                ref_seqs_fasta.append(seqzz)

        type_subset = filtered[filtered["Types"]==hit]
        barcodes = list(type_subset["Barcode"])
        seqs = list(type_subset["Sequence"])
        rev_comp = list(type_subset["Reverse Complement"])
        ref_seq = list(type_subset["Reference Sequence"])
        seq_records = []
        for codes, seqz, revs, refz in zip(barcodes, seqs, rev_comp, ref_seq):
            seq_string= str(seqz)
            if revs ==1:
                rc = "RevComp "
                seq1 = Seq(seq_string)
                seq1 = seq1.reverse_complement()
            else:
                rc = ""
                seq1 = Seq(seq_string)
            seq_rec = SeqRecord(seq1, id = codes, description = str(rc+refz))
            seq_records.append(seq_rec)
        fasta_out = ref_seqs_fasta + seq_records
        name = hit + "_nt.fasta"
        out= output_dir + 'output/fasta_output/' +  name
        SeqIO.write(fasta_out, out, "fasta")
        print('Writing ' + name + ' to ' + output_dir + 'output/fasta_output/')
        
        # mafft fasta output - aligned
        in_file=out
        mafft_exe="/usr/local/bin/mafft"
        mafft_cline = MafftCommandline(mafft_exe,input=in_file, nuc=True, namelength=40)
        stdout, stderr = mafft_cline()
        mafft_name =  hit + "_nt_mafft.fasta"
        out_file = output_dir + 'output/fasta_output/' + mafft_name
        with open(out_file, "w") as handle:
            handle.write(stdout)
        print('Writing ' + mafft_name +' to '+ output_dir + 'output/fasta_output/')
            
        # MAFFT/clustalw output - aligned
        in_file=out
        mafft_exe="/usr/local/bin/mafft"
        mafft_cline = MafftCommandline(mafft_exe,input=in_file, nuc=True, namelength=40, clustalout=True)
        stdout, stderr = mafft_cline()
        mafft_name =  hit + "_nt.txt"
        out_file = output_dir + 'output/alignments/' + mafft_name
        with open(out_file, "w") as handle:
            handle.write(stdout)
        print('Writing ' + mafft_name +' to '+ output_dir + 'output/alignments/')
            
            
def trim_translate(data_frame_in, output_dir):
    '''trim and translate sequences for each FCGR/species combination'''
    
    types = list(set(data_frame_in["Types"].tolist()))
    for hit in types:
        infile = output_dir + 'output/fasta_output/' + hit +'_nt_mafft.fasta'
        alignments = list(SeqIO.parse(infile, 'fasta'))
        
        ref = alignments[0]
        l_trim = len(ref.seq)-len(ref.seq.lstrip('-'))
        r_trim = len(ref.seq)-len(ref.seq.rstrip('-'))
        ref_trimmed = ref.seq.ungap('-')
        ref_trans = SeqRecord(seq=ref_trimmed.translate())
        ref_trans.id = ref.id
        ref_trans.description = ''
        translated = [ref_trans]

        ids = []
        flags = []

        for aln in alignments[1:]:
            aln.seq = aln.seq[l_trim:]
            aln.seq = aln.seq[:-r_trim]
            aln.seq = aln.seq.ungap('-')
            ids.append(aln.id)
            if len(aln.seq) % 3 == 0:
                seqz = aln.translate()
                seqz.id = aln.id
                seqz.description = ''
                if seqz.seq.endswith('*'):
                    if seqz.seq.count('*')==1:
                        translated.append(seqz)
                        flag = ''
                    else:
                        flag='Nonsense mutation'
                else:
                    flag=("Does not end with STOP codon")
            else:
                flag=("Not multiple of 3")
            flags.append(flag)
            
        out = output_dir + 'output/fasta_output/' + hit +'_aa.fasta'
        SeqIO.write(translated, out, "fasta")
        print('Writing ' + hit+'_aa.fasta' +' to '+ output_dir + 'output/fasta_output/')

        flag_df = pd.DataFrame({"Barcode": ids, "Excluded?": flags})
        out_full2 = data_frame_in
        out_full2 = pd.merge(out_full2, flag_df, how='left', on=["Barcode"])
        out_full2.loc[out_full2['Excluded?_y'].map(str)=='nan',"Excluded?_y"] = ''

        out_full2['excluded_cat'] = out_full2["Excluded?_x"].map(str) + out_full2["Excluded?_y"].map(str)
        out_full2 = out_full2.drop(['Excluded?_x', 'Excluded?_y'], axis = 1)
        out_full2.rename(columns={'excluded_cat':'Excluded?'}, inplace=True)
        data_frame_in = out_full2

        in_file=out
        mafft_exe="/usr/local/bin/mafft"
        mafft_cline = MafftCommandline(mafft_exe,input=in_file, nuc=False, namelength=40, clustalout=True)
        stdout, stderr = mafft_cline()
        out_file = output_dir + 'output/alignments/' + hit + "_aa.txt"
        with open(out_file, "w") as handle:
            handle.write(stdout)
        print('Writing ' + hit + '_aa.txt' +' to '+ output_dir + 'output/alignments/')
            
        mafft_cline = MafftCommandline(mafft_exe,input=in_file, nuc=False, namelength=40, clustalout=False)
        stdout, stderr = mafft_cline()
        out_file = output_dir + 'output/fasta_output/'+ hit + "_aa_mafft.fasta"
        with open(out_file, "w") as handle:
            handle.write(stdout)
        print('Writing ' +hit + '_aa_mafft.fasta' +' to '+ output_dir + 'output/fasta_output/')
        
    return(data_frame_in)

def trim(data_frame_in, output_dir):
    '''trim sequences for each FCGR/species combination'''
    
    types = list(set(data_frame_in["Types"].tolist()))
    for hit in types:
        infile = output_dir + 'output/fasta_output/' + hit +'_nt_mafft.fasta'
        alignments = list(SeqIO.parse(infile, 'fasta'))
        
        ref = alignments[0]
        l_trim = len(ref.seq)-len(ref.seq.lstrip('-'))
        r_trim = len(ref.seq)-len(ref.seq.rstrip('-'))
        
        for aln in alignments:
            aln.seq = aln.seq[l_trim:]
            aln.seq = aln.seq[:-r_trim]

        out = output_dir + 'output/fasta_output/' + hit +'_nt_trimmed.fasta'
        SeqIO.write(alignments, out, "fasta")
        print('Writing ' + hit + '_nt_trimmed.fasta' +' to '+ output_dir + 'output/fasta_output/')
        
def mafft(infasta, output_dir, gene, nuc=True, clustalout=True):

    mafft_exe="/usr/local/bin/mafft"
    mafft_cline = MafftCommandline(mafft_exe,input=infasta, nuc=nuc, namelength=40, clustalout=clustalout)
    stdout, stderr = mafft_cline()
    if nuc==True:
        kind = 'NT'
    else:
        kind = 'AA'
    if clustalout==True:
        ext = '.txt'
    else:
        ext = '.fasta'
    mafft_name =  gene + '_' +kind+'_mafft' + ext
    out = output_dir + mafft_name
    with open(out, "w") as handle:
        handle.write(stdout)
        
def final_output(data_frame_in, output_dir, order_num, pool_num):
    excluded = data_frame_in.loc[data_frame_in['Excluded?']!='']
    excluded_name = output_dir + 'output/excluded/' + str(order_num) + '_P' + str(pool_num) + '_excluded_sequences.csv'
    excluded.to_csv(excluded_name, index=False)
    
    end_sequences = data_frame_in.loc[data_frame_in['Excluded?']=='']
    end_name = output_dir + 'output/' + str(order_num) + '_P' + str(pool_num) + '_alignments.csv'
    end_sequences = end_sequences[['Barcode', 'Num Reads', 'Top Hit', 'Reference Sequence', 'Reverse Complement', 'Gapped Identity', 'Gapless Identity', 'NTSubs', 'NT Read Length', 'AASubs', "AA Read Length"]]
    
    test = end_sequences["Barcode"].str.split("_", n = 8, expand = True)
    end_sequences['Order'] = test[0]
    end_sequences['Species'] = test[1]
    end_sequences['PTID'] = test[2]
    end_sequences['Pool'] = test[3]
    end_sequences['Pool'] = end_sequences['Pool'].astype(str).str[1:]
    end_sequences['Sequence ID'] = test[4]
    end_sequences['Primer'] = test[5]
    end_sequences['Cluster'] = test[6]
    end_sequences['Cluster'] = end_sequences['Cluster'].astype(str).str[1:]
    end_sequences['Phase'] = test[7]
    end_sequences['Phase'] = end_sequences['Phase'].astype(str).str[1:]
    end_sequences.drop('Barcode', axis=1, inplace=True)

    end_sequences = end_sequences[['Order','Pool', 'Species', 'PTID','Sequence ID','Primer', 'Cluster', 'Phase', 'Num Reads', 'Top Hit', 'Reference Sequence', 'Reverse Complement', 'Gapped Identity', 'Gapless Identity', 'NTSubs', 'NT Read Length', 'AASubs', 'AA Read Length' ]]

    end_sequences.to_csv(output_dir + 'output/' + str(order_num) + '_P' + str(pool_num) + '_alignments.csv', index=False)
    print('Writing final results to ' + output_dir + 'output/' + str(order_num) + '_P' + str(pool_num) + '_alignments.csv')
        
        



