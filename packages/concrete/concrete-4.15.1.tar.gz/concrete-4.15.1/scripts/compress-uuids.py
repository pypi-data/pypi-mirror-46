#!/usr/bin/env python

'''
Read a concrete tarball and write it back out, rewriting UUIDs with
compressible UUID scheme
'''
from __future__ import unicode_literals

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import logging

from concrete.util.file_io import CommunicationReader, CommunicationWriterTGZ
from concrete.util.concrete_uuid import compress_uuids as _compress_uuids
from concrete.util import set_stdout_encoding
import concrete.version


def compress_uuids(input_path, output_path, verify=False, uuid_map_path=None,
                   single_analytic=False):
    reader = CommunicationReader(input_path, add_references=False)
    writer = CommunicationWriterTGZ(output_path)

    if uuid_map_path is None:
        uuid_map_file = None
    else:
        uuid_map_file = open(uuid_map_path, 'w')

    for (i, (comm, comm_filename)) in enumerate(reader):
        (new_comm, uc) = _compress_uuids(comm, verify=verify,
                                         single_analytic=single_analytic)

        logging.info('compressed %s (%d analytics, %d uuids) (%d/?)'
                     % (comm.id, len(uc.augs), len(uc.uuid_map), i + 1))

        if uuid_map_file is not None:
            for (old_uuid, new_uuid) in sorted(uc.uuid_map.items(),
                                               key=lambda p: str(p[1])):
                uuid_map_file.write('%s %s\n' % (old_uuid, new_uuid))

        writer.write(new_comm, comm_filename=comm_filename)


def main():
    set_stdout_encoding()

    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description='Read a concrete tarball and write it back out, rewriting'
                    ' UUIDs with compressible UUID scheme',
    )
    parser.set_defaults(log_level='INFO')
    parser.add_argument('input_path', type=str,
                        help='Input tarball path (- for stdin)')
    parser.add_argument('output_path', type=str,
                        help='Output tarball path (- for stdout)')
    parser.add_argument('-l', '--loglevel', '--log-level',
                        help='Logging verbosity level threshold (to stderr)',
                        default='info')
    parser.add_argument('--verify', action='store_true',
                        help='Verify within-communication links are satisfied'
                             ' after conversion')
    parser.add_argument('--single-analytic', action='store_true',
                        help='Use one 10-byte prefix for all UUIDs in the'
                             ' communication rather than keying 4 of those'
                             ' bytes on the metadata tool (does not make a'
                             ' noticeable difference in size for typical'
                             ' communications)')
    parser.add_argument('--uuid-map-path', type=str,
                        help='Output path of UUID map')
    concrete.version.add_argparse_argument(parser)
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)-15s %(levelname)s: %(message)s',
                        level=args.loglevel.upper())

    # Won't work on Windows
    input_path = '/dev/fd/0' if args.input_path == '-' else args.input_path
    output_path = '/dev/fd/1' if args.output_path == '-' else args.output_path

    compress_uuids(input_path, output_path, verify=args.verify,
                   single_analytic=args.single_analytic,
                   uuid_map_path=args.uuid_map_path)


if __name__ == "__main__":
    main()
