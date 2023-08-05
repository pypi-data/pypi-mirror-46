from Bio import SeqIO
import string
import pandas as pd
import subprocess
import string
from Bio.Align.Applications import MafftCommandline

alphabet = list(string.ascii_uppercase)
letters = list(string.ascii_uppercase)
for i,letter in zip(range(1,26),alphabet):
    for letter2 in alphabet[i:]:
        letters.append(letter+letter2)


def find(ch,string):
    '''find all occurence of substring in string'''
    pos = []
    for i in range(len(string)):
        if ch == string[i]:
            pos.append(i)
    return(pos)

def get_numbering(in_file):
    '''get numbering schema from mafft aa fasta file'''
    
    seqs = list(SeqIO.parse(in_file, 'fasta'))
    ref = str(seqs[0].seq)

    i = 1
    nums = []
    for char in ref:
        if char != '-':
            nums.append(i)
            i += 1
        if char == '-':
            nums.append('-')
            
    indx = find('-', ref)

    chars = ['A']
    char_index = 0

    for i, pos in zip(indx[1:], range(len(indx))):
        if i-1!=indx[pos]:
            char_index = 0
            chars.append(letters[char_index])
        if i-1==indx[pos]:
            char_index += 1
            chars.append(letters[char_index])
            
    pos_nums = []
    pos = 1      
    for x in nums:
        if x!='-':
            pos += 1
        else:
            pos_nums.append(pos-1)

    num_letters = []
    for c, n in zip(chars, pos_nums):
        num_letters.append(str(n)+c)

    for i, n in zip(indx, num_letters):
        nums[i] = n

    return(list(nums))

# def get_aa_subs(data_frame_in, output_dir):
    
#     types = list(set(data_frame_in["Types"].tolist()))
    
#     numbering = {}
#     for hit in types:
#         file = output_dir + 'output/fasta_output/' + hit + '_aa_mafft.fasta'
#         numbering[hit] = get_numbering(file)

#     data_frame_in['AASubs'] = ''

#     for hit in types:
#         file = output_dir + 'output/fasta_output/' + hit + '_aa_mafft.fasta'
#         seqs = list(SeqIO.parse(file, 'fasta'))
        
#         print(hit)
        
#         nums = numbering[hit]
        
#         ref = seqs[0]
        
#         all_snps = {}
#         for seqz in seqs[1:]:
#             snps = []
#             for r, s, num in zip(ref, seqz, nums):
#                 if r!=s:
#                     sequence = s
#                     reference = r
#                     snp = reference + str(num) + sequence
#                     snps.append(snp)
#             all_snps[seqz.id] = snps
            
#         barcodes = list(all_snps.keys())
#         subs = list(all_snps.values())
#         for bar, sub in zip(barcodes, subs):
#             data_frame_in.loc[data_frame_in["Barcode"]==bar,'AASubs']=str(sub)
#         data_frame_in2 = data_frame_in
            
#     return(data_frame_in2)

def get_AA_read_lengths(data_frame_in, output_dir):

    data_frame_in['AA Read Length'] = ''

    types = list(set(data_frame_in["Types"].tolist()))

    for hit in types:
        read_lengths = []
        barcodes = []
        file = output_dir + 'output/fasta_output/' + hit + '_aa.fasta'
        seqs = list(SeqIO.parse(file, 'fasta'))
        for seqz in seqs[1:]:
            read_lengths.append(len(seqz.seq))
            barcodes.append(seqz.id)

        for rl, bar in zip(read_lengths, barcodes):
            data_frame_in.loc[data_frame_in['Barcode']==bar, 'AA Read Length'] = rl
    
    return(data_frame_in)

# def get_nt_subs(data_frame_in, output_dir):
    
#     types = list(set(data_frame_in["Types"].tolist()))
    
#     numbering = {}
#     for hit in types:
#         file = output_dir + 'output/fasta_output/' + hit + '_nt_trimmed.fasta'
#         numbering[hit] = get_numbering(file)

#     data_frame_in['NTSubs'] = ''

#     for hit in types:
#         file = output_dir + 'output/fasta_output/' + hit + '_nt_trimmed.fasta'
#         seqs = list(SeqIO.parse(file, 'fasta'))
        
#         print(hit)
        
#         nums = numbering[hit]
        
#         ref = seqs[0]
        
#         all_snps = {}
#         for seqz in seqs[1:]:
#             snps = []
#             for r, s, num in zip(ref, seqz, nums):
#                 if r!=s:
#                     sequence = s
#                     reference = r
#                     snp = reference + str(num) + sequence
#                     snps.append(snp)
#             all_snps[seqz.id] = snps
            
#         barcodes = list(all_snps.keys())
#         subs = list(all_snps.values())
#         for bar, sub in zip(barcodes, subs):
#             data_frame_in.loc[data_frame_in["Barcode"]==bar,'NTSubs']=str(sub)
#         data_frame_in2 = data_frame_in
            
#     return(data_frame_in2)

def get_NT_read_lengths(data_frame_in, output_dir):

    data_frame_in['NT Read Length'] = ''

    types = list(set(data_frame_in["Types"].tolist()))

    for hit in types:
        read_lengths = []
        barcodes = []
        file = output_dir + 'output/fasta_output/' + hit + '_nt_trimmed.fasta'
        seqs = list(SeqIO.parse(file, 'fasta'))
        for seqz in seqs[1:]:
            read_lengths.append(len(seqz.seq))
            barcodes.append(seqz.id)

        for rl, bar in zip(read_lengths, barcodes):
            data_frame_in.loc[data_frame_in['Barcode']==bar, 'NT Read Length'] = rl
    
    return(data_frame_in)

def get_nt_subs_single_fasta(fasta, gene):
    
    numbering = {}
    numbering[gene] = get_numbering(fasta)

    nt_subs = []

    seqs = list(SeqIO.parse(fasta, 'fasta'))

    nums = numbering[gene]
        
    ref = seqs[0]
        
    all_snps = {}
    for seqz in seqs[1:]:
        snps = []
        for r, s, num in zip(ref, seqz, nums):
            if r!=s:
                sequence = s
                reference = r
                snp = reference + str(num) + sequence
                snps.append(snp)
        all_snps[seqz.id] = snps

    barcodes = list(all_snps.keys())
    subs = list(all_snps.values())
    
            
    return(barcodes,subs)

def get_aa_subs(data_frame_in, output_dir):
    
    data_frame_in['AASubs'] = ''
    
    mafft_exe="/usr/local/bin/mafft"
    
    types = list(set(data_frame_in["Types"].tolist()))
    
    for hit in types:
        
        print('Getting AA substitutions for ' + hit)

        seqs = list(SeqIO.parse(output_dir + 'output/fasta_output/' + hit +'_aa.fasta', 'fasta'))
        ref = seqs[0]

        all_snps = {}
        for seq, i in zip(seqs[1:], range(1,len(seqs))):

            to_fasta = [ref ,seq]

            fasta_name = output_dir + '/output/temp/' + hit + '/ref_' + str(i) + '.fasta'
            SeqIO.write(to_fasta, fasta_name, 'fasta')

            mafft_cline = MafftCommandline(mafft_exe,input=fasta_name, nuc=False, namelength=40, clustalout=False)
            stdout, stderr = mafft_cline()

            mafft_name =  output_dir + 'output/temp/' + hit + '/ref_' + str(i) + '_mafft.fasta'
            with open(mafft_name, "w") as handle:
                handle.write(stdout)

            nums = get_numbering(mafft_name)

            seq_pair = list(SeqIO.parse(mafft_name, 'fasta'))


            ref_list = list(seq_pair[0])
            sample_seq = list(seq_pair[1])

            snps = []
            for r, s, num in zip(ref_list, sample_seq, nums):
                if r!=s:
                    sequence = s
                    reference = r
                    snp = reference + str(num) + sequence
                    snps.append(snp)

            all_snps[seq.id] = snps
            
        barcodes = list(all_snps.keys())
        subs = list(all_snps.values())
        for bar, sub in zip(barcodes, subs):
            data_frame_in.loc[data_frame_in["Barcode"]==bar,'AASubs']=str(sub)
        data_frame_in2 = data_frame_in
            
    return(data_frame_in2)

def get_nt_subs(data_frame_in, output_dir):
    
    data_frame_in['NTSubs'] = ''
    
    mafft_exe="/usr/local/bin/mafft"
    subprocess.run(['mkdir', output_dir + 'output/temp'])
    
    types = list(set(data_frame_in["Types"].tolist()))
    
    for hit in types:
        
        subprocess.run(['mkdir', output_dir + 'output/temp/'+hit])
        
        print('Getting NT mutations for '+ hit)
        seqs = list(SeqIO.parse(output_dir + 'output/fasta_output/' + hit +'_nt_trimmed.fasta', 'fasta'))
        ref = seqs[0]

        all_snps = {}
        for seq, i in zip(seqs[1:], range(1,len(seqs))):

            to_fasta = [ref ,seq]

            fasta_name = output_dir + '/output/temp/' + hit + '/ref_nt_' + str(i) + '.fasta'
            SeqIO.write(to_fasta, fasta_name, 'fasta')

            mafft_cline = MafftCommandline(mafft_exe,input=fasta_name, nuc=True, namelength=40, clustalout=False)
            stdout, stderr = mafft_cline()

            mafft_name =  output_dir + 'output/temp/' + hit + '/ref_nt_' + str(i) + '_mafft.fasta'
            with open(mafft_name, "w") as handle:
                handle.write(stdout)

            nums = get_numbering(mafft_name)

            seq_pair = list(SeqIO.parse(mafft_name, 'fasta'))


            ref_list = list(seq_pair[0])
            sample_seq = list(seq_pair[1])

            snps = []
            for r, s, num in zip(ref_list, sample_seq, nums):
                if r!=s:
                    sequence = s
                    reference = r
                    snp = reference + str(num) + sequence
                    snps.append(snp)

            all_snps[seq.id] = snps
            
        barcodes = list(all_snps.keys())
        subs = list(all_snps.values())
        for bar, sub in zip(barcodes, subs):
            data_frame_in.loc[data_frame_in["Barcode"]==bar,'NTSubs']=str(sub)
        data_frame_in2 = data_frame_in
            
    return(data_frame_in2)




            



