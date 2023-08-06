#!/usr/bin/env python3

import glob
import os
import argparse
import datetime
import textwrap
from multiprocessing import Pool
from bactinspector.utility_functions import get_base_name
from bactinspector.mash_functions import run_mash_sketch, get_best_mash_matches_with_pandas, get_most_frequent_species_match
import pandas as pd


def is_valid_file(parser, arg):
    if not os.path.isfile(arg):
        parser.error('The file {} does not exist!'.format(arg))
    else:
        # File exists so return the filename
        return arg

def parse_arguments():
    description = textwrap.dedent("""
    A module to determine the most probable species based on sequence in fasta files using refseq and Mash (https://mash.readthedocs.io/en/latest/index.html)
    It will count the species of the top ref seq mash matches and report most frequent.

    In order to use the module:
      • Specify an input directory and output directory (default is current directory)
      • Specify either a 
        • fasta file pattern with -f (e.g "*.fas") or 
        • mash sketch file pattern with -m (e.g "*.msh") if you have already sketched the fasta files
      • Specify the path to the refseq sketch file downloaded from https://gembox.cbcb.umd.edu/mash/refseq.genomes.k21s1000.msh with -r
      • By default the top 10 matches will be used. Change this with -n
      • Speed things up by changing the number of parallel processes to match the cores on your computer using -p
      • If mash is not in your PATH specify the directory containing the mash executable with -mp
    """)
    # parse all arguments
    parser = argparse.ArgumentParser(description=description,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-i', '--input_dir', help='path to input_directory', default = '.')
    parser.add_argument('-o', '--output_dir', help='path to output_directory', default = '.')
    parser.add_argument('-p', '--parallel_processes', help='number of processes to run in parallel', default = 1, type = int)
    parser.add_argument('-r',
                        '--ref_seq_mash_sketch',
                        help = 'path to refseq mash sketch file',
                        type=lambda x: is_valid_file(parser, x),
                        required = True
                        )
    parser.add_argument('-n', '--num_best_matches', help='number of best matches to return', default = 10, type = int)

    parser.add_argument('-mp', '--mash_path', help='path to the mash executable. If not provided it is assumed mash is in the PATH')

    filetype_extension = parser.add_mutually_exclusive_group(required = True)
    filetype_extension.add_argument('-f', '--fasta_file_pattern', help='pattern to match fasta files e.g "*.fas"')
    filetype_extension.add_argument('-m', '--mash_sketch_file_pattern', help='pattern to match mash sketch files e.g "*.msh"')


    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    pool=Pool(processes=args.parallel_processes)

    if args.mash_path:
        mash_path = args.mash_path
    else:
        mash_path = ''
    
    if args.fasta_file_pattern:
        # run sketches in parallel
        fasta_files = glob.glob(os.path.join(args.input_dir, args.fasta_file_pattern))
        sketch_files = pool.starmap(run_mash_sketch, [(fasta_file,  args.output_dir, mash_path) for fasta_file in fasta_files])

    if args.mash_sketch_file_pattern:
        sketch_files = glob.glob(os.path.join(args.input_dir, args.mash_sketch_file_pattern))

    # run sketches in parallel
    match_files = pool.starmap(get_best_mash_matches_with_pandas, [(sample_sketch, args.ref_seq_mash_sketch, args.output_dir, mash_path,args.num_best_matches) for sample_sketch in sketch_files])

    #  read in species match table
    refseq_species_match_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'refseq.genomes.k21s1000.species.tsv')
    refseq_species_matches = pd.read_csv(refseq_species_match_file, sep = "\t" )
    
    results = {'file': [], 'species': [], 'percentage': []}
    for match_file in match_files:
        species, count = get_most_frequent_species_match(match_file, refseq_species_matches)
        results['file'].append(get_base_name(match_file).replace('.best_matches', ''))
        results['species'].append(species)
        results['percentage'].append(int(count/args.num_best_matches*100))
    
    results_df = pd.DataFrame(results).sort_values('species', ascending=True)
    now = datetime.datetime.now()
    outfile = os.path.join(args.output_dir, 'species_investigation_{0}.tsv'.format(now.strftime("%Y-%m-%d")))
    results_df.to_csv(outfile, sep = "\t", index = False)
    print("Results written to {0}".format(outfile))

if __name__ == "__main__":
    main()





