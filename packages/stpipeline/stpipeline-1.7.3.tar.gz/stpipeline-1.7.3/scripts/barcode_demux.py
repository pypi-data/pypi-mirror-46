#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Splits FASTQ files using barcodes found in R1 (from taggd)
Input:

- R1.fastq R2.fastq

Output:

- One fastq file for each barcode found in R1.fastq

@Author Jose Fernandez Navarro <jose.fernandez.navarro@scilifelab.se>
"""

import os.path
import argparse
from stpipeline.common.fastq_utils import *

def main(input_data, output):

    #TODO check format
    if len(input_data) != 2 or not os.path.isfile(input_data[0]) \
    or not os.path.isfile(input_data[1]):
        sys.stderr.write("Error, input file/s not present or invalid format\n")
        sys.exit(1)
    
    # Read the parameters
    fw = input_data[0]
    rv = input_data[1]
    
    # Open R1 and store barcodes and headers in dictionary
    fw_file = safeOpenFile(fw, "rU")
    barcode_to_reads = dict()
    for (header_fw, _, _) in readfq(fw_file):
        bc = header_fw.split()[2].split(":")[-1]
        header_clean = header_fw.split()[0]
        barcode_to_reads[header_clean] = bc
    
    # Create a dictionary of barcodes to fastq writers (one for each barcode)
    file_writers = dict()
    for bc in barcode_to_reads.values():
        out_rv_bc = safeOpenFile("{}_{}.fastq".format(output,bc), 'w')
        out_rv_bc_writer = writefq(out_rv_bc)
        file_writers[bc] = (out_rv_bc,out_rv_bc_writer)
    
    # Parse R2 and write records to correct file (barcode)
    rv_file = safeOpenFile(rv, "rU")
    for (header_rv, sequence_rv, quality_rv) in readfq(rv_file):
        try:
            bc = barcode_to_reads[header_rv]
            print("Printing {} to {}".format(header_rv, bc))
            file_writers[bc][1].send((header_rv, sequence_rv, quality_rv))
        except KeyError:
            print("Read {} does not contain barcode".format(header_rv))
    
    fw_file.close()
    rv_file.close()
    for writer in file_writers.values():
        writer[0].flush()
        writer[0].close()
        writer[1].close()    
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input_data", nargs=2)
    parser.add_argument("--output", default="output", help="Prefix for output files")
    args = parser.parse_args()
    main(args.input_data, args.output)
