#!/usr/bin/env python

'Convert text file to Concrete Communication file.'
from __future__ import unicode_literals

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import codecs
import logging

import concrete.version
from concrete.util.file_io import write_communication_to_file
from concrete.util.simple_comm import (
    create_comm, AL_NONE, add_annotation_level_argparse_argument
)
from concrete.util import set_stdout_encoding


def main():
    set_stdout_encoding()

    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description='Convert text file to communication',
    )
    parser.set_defaults(annotation_level=AL_NONE)
    parser.add_argument('text_path', type=str,
                        help='Input text file path (- for stdin)')
    parser.add_argument('concrete_path', type=str,
                        help='Output concrete file path (- for stdout)')
    add_annotation_level_argparse_argument(parser)
    parser.add_argument('-l', '--loglevel', '--log-level',
                        help='Logging verbosity level threshold (to stderr)',
                        default='info')
    concrete.version.add_argparse_argument(parser)
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)-15s %(levelname)s: %(message)s',
                        level=args.loglevel.upper())

    # Won't work on Windows
    text_path = '/dev/fd/0' if args.text_path == '-' else args.text_path
    concrete_path = (
        '/dev/fd/1' if args.concrete_path == '-' else args.concrete_path
    )
    annotation_level = args.annotation_level

    with codecs.open(text_path, encoding='utf-8') as f:
        comm = create_comm(text_path, f.read(),
                           annotation_level=annotation_level)
        write_communication_to_file(comm, concrete_path)


if __name__ == "__main__":
    main()
