from typing import List

from regexgen.exact.state import State
import re


class TrieBuilder():
    """
    Trie structure for strings.
    Each string will be represented by a branch.
    Character in the string represent connections between the states of the automaton.

    Example:
    strings: lala, lal0
    states: $q_i$

    q0 →'l'→ q1 →'a'→ q2 →'l'→ q3 →'a'→ q4
                                ↳ '0'→ q5

    q0    : root
    q4,q5 : accepting (final) states

    Note that this tree would not be minimal,
    the final states can be merged. Hence we have to minimise this.

    """

    def __init__(self, strings, debug=False):
        self.debug = debug
        self.root = State(0)
        self.state_count = 1  # used to hash the states, 0 is root
        self.all_states = [self.root]
        self.alphabet = set()
        self.add_strings(strings)

    def add_string(self, string: str):
        """
        Add a string to the trie.
        The last state will be a final state
        """
        previous_state = self.root
        for char in string:
            # if the transition already exists
            # just walk along the edges of the graph
            # this saves some steps in the minimisation
            if char in previous_state.outgoing.keys():
                previous_state = previous_state.outgoing[char]
            else:
                self.alphabet.add(char)  # populate $\Sigma$
                new_state = State(self.state_count)
                self.state_count += 1
                previous_state.add_outgoing(char, new_state)
                new_state.add_incoming(char, previous_state)
                if self.debug:
                    print(
                        f"Added {char} {previous_state.hash_value}->{new_state.hash_value}")
                self.all_states.append(new_state)
                previous_state = new_state
        previous_state.accepting = True  # mark last as final state

    def add_strings(self, strings: List[str]):
        """ add a bunch of strings """
        for string in strings:
            self.add_string(string)
