from __future__ import unicode_literals
import logging

from ..structure.ttypes import TokenizationKind
from .unnone import lun

from collections import deque
from math import log, exp
from functools import reduce


class NoSuchTokenTagging(Exception):
    '''
    Exception representing there is no :class:`TokenTagging` annotation
    that matches the given criteria in a given concrete object
    '''
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


def get_tokens(tokenization, suppress_warnings=False):
    """Get list of :class:`.Token` objects for a :class:`.Tokenization`

    Return list of Tokens from lattice.cachedBestPath, if Tokenization
    kind is TOKEN_LATTICE; else, return list of Tokens from tokenList.

    Warn and return list of Tokens from tokenList if kind is not set.

    Return None if kind is set but the respective data fields are not.

    Args:
        tokenization (Tokenization): tokenization to extract tokens
            from
        suppress_warnings (bool): True to suppress warning messages
            that `tokenization.kind` is None

    Returns:
        List of :class:`.Token` objects, or `None`

    Raises:
        ValueError: if `tokenization.kind` is not a recognized
            tokenization kind
    """

    if tokenization.kind is None:
        if not suppress_warnings:
            logging.warn('Tokenization.kind is None but is required in '
                         'Concrete; using tokenList')

        token_list = tokenization.tokenList
        if token_list.tokenList is not None:
            return token_list.tokenList

    elif tokenization.kind == TokenizationKind.TOKEN_LATTICE:
        token_lattice = tokenization.lattice
        if token_lattice.cachedBestPath is not None:
            lattice_path = token_lattice.cachedBestPath
            if lattice_path.tokenList is not None:
                return lattice_path.tokenList

    elif tokenization.kind == TokenizationKind.TOKEN_LIST:
        token_list = tokenization.tokenList
        if token_list.tokenList is not None:
            return token_list.tokenList

    else:
        raise ValueError('Unrecognized TokenizationKind %s'
                         % tokenization.kind)

    return None


def get_token_taggings(tokenization, tagging_type, case_sensitive=False):

    """Return list of :class:`.TokenTagging` objects of `taggingType`
    equal to `tagging_type`.

    Args:
        tokenization (Tokenization): tokenization from which taggings
            will be selected
        tagging_type (str): value of `taggingType` to filter to
        case_sensitive (bool): True to do case-sensitive matching
            on `taggingType`.

    Returns:
        List of :class:`.TokenTagging` objects of `taggingType` equal
        to `tagging_type`, in same order as they appeared in the
        tokenization.  If no matching :class:`.TokenTagging` objects
        exist, return an empty list.
    """
    if not tokenization.tokenTaggingList:
        return []
    else:
        return [
            tt for tt in tokenization.tokenTaggingList
            if (
                (tt.taggingType == tagging_type)
                if case_sensitive else
                (tt.taggingType.lower() == tagging_type.lower())
            )
        ]


def get_tagged_tokens(tokenization, tagging_type, tool=None):

    """Return list of :class:`.TaggedToken` objects of taggingType equal
    to tagging_type, if there is a unique choice.

    Args:
        tokenization (Tokenization): tokenization to return
            tagged tokens for
        tagging_type (str): only return tagged tokens for
            :class:`TokenTagging` objects whose `taggingType`
            field is equal to `tagging_type`
        tool (str): If not None, only return tagged tokens for
            :class:`TokenTagging` objects whose `metadata.tool`
            field is equal to `tool`

    Returns:
        List of :class:`.TaggedToken` objects of `taggingType` equal
        to `tagging_type`, if there is a unique choice.

    Raises:
        NoSuchTokenTagging: if there is no matching tagging
        Exception: if there is more than one matching tagging.
    """
    tts = [
        tt
        for tt in get_token_taggings(tokenization, tagging_type)
        if tool is None or tt.metadata.tool.lower() == tool.lower()
    ]
    if len(tts) == 0:
        raise NoSuchTokenTagging('No matching %s tagging.' % tagging_type)
    elif len(tts) == 1:
        return tts[0].taggedTokenList
    else:
        raise Exception('More than one matching %s tagging.' % tagging_type)


def get_lemmas(t, tool=None):
    """
    Returns the result of :func:`get_tagged_tokens` with a
    `tagging_type` of "LEMMA"

    Args:
        t (Tokenization): tokenization to extract tagged tokens from
        tool (str): If not None, only return tagged tokens for
            :class:`TokenTagging` objects whose `metadata.tool`
            field is equal to `tool`

    Returns:
        list of 'LEMMA'-tagged tokens matching `tool` (if specified)
    """
    return get_tagged_tokens(t, 'LEMMA', tool=tool)


def get_pos(t, tool=None):
    """
    Returns the result of :func:`get_tagged_tokens` with a
    `tagging_type` of "LEMMA"

    Args:
        t (Tokenization): tokenization to extract tagged tokens from
        tool (str): If not None, only return tagged tokens for
            :class:`TokenTagging` objects whose `metadata.tool`
            field is equal to `tool`

    Returns:
        list of 'POS'-tagged tokens matching `tool` (if specified)
    """
    return get_tagged_tokens(t, 'POS', tool=tool)


def get_ner(t, tool=None):
    """
    Returns the result of :func:`get_tagged_tokens` with a
    `tagging_type` of "NER"

    Args:
        t (Tokenization): tokenization to extract tagged tokens from
        tool (str): If not None, only return tagged tokens for
            :class:`TokenTagging` objects whose `metadata.tool`
            field is equal to `tool`

    Returns:
        list of 'NER'-tagged tokens matching `tool` (if specified)
    """
    return get_tagged_tokens(t, 'NER', tool=tool)


def plus(x, y):
    """
    Return concatenation of two lists.

    Args:
        x (list):
        y (list)

    Returns:
        list concatenation of x and y
    """
    return x + y


def flatten(a):
    """
    Returned flattened version of input list.

    Args:
        a (list):
    Returns:
        list: Flattened list
    """
    return reduce(plus, a, [])


def get_comm_tokens(comm, sect_pred=None, suppress_warnings=False):
    """Get list of :class:`.Token` objects in :class:`.Communication`.

    Args:
        comm (Communication): communications to extract tokens from
        sect_pred (function): Function that takes a :class:`.Section`
            and returns false if the :class:`.Section` should be
            excluded.
        suppress_warnings (bool): True to suppress warning messages
            that `Tokenization.kind` is None

    Returns:
        List of :class:`.Token` objects in :class:`.Communication`,
        delegating to :func:`get_tokens` for each sentence.
    """
    return flatten(map(
        lambda sect: flatten(map(
            lambda sent: get_tokens(sent.tokenization, suppress_warnings),
            sect.sentenceList
        )),
        filter(sect_pred, comm.sectionList)
        if (sect_pred is not None) else comm.sectionList
    ))


def get_comm_tokenizations(comm, tool=None):
    """Get list of :class:`.Tokenization` objects in a :class:`.Communication`

    Args:
        comm (Communication): communications to extract tokenizations
            from
        tool (str): If not None, only return :class:`.Tokenization`
            objects whose `metadata.tool` field is equal to `tool`

    Returns:
        List of :class:`.Tokenization` objects
    """
    for section in lun(comm.sectionList):
        for sentence in lun(section.sentenceList):
            if tool is None or sentence.tokenization.metadata.tool == tool:
                yield sentence.tokenization


def _lattice_to_fsm(lattice):
    '''
    Return FSM representation of token lattice.

    Args:
        lattice (TokenLattice): the token lattice to process

    Returns:
        tuple containing four items: 0. arcs represented as
        a dictionary from source states to dictionaries from
        destination states to lists of (token, weight) pairs;
        1. arcs represented as a dictionary from destination states to
        dictionaries from source states to lists of (token, weight)
        pairs; 2. the set of tokens; and 3. the set of states.
    '''
    fsm = {}
    bkFsm = {}

    tokens = set()
    states = set()
    for arc in lattice.arcList:
        if arc.src is None:
            raise ValueError('Arc.src must be set')
        src = arc.src

        if arc.dst is None:
            raise ValueError('Arc.dst must be set')
        dst = arc.dst

        if arc.token is None:
            raise ValueError('Arc.token must be set')
        token = arc.token.tokenIndex

        if arc.weight is None:
            raise ValueError('Arc.weight must be set')
        wt = arc.weight

        tokens.add(token)
        states.add(src)
        states.add(dst)

        if src not in fsm:
            fsm[src] = {}
        if dst not in fsm[src]:
            fsm[src][dst] = []
        fsm[src][dst].append((token, wt))

        if dst not in bkFsm:
            bkFsm[dst] = {}
        if src not in bkFsm[dst]:
            bkFsm[dst][src] = []
        bkFsm[dst][src].append((token, wt))

    return (fsm, bkFsm, tokens, states)


def _logsumexp(a):
    '''
    Return log of sum of exponentiations of elements in a.

    Args:
        a: list or vector (of numbers)

    Returns:
        log of sum of exponentiations of elements in a.
    '''
    try:
        from scipy.misc import logsumexp
        return logsumexp(a)
    except ImportError:
        m = max(a)
        return m + log(sum(map(lambda x: exp(x - m), a)))


def _calc_marginal_in_log_prob(fsm, states, start, end):
    """
    Calculate marginal in-log-probability of each state.
    """

    alpha = {}
    alpha[start] = 0.

    state_queue = deque([start])

    while state_queue:
        currState = state_queue.popleft()

        if currState == end:
            continue

        arcs = fsm[currState]

        for (dst, tokenWts) in arcs.items():
            if dst not in alpha:
                state_queue.append(dst)
                alpha[dst] = float('-inf')
            for token, wt in tokenWts:
                alpha[dst] = _logsumexp([alpha[dst], alpha[currState] + wt])

    return alpha


def compute_lattice_expected_counts(lattice):
    """Given a :class:`.TokenLattice` in which the dst, src, token, and
    weight fields are set in each arc, compute and return a list of
    expected token log-probabilities.

    Input arc weights are treated as unnormalized log-probabilities.

    Args:
        lattice (TokenLattice): lattice to compute expected counts for

    Returns:
        List of floats (expected log-probabilities) with the float
        at position i corresponding to the token with tokenIndex i.
    """

    (fsm, bkFsm, tokens, states) = _lattice_to_fsm(lattice)
    alpha = _calc_marginal_in_log_prob(fsm, states,
                                       lattice.startState, lattice.endState)
    beta = _calc_marginal_in_log_prob(bkFsm, states,
                                      lattice.endState, lattice.startState)
    norm = alpha[lattice.endState]

    expectedCounts = {}

    for state in states:
        currState = state

        if currState == lattice.endState:
            continue

        arcs = fsm[currState]

        for dst, tokenWts in arcs.items():
            for token, wt in tokenWts:
                if token not in expectedCounts:
                    expectedCounts[token] = []
                expectedCounts[token].append(
                    alpha[currState] + beta[dst] + wt - norm)

    if expectedCounts:
        return [
            (_logsumexp(expectedCounts[idx]) if idx in expectedCounts else None)
            for idx in range(max(expectedCounts) + 1)
        ]
    else:
        return []


def get_tokenizations(comm, tool=None):
    """
    Returns a flat list of all Tokenization objects in a Communication

    Args:
        comm (Communication): communication to get tokenizations from
        tool (str): if not None, return only tokenizations whose
            `metadata.tool` field matches `tool`

    Returns:
        A list of all Tokenization objects within the Communication
        matching `tool` (if it is not None)
    """
    tokenizations = []

    if comm.sectionList:
        for section in comm.sectionList:
            if section.sentenceList:
                for sentence in section.sentenceList:
                    if sentence.tokenization:
                        if (tool is None or
                                sentence.tokenization.metadata.tool == tool):
                            tokenizations.append(sentence.tokenization)
    return tokenizations
