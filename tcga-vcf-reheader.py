#!/usr/bin/env python2.7

"""Tool to read a TCGA Variant Call Format (VCF) file and output an
equivalent file with a different header"""


import argparse
import sys

import yaml


__VERSION__ = '0.1.0'


def main():
    args = parse_args()
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
    with open(args.parameter_file_path) as yaml_file:
        parameter_map = yaml.load(yaml_file)
    CONFIG = parameter_map['config']
    SAMPLE_LINE_FORMAT = '##' + CONFIG['sample_line_format'].replace(' ', '')
    fixed_headers = CONFIG['fixed_headers']
    filtered_headers = set(item[0] for item in fixed_headers)
    asserted_headers = set(item[0] for item in fixed_headers if item[1])
    with open(args.input_file_path) as fin:
        with open(args.output_file_path, 'w') as fout:
            for name, ignored, value in fixed_headers:
                write_meta_line(fout, name, value)
            for id, params in parameter_map['samples'].items():
                print id
                
                sample_line = SAMPLE_LINE_FORMAT.format(
                    id=id, **dict(params, **CONFIG['fixed_sample_params'])
                )
                print sample_line


def write_meta_line(fout, name, value):
    fout.write('##{}={}\n'.format(name, value))


if __name__ == '__main__':
    main()
