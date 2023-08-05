#!/usr/bin/python

import sys 
sys.path.append('/Volumes/dusom_dhvi/All_Staff/DHVI-Users/mb488/Scripts/FcGR_Pipeline/')

import sys, getopt
from fcgr_py import process

# def main(argv):
#     input_dir = ''
#     output_dir = ''
#     try:
#         opts, args = getopt.getopt(argv,"hi:o:f:btO:p",["input_dir=","output_dir=", 'fastq_name=', 'barcode_names', 'threshold', 'order_num=', 'pool_num'])
#     except getopt.GetoptError:
#         print 'test.py -i <inputfile> -o <outputfile>'
#         sys.exit(2)
#     for opt, arg in opts:
#         if opt == '-h':
#         print 'fcgr_pipeline.py -i <input_dir> -o <output_dir> -f <fastq_name> -b <barcode_names.txt> -t <threshold> --order_num <order#> --pool_num <pool#>' 
#         sys.exit()
#     elif opt in ("-i", "--input_dir"):
#         input_dir = arg
#     elif opt in ("-o", "--output_dir"):
#         output_dir = arg
#     elif opt in ('-f', '--fastq_name'):
#         fastq_name = arg
#     elif opt in ('-b', '--barcode_names'):
#         barcode_names = arg
#     elif opt in ('-t', '--threshold'):
#         threshold = arg
#     elif opt in ('-O', '--order_num'):
#         order_num = arg
#     elif opt in ('-p', '--pool_num'):
#         pool_num = arg
        
#     fcgr_pipeline(input_dir, fastq_name, output_dir, order_num, pool_num=1, barcode_names = 'barcode_names.txt')
    
    
import argparse

# Create argument parser
parser = argparse.ArgumentParser(prog='FcGR Pipeline', usage='%(prog)s [options]')

# Positional mandatory arguments
parser.add_argument('input_dir', help = 'Directory where fastq and barcode names files are located', type=str)
parser.add_argument("output_dir", help="Directory to output results", type=str)
parser.add_argument("fastq_name", help="Name of fastq file", type=str)
parser.add_argument("order_num", help="Order number", type=int)

# Optional arguments
parser.add_argument("-p", "--pool_num", help="Pool number", type=int, default=1)
parser.add_argument("-b", "--barcode_names", help="Name of file containing barcode info (barcode_names.txt)", type=str, default='barcode_names.txt')
parser.add_argument("-t", "--threshold", help="Gapless identity threshold", type=float, default=.99)

# Parse arguments
args = parser.parse_args()


process.fcgr_pipeline(input_dir = args.input_dir, output_dir = args.output_dir,fastq_name = args.fastq_name, order_num = args.order_num, pool_num =args.pool_num, barcode_names = args.barcode_names , threshold = args.threshold)