# -*- coding: utf-8 -*-
import sys

import fastqlib as u

def main(input_file_path, output_file_path, number_of_sequences = -1, compressed = False):
    input = u.FastQSource(input_file_path, compressed)
    output = u.FileOutput(output_file_path, compressed)

    while input.next() and number_of_sequences:
        if input.p_available:
            input.print_percentage()
        e = input.entry
        output.write('>%s\n%s\n' % ('.'.join([e.machine_name,
                                              e.run_id,
                                              e.x_coord,
                                              e.y_coord,
                                              e.pair_no]),
                                             e.sequence))
        number_of_sequences -= 1

    sys.stderr.write('\n')
    input.close()
    output.close()
    
    return

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Convert FastQ to FASTA')
    parser.add_argument('-i', '--input', required=True, metavar = 'INPUT',
                        help = 'FASTQ file to be converted')
    parser.add_argument('-n', '--number-of-sequences', type=int, default = -1,
                        metavar = 'NUMBER', help = 'Number of sequences to be converted')
    parser.add_argument('-o', '--output', help = 'FASTA output (default: [-i]-FASTA-[-n]')

    args = parser.parse_args()

    input_file_path = args.input
    
    compressed = input_file_path.endswith('.gz')
    
    if args.output:
        if compressed and not args.output.endswith('.gz'):
            output_file_path = args.output + '.gz'
        else:
            output_file_path = args.output
    else:
        if compressed:
            if args.number_of_sequences > 0:
                output_file_path = input_file_path[:-3] + '-FASTA-%d.gz' % args.number_of_sequences
            else:
                output_file_path = input_file_path[:-3] + '-FASTA.gz'
        else:
            if args.number_of_sequences > 0:
                output_file_path = input_file_path + '-FASTA-%d' % args.number_of_sequences
            else:
                output_file_path = input_file_path + '-FASTA'

    sys.exit(main(input_file_path, output_file_path, args.number_of_sequences, compressed))