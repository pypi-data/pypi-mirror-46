__all__ = []
from typing import List
from regexgen.exact.brzozowski import trie_to_regex
from regexgen.exact.hopcroft import mini
from regexgen.exact.trie import TrieBuilder
from regexgen.fuzzy.regEx import MinimalFuzzyRegEx
import re


def to_regEx(input_strings: List[str]) -> str:
    """
    Exact matching of a set of strings
    - Turn set strings into an automaton.

    - Minimise the automaton using Hopcrofts algorithm.
    https://en.wikipedia.org/wiki/DFA_minimization

    - Turn the minimal automaton (DFA) into regex using Brzozowski's algebraic method.
    http://cs.stackexchange.com/questions/2016/how-to-convert-finite-automata-to-regular-expressions#2392

    returns a string: 'a', 'b', 'c' -> "/[a-c]/"
    """

    assert type(input_strings) == list
    return trie_to_regex(mini(TrieBuilder(input_strings)))


def to_fuzzy_regEx(input_strings: List[str]) -> str:
    """
    Turn a list of strings into a fuzzy regex.
    Fuzzy in this context means that this does not match single characters but groups of them.

    Example:
        Peter, Parker -> Exact: /P(?:et|ark)er/
                      -> Fuzzy: /(?:\w{5}\w.)/ (dot means one more)
    """
    assert type(input_strings) == list
    regex = MinimalFuzzyRegEx(input_strings)
    return str(regex)
