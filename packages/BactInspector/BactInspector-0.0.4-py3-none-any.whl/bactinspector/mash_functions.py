import os, glob, sys
import pandas
from bactinspector.utility_functions import add_new_file_extension, get_base_name, run_command
import pandas as pd
from io import StringIO


def run_mash_sketch(fasta_file, output_dir = None, mash_path = ''):
    """
    run mash sketch on a fasta file and return the path to the resulting sketch file
    """
    if output_dir:
        sketch_file = os.path.join(output_dir, '{0}.msh'.format(get_base_name(fasta_file)))
    else:
        sketch_file = add_new_file_extension(fasta_file, 'msh')
    
    if not os.path.exists(sketch_file) or os.path.getsize(sketch_file) == 0:
        print('Sketching {0}'.format(get_base_name(fasta_file)))
        command_and_arguments = [os.path.join(mash_path, 'mash'), 'sketch', fasta_file,  '-o', sketch_file]
        ret_code, out, err = run_command(command_and_arguments)
        if ret_code != 0:
            print('Error whilst performing mash sketch: {0}'.format(err))
            sys.exit(ret_code)
    return sketch_file

def get_best_mash_matches(sample_sketch, ref_seq_sketch, output_dir = None, mash_path = '', number_of_best_matches = 10):
    """
    run mash dist sample sketch file vs the ref_seq sketches and return the best matches
    """
    match_file = add_new_file_extension(sample_sketch, 'best_matches.txt')
    if not os.path.exists(match_file) or os.path.getsize(match_file) == 0:
        print('Getting best match for {0}'.format(get_base_name(sample_sketch)))

        command_and_arguments = "{0} dist {1} {2} | sort -grk3 | tail {3} | awk '{{print $2}}' > {4}".format(
            os.path.join(mash_path, 'mash'),
            sample_sketch,
            ref_seq_sketch,
            number_of_best_matches,
            match_file
        )
        ret_code, out, err = run_command(command_and_arguments, shell=True)
        if ret_code != 0:
            print('Error whilst performing mash dist: {0}'.format(err))
            sys.exit(ret_code)
    return match_file

def get_best_mash_matches_with_pandas(sample_sketch, ref_seq_sketch, output_dir = None, mash_path = '', number_of_best_matches = 10):
    """
    run mash dist sample sketch file vs the ref_seq sketches and return the best matches
    """
    match_file = add_new_file_extension(sample_sketch, 'best_matches.txt')
    if not os.path.exists(match_file) or os.path.getsize(match_file) == 0:
        print('Getting best match for {0}'.format(get_base_name(sample_sketch)))

        command_and_arguments = [os.path.join(mash_path, 'mash'),  'dist', sample_sketch, ref_seq_sketch ]
        ret_code, out, err = run_command(command_and_arguments)
        if ret_code != 0:
            print('Error whilst performing mash dist: {0}'.format(err))
            sys.exit(ret_code)
        distances_fh = StringIO(out.decode("utf-8"))
        mash_dists = pd.read_csv(distances_fh, sep = "\t", names = ['query', 'subject', 'distance', 'p-value', 'shared-hashes'])
        # sort file by distance and output the subjects (match in refseq) as a list
        matches = list(mash_dists.sort_values('distance', ascending=True).head(number_of_best_matches).loc[:,'subject'])

        # write matches to file
        with open(match_file, 'w') as match_fh:
            match_fh.write('filename\n')
            for match in matches:
                match_fh.write('{0}\n'.format(match))
    return match_file

def get_species_match_counts(match_file, refseq_species_matches):
    """
    use pandas to merge best match file with ref species matches and report the most frequent species
    return species and count
    """
    best_matches = pd.read_csv(match_file, sep = '\t')
    # delete matches if they already exist
    best_matches = best_matches[['filename']]
    # the lambda below only includes species
    best_match_species_df = best_matches.merge(
        refseq_species_matches,
            on = ['filename']
    )
    best_match_species_df[['filename', 'length', 'num_contigs', 'organism_name']].to_csv(match_file, sep = "\t", index = False)
    best_match_species = best_match_species_df['organism_name'].map(lambda x: ' '.join(x.split(' ')[0:2]))
    return best_match_species.value_counts()

def get_most_frequent_species_match(match_file, refseq_species_matches):
    species_match_counts = get_species_match_counts(match_file, refseq_species_matches)
    return species_match_counts.index[0], species_match_counts[0]