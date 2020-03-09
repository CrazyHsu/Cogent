#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
File name: batch_run_Cogent_reconstruction.py.py
Author: CrazyHsu @ crazyhsu9527@gmail.com 
Created on: 2020-03-07 15:41:52
Last modified: 2020-03-07 15:41:52
'''

import os, sys, subprocess
from multiprocessing import Pool

def runCMD(cmd):
    # print cmd
    subprocess.call(cmd, shell=True)

def main(args):
    try:
        pool = Pool(processes=args.threads)
        multiRes = []
        for d in os.listdir(args.dirname):
            d2 = os.path.join(args.dirname, d)
            if not os.path.isdir(d2): continue
            fa = os.path.join(d2, 'in.fa')
            we = os.path.join(d2, 'in.weights')
            if not os.path.exists(fa):
                print >> sys.stderr, "{0} is missing! Please fix this first.".format(fa)
                sys.exit(-1)
            if not os.path.exists(we):
                print >> sys.stderr, "{0} is missing! Please fix this first.".format(we)
                sys.exit(-1)

            cmd = "reconstruct_contig.py " + d2
            # use the directory name as output prefix
            cmd += " -p {0} ".format(os.path.basename(d2))
            if args.genome_fasta_mmi is not None:
                cmd += " -G {0} -S {1} -t {2} ".format(args.genome_fasta_mmi, args.species_name, args.threads)
            # print cmd
            singleRunRes = pool.apply_async(runCMD, (cmd,))
            multiRes.append(singleRunRes)
        for j in multiRes:
            j.wait()
    except Exception as e:
        print e


if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("dirname")
    parser.add_argument("-G", "--genome_fasta_mmi", default=None, help="Optional genome fasta or mmi (ex: genome.fasta or genome.mmi). If provided, Cogent output will be mapped to the genome using minimap2.")
    parser.add_argument("-S", "--species_name", default="NA", help="Species name (optional, only used if genome fasta/mmi provided).")
    parser.add_argument("-T", "--threads", default=3, type=int, help="Threads to run the script")

    args = parser.parse_args()

    main(args)
