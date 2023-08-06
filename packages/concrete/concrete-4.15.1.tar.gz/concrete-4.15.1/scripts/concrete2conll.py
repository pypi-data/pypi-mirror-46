#!/usr/bin/env python
"""Convert a tokenized Communication to a CoNLL-style file
"""

from __future__ import print_function

import argparse
import codecs
from collections import defaultdict

import concrete
from concrete.util import read_communication_from_file


def concrete2conll(concrete_filename, conll_filename):
    comm = read_communication_from_file(concrete_filename)

    conll_file = codecs.open(conll_filename, 'w', encoding='utf-8')

    for tokenization in concrete.util.tokenization.get_comm_tokenizations(comm):
        try:
            ner_tagged_tokens = concrete.util.tokenization.get_ner(tokenization)
            index_to_tag = defaultdict(str)
            for ner_tagged_token in ner_tagged_tokens:
                index_to_tag[ner_tagged_token.tokenIndex] = ner_tagged_token.tag
            for token in tokenization.tokenList.tokenList:
                conll_file.write('%d\t%s\t%s\n' %
                                 (token.tokenIndex+1, token.text, index_to_tag[token.tokenIndex]))
        except concrete.util.tokenization.NoSuchTokenTagging:
            for token in tokenization.tokenList.tokenList:
                conll_file.write('%d\t%s\n' % (token.tokenIndex+1, token.text))
        conll_file.write('\n')


def main():
    parser = argparse.ArgumentParser(
        description="Convert a tokenized Communication to a CoNLL-style file")
    parser.add_argument('concrete_file')
    parser.add_argument('conll_file')
    args = parser.parse_args()
    concrete2conll(args.concrete_file, args.conll_file)


if __name__ == "__main__":
    main()
