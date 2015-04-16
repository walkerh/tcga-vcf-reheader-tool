#!/usr/bin/env python2.7

"""Tool to read a TCGA Variant Call Format (VCF) file and output an
equivalent file with a different header"""


import argparse
import sys

import yaml


__VERSION__ = '0.1.0'


def main():
    args = parse_args()
    with open(args.parameter_file_path) as yaml_file:
        args.parameter_map = yaml.load(yaml_file)
    # TODO: Configure logging
    run(args)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input_file_path', help='the VCF to read')
    parser.add_argument('output_file_path', help='the VCF to write')
    parser.add_argument('parameter_file_path', help='the YAML with details')
    args = parser.parse_args()
    return args


def run(args):
    """Main entry point for testing and higher-level automation"""
    CONFIG = args.parameter_map['config']
    SAMPLE_LINE_FORMAT = '##' + CONFIG['sample_line_format'].replace(' ', '')
    fixed_headers = CONFIG['fixed_headers']
    filtered_headers = set(item[0] for item in fixed_headers)
    asserted_headers = set(item[0] for item in fixed_headers if item[1])
    with open(args.input_file_path) as fin:
        with open(args.output_file_path, 'w') as fout:
            write_fixed_headers(fout, fixed_headers)
            for id, params in args.parameter_map['samples'].items():
                sample_line = SAMPLE_LINE_FORMAT.format(
                    id=id, **dict(params, **CONFIG['fixed_sample_params'])
                )
                write_stripped_line(fout, sample_line)


def write_fixed_headers(fout, fixed_headers):
    for name, ignored, value in fixed_headers:
        write_meta_line(fout, name, value)


def write_meta_line(fout, name, value):
    fout.write('##{}={}\n'.format(name, value))


def write_stripped_line(fout, line):
    """Just adds the newline."""
    fout.write(line)
    fout.write('\n')


if __name__ == '__main__':
    main()
