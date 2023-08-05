import copy
from regexgen.exact.state import State

def mini(trie):
    root = trie.root

    states = set(trie.all_states)
    finalstates = list(filter(lambda state: state.accepting, states))

    # P are the equivalenz-classes
    # if two states fall into the same class they can be merged in the minimal DFA
    # in the beginning we know for sure the final states are one equivalenz-class
    P = set([frozenset(finalstates), frozenset(states.difference(finalstates))])
    W = set(P) 

    while len(W) > 0:
        # A := one removed set, first iteration: final states as these are clearly different from the rest
        A = W.pop() 
        for c in trie.alphabet: # := sigma

            # X:= set of states with transition on c into A
            X = set()
            for state in A:
                if c in state.incoming.keys():
                    for source_state in state.incoming[c]:
                        X.add(source_state)
            #if len(X) == 0 :continue

            P_copy = copy.copy(P) # we want to change P while we loop it
            for Y in P_copy:
                i = X.intersection(Y) # |X ∩ Y|
                d = Y.difference(X)   # |Y \ X|
                if len(i) == 0 : continue
                if len(d) == 0 : continue

                # replace Y with i and d
                P.remove(Y) 
                P.add(frozenset(i))
                P.add(frozenset(d))

                if Y in W:
                    W.remove(Y)
                    W.add(frozenset(i))
                    W.add(frozenset(d))
                else: 
                    if len(i) <= len(d):
                        W.add(frozenset(i)) 
                    else:
                        W.add(frozenset(d))

    # the states s in S now resemble equivalenz classes, 
    # meaning that any state s in S is representative of the whole set S. 
    # They have the same or equivalent outgoing transitions.
    # The minimal automation then is any state in S, the transitions in 
    # the new automaton must be set from S_i->S_j, so from a set in P to another set in P


    new_states = []
    new_root = None
    for i_S, S in enumerate(P):
        new_state  = State(i_S)
        if root in S:
            new_root = new_state
        new_states.append(new_state)

    for i_S, S in enumerate(P):
        new_state = new_states[i_S]
        for s in S:
            if s.accepting == True: new_state.accepting= True
            for char, target_state in s.outgoing.items():
                target_index = None
                for class_index, eq_class in enumerate(P):
                    if target_state in eq_class:
                        target_index = class_index
                    if target_index != None:
                        new_state.outgoing[char] = new_states[target_index]
    assert new_root != None, "Root None after minimisation this shouldnt happen."

    return new_root

