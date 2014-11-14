#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import argparse
import os.path
import json
from parser import TreeNode, Context, parse_node, get_generator

__all__ = ['main']


def parse_args():
    parser = argparse.ArgumentParser(
        description=('Convert json to model source file. '
                     'Currently supports Objective C'),
        epilog='Please send bug reports to clowwindy <clowwindy42@gmail.com>')
    parser.add_argument('-i', '--input', required=True,
                        help='a directory containing json files')
    parser.add_argument('-o', '--output', required=True,
                        help='a directory for output files')
    parser.add_argument('-l', '--language', default='objc',
                        help='language, default: objc')
    return parser.parse_args()


def main():
    args = parse_args()
    inputs = glob.glob(os.path.join(args.input, '*.json'))
    for i in inputs:
        print 'converting', i
        content = json.load(open(i))
        node = TreeNode()
        context = Context()
        parse_node(content, node, context)
        context.add_node(node)
        context.build_inheritance()
        get_generator(args.language).gen_code(args.output, context)

if __name__ == '__main__':
    main()
