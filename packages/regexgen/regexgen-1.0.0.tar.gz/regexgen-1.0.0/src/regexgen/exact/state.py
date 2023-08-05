from typing import Type


class StringIsNotCharError(Exception):
    pass


class State():
    def __init__(self, hash_value=0):
        self.accepting = False  # is final state
        self.outgoing = {}  # char -> state; only one to one
        # char -> list(state) : there can be more than one state that transitions into self with a char
        self.incoming = {}
        self.hash_value = hash_value

    def get_sub_tree(self, visited=None):
        if visited is None:
            visited = []
        if self in visited:
            return  # this happens in the minimal tree when 2 branches lead to the same finalstate

        visited.append(self)
        for state in self.outgoing.values():
            _ = state.get_sub_tree(visited)
        return visited

    def __hash__(self): return self.hash_value

    def __eq__(self, other):
        if other == None:
            return False
        return self.hash_value == other.hash_value

    def force_char(self, string: str):
        """ make sure the string is a char and not empty (epsilon transitions)"""
        if len(string) != 1 and not r"\\" == string[0]:
            raise StringIsNotCharError(
                f"State:: did not get a valid char. Got a string of length {len(string)}. :: {string}")
        return string

    def has_outgoing(self, string: str):
        """ check if this state has this transition already"""
        char = self.force_char(string)
        return char in self.outgoing.keys()

    def add_outgoing(self, char, state):
        """
        map char -> other state
        @return the state this transition leads to
        which is either a new one or an existing one
        """
        if self.has_outgoing(char):
            print(
                f"WARNING state: {self.hash_value} already has a tansition on {char}")
        else:
            self.outgoing[char] = state

    def add_incoming(self, char, state):
        """
        add an incoming transition
        map: char -> Set(states)  where this can come from
        such that the transitions will be grouped by char
        """
        if char in self.incoming.keys():
            self.incoming[char].append(state)
        else:
            self.incoming[char] = [state]

    def print_subtree(self):
        print("----------------------------------------------------")
        for char, state in self.outgoing.items():
            print(
                f"{self.hash_value}-{char}->{state.hash_value} accepting: {state.accepting}")
            state.print_subtree()
