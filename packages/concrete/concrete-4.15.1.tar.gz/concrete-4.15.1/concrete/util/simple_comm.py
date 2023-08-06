"""Create a simple (valid) Communication suitable for testing purposes
"""
from __future__ import unicode_literals

import logging
import os
import re
import tempfile
import time

from ..communication.ttypes import Communication
from ..metadata.ttypes import AnnotationMetadata
from ..spans.ttypes import TextSpan
from ..structure.ttypes import (
    Section,
    Sentence,
    Token,
    Tokenization,
    TokenizationKind,
    TokenList
)
from .concrete_uuid import AnalyticUUIDGeneratorFactory
from .file_io import CommunicationWriter


AL_NONE = 'none'
AL_SECTION = 'section'
AL_SENTENCE = 'sentence'
AL_TOKEN = 'token'


def add_annotation_level_argparse_argument(parser):
    """Add an '--annotation-level' argument to an ArgumentParser

    The '--annotation-level argument specifies the level of
    concrete annotation to infer from whitespace in text.
    See :func:`create_comm` for details.

    Args:
        parser (argparse.ArgumentParser): the parser to add the argument
            to
    """
    parser.add_argument('--annotation-level', type=str,
                        choices=(AL_NONE, AL_SECTION, AL_SENTENCE, AL_TOKEN),
                        help='Level of concrete annotation to infer from'
                             ' whitespace in text (%s: no annotation,'
                             ' %s: sections inferred'
                             ' from double-newline, %s: "%s" and sentences'
                             ' inferred from single-newline, %s: "%s" and'
                             ' tokens inferred from remaining whitespace)' %
                             (AL_NONE,
                              AL_SECTION,
                              AL_SENTENCE, AL_SECTION,
                              AL_TOKEN, AL_SENTENCE))


def _split(s, delim):
    '''
    Split string and return list of tuples representing the pieces of
    the string and their offsets in the string.

    Args:
        s (str): string to split
        delim (str): delimiter by which to split string

    Returns:
        list of tuples representing the split pieces of the string;
        each tuple contains a string (a piece of `s`), an integer
        indicating where that string starts in `s`, and an integer
        indicating where that string ends in `s` (exclusive), in
        that order
    '''
    pieces = s.split(delim)
    indexed_pieces = []
    offset = 0
    for p in pieces:
        indexed_pieces.append((p, offset, offset + len(p)))
        offset += len(p) + len(delim)
    return indexed_pieces


def create_sentence(sen_text, sen_start, sen_end,
                    aug, metadata_tool, metadata_timestamp,
                    annotation_level):
    """Create :class:`.Sentence` from provided text and metadata.

    Lower-level routine (called indirectly by :func:`create_comm`)

    Args:
        sen_text (str): text to create sentence from
        sen_start (int): starting position of sentence in Communication
            text (inclusive)
        sen_end (int): ending position of sentence in Communication text
            (inclusive)
        aug (_AnalyticUUIDGenerator): compressible UUID generator for
            the analytic that generated this sentence
        metadata_tool (str): tool name of the analytic that generated
            this sentence
        metadata_timestamp (int): Time in seconds since the Epoch
        annotation_level (str): See :func:`create_comm` for details

    Returns:
        Concrete Sentence containing given text and metadata
    """

    sections = (annotation_level is not None) and (annotation_level != AL_NONE)
    sentences = sections and (annotation_level != AL_SECTION)
    tokens = sentences and (annotation_level != AL_SENTENCE)

    return Sentence(
        uuid=next(aug),
        textSpan=TextSpan(sen_start, sen_end),
        tokenization=Tokenization(
            uuid=next(aug),
            kind=TokenizationKind.TOKEN_LIST,
            metadata=AnnotationMetadata(
                tool=metadata_tool,
                timestamp=metadata_timestamp,
            ),
            tokenList=TokenList(tokenList=[
                Token(
                    tokenIndex=i,
                    text=match.group(),
                    textSpan=TextSpan(
                        start=match.start() + sen_start,
                        ending=match.end() + sen_start
                    ),
                )
                for (i, match)
                in enumerate([m for m in re.finditer(r'\S+', sen_text)])
            ]),
        ) if tokens else None,
    )


def create_section(sec_text, sec_start, sec_end, section_kind,
                   aug, metadata_tool, metadata_timestamp,
                   annotation_level):
    """Create :class:`.Section` from provided text and metadata.
    Section text will be split into sentence texts by newlines and
    each sentence will be created with a call to
    :func:`create_sentence`.

    Lower-level routine (called by :func:`create_comm`).

    Args:
        sec_text (str): text to create section from
        sec_start (int): starting position of section in Communication
            text (inclusive)
        sec_end (int): ending position of section in Communication text
            (inclusive)
        section_kind (str): value for `Section.kind` field to be set to
        aug (_AnalyticUUIDGenerator): compressible UUID generator for
            the analytic that generated this section
        metadata_tool (str): tool name of the analytic that generated
            this section
        metadata_timestamp (int): Time in seconds since the Epoch
        annotation_level (str): See :func:`create_comm` for details

    Returns:
        Concrete Section containing given text and metadata
    """

    sections = (annotation_level is not None) and (annotation_level != AL_NONE)
    sentences = sections and (annotation_level != AL_SECTION)

    return Section(
        uuid=next(aug),
        textSpan=TextSpan(sec_start, sec_end),
        kind=section_kind,
        sentenceList=(
            [
                create_sentence(sen_text,
                                sec_start + sen_start,
                                sec_start + sen_end,
                                aug, metadata_tool, metadata_timestamp,
                                annotation_level)
                for (sen_text, sen_start, sen_end) in _split(sec_text, '\n')
            ] if ('\n' in sec_text) or sec_text.strip() else []
        ) if sentences else None,
    )


def create_comm(comm_id, text='',
                comm_type='article', section_kind='passage',
                metadata_tool='concrete-python',
                metadata_timestamp=None,
                annotation_level=AL_TOKEN):
    """Create a simple, valid :class:`.Communication` from text.

    By default the text will be split by double-newlines into sections
    and then by single newlines into sentences within those sections.
    Each section will be created with a call to :func:`create_section`.

    `annotation_level` controls the amount of annotation that is added:

     - AL_NONE:      add no optional annotations (not even sections)
     - AL_SECTION:   add sections but not sentences
     - AL_SENTENCE:  add sentences but not tokens
     - AL_TOKEN:     add all annotations, up to tokens (the default)

    Args:
        comm_id (str): Communication id
        text (str): Communication text
        comm_type (str): Communication type
        section_kind (str): Section kind to set on all sections
        metadata_tool (str): tool name of analytic that generated
            this text
        metadata_timestamp (int): Time in seconds since the Epoch.
            If `None`, the current time will be used.
        annotation_level (str): string representing annotation
            level to add to communication (see above)

    Returns:
        Communication containing given text and metadata
    """

    if metadata_timestamp is None:
        metadata_timestamp = int(time.time())

    augf = AnalyticUUIDGeneratorFactory()
    aug = augf.create()

    sections = (annotation_level is not None) and (annotation_level != AL_NONE)

    return Communication(
        id=comm_id,
        uuid=next(aug),
        type=comm_type,
        text=text,
        metadata=AnnotationMetadata(
            tool=metadata_tool,
            timestamp=metadata_timestamp,
        ),
        sectionList=(
            [
                create_section(sec_text, sec_start, sec_end, section_kind,
                               aug, metadata_tool, metadata_timestamp,
                               annotation_level)
                for (sec_text, sec_start, sec_end) in _split_sections(text)
            ] if text.strip() else []
        ) if sections else None,
    )


def _split_sections(s):
    """Split string into sections when there are two or more "empty" lines

    Args:
        s (str): text to split

    Returns:
        list of tuples representing the split pieces of the section;
        each tuple contains a string (a piece of `s`), an integer
        indicating where that section starts in `s`, and an integer
        indicating where that section ends in `s` (exclusive), in
        that order
    """
    # Ignore whitespace at beginning/end of document
    m = re.match(r'^(?:\s*\r?\n)*(.*?)(?:\s*\r?\n)*$', s, re.DOTALL)
    stripped_start_offset = m.span(1)[0]
    stripped_end_offset = m.span(1)[1]
    stripped = s[stripped_start_offset:stripped_end_offset]

    offsets = []
    offsets.append(stripped_start_offset)
    for sec_break in [sm.span() for sm in re.finditer(r'(?:\s*\r?\n){2,}', stripped, re.DOTALL)]:
        offsets.append(sec_break[0] + stripped_start_offset)
        offsets.append(sec_break[1] + stripped_start_offset)
    offsets.append(stripped_end_offset)

    sections = []
    it = iter(offsets)
    for (start, end) in zip(it, it):
        sections.append((s[start:end], start, end))

    return sections


def create_simple_comm(comm_id, sentence_string="Super simple sentence ."):
    """Create a simple (valid) :class:`.Communication` suitable for testing purposes

    The Communication will have a single :class:`.Section` containing
    a single :class:`.Sentence`.

    Args:
        comm_id (str): Communication id
        sentence_string (str): Communication text

    Returns:
        Communication containing given text and having the given id
    """
    logging.warning('create_simple_comm will be removed in a future'
                    ' release, please use create_comm instead')

    toolname = "TEST"
    timestamp = int(time.time())

    augf = AnalyticUUIDGeneratorFactory()
    aug = augf.create()

    comm = Communication(
        id=comm_id,
        metadata=AnnotationMetadata(tool=toolname, timestamp=timestamp),
        type=toolname,
        uuid=next(aug)
    )

    tokenization = Tokenization(
        kind=TokenizationKind.TOKEN_LIST,
        metadata=AnnotationMetadata(tool=toolname, timestamp=timestamp),
        tokenList=TokenList(
            tokenList=[]),
        uuid=next(aug)
    )
    token_string_list = sentence_string.split()
    for i, token_string in enumerate(token_string_list):
        tokenization.tokenList.tokenList.append(Token(text=token_string,
                                                      tokenIndex=i))

    sentence = Sentence(
        textSpan=TextSpan(0, len(sentence_string)),
        tokenization=tokenization,
        uuid=next(aug)
    )

    section = Section(
        kind="SectionKind",
        sentenceList=[sentence],
        textSpan=TextSpan(0, len(sentence_string)),
        uuid=next(aug)
    )

    comm.sectionList = [section]
    comm.text = sentence_string

    return comm


class SimpleCommTempFile(object):
    """DEPRECATED. Please use :func:`create_comm` instead.

    Class representing a temporary file of sample concrete objects.
    Designed to facilitate testing.

    Attributes:
        path (str): path to file
        communications (Communication[]): List of communications that were written to file

    Usage::

        from concrete.util import CommunicationReader
        with SimpleCommTempFile(n=3, id_fmt='temp-%d') as f:
            reader = CommunicationReader(f.path)
            for (orig_comm, comm_path_pair) in zip(f.communications, reader):
                print(orig_comm.id)
                print(orig_comm.id == comm_path_pair[0].id)
                print(f.path == comm_path_pair[1])
    """

    def __init__(self, n=10, id_fmt='temp-%d',
                 sentence_fmt='Super simple sentence %d .',
                 writer_class=CommunicationWriter, suffix='.concrete'):
        """
        Create temp file and write communications.

        Args:
            n:i     number of communications to write
            id_fmt: format string used to generate communication IDs;
                    should contain one instance of %d, which will be
                    replaced by the number of the communication
            sentence_fmt: format string used to generate communication
                    IDs; should contain one instance of %d, which will
                    be replaced by the number of the communication
            writer_class: CommunicationWriter or CommunicationWriterTGZ
            suffix: file path suffix (you probably want to choose this
                    to match writer_class)
        """
        logging.warning('SimpleCommTempFile will be removed in a future'
                        ' release, please use create_comm instead')

        (fd, path) = tempfile.mkstemp(suffix=suffix)
        os.close(fd)
        self.path = path
        self.communications = []
        w = writer_class()
        w.open(path)
        for i in range(n):
            comm = create_simple_comm(id_fmt % i, sentence_fmt % i)
            self.communications.append(comm)
            w.write(comm)
        w.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if os.path.exists(self.path):
            os.remove(self.path)
