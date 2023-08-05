import numpy as np
from regexgen.exact.expressions import Literal
from regexgen.exact.operators import union, concat, star


def trie_to_regex(root):

    # use Ardens Lemma to solve the DFA
    # https://cs.stackexchange.com/questions/2016/how-to-convert-finite-automata-to-regular-expressions#2392
    # A represents a state transition table for the given DFA.
    # Example:
    # strings: 'a', 'b'
    # q0 -a-> q1 -b-> (q2)      # () means accepting (final) state
    # Equations:
    #     q2 = b q1
    #     q1 = a q0
    #     q2 = b (a q0) = ba q0
    # thus our regEx = 'ba'
    # Ardens Lemma comes into the game once a state has a transition to itself

    # the order is critical here
    states = root.get_sub_tree()
    size = len(states)

    # A map from state i->j
    A = np.empty(shape=(size, size), dtype=object)

    # B is a vector of accepting states in the DFA, marked as epsilons.
    B = np.empty(shape=size, dtype=object)

    # set up the system of equations
    for i, state in enumerate(states):
        if state.accepting:
            B[i] = Literal('')  # epsilons
        for tran, target_state in state.outgoing.items():
            if target_state not in states:
                continue  # old state before minimisation #TODO remove
            j = states.index(target_state)
            if A[i][j] is None:
                A[i][j] = Literal(tran)
            else:
                A[i][j] = union(A[i][j], Literal(tran))

    # Solve the of equations
    # we append the result to B starting from epsilon (empty string)
    for n in reversed(range(size)):
        # use Ardens Lemma for transitions onto the same state (n->n)
        if not A[n][n] is None:
            B[n] = concat(star(A[n][n]), B[n])
            for j in range(n):
                A[n][j] = concat(star(A[n][n]), A[n][j])

        for i in range(n):
            if not A[i][n] is None:
                # mark i as a final state if it leads to a final state
                # then merge the state it leads to into i
                B[i] = union(B[i], concat(A[i][n], B[n]))
                for j in range(n):
                    A[i][j] = union(A[i][j], concat(A[i][n], A[n][j]))
    return f"/{str(B[0])}/"
