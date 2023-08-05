from difflib import SequenceMatcher
from regexgen.expressions import Literal, Repetition, Concatenation, Char, Alternation
class UnionOfStringError(Exception):
    pass

def star(expression): 
    if expression is None: return None
    return Repetition(expression, '*')

def concat(exp1, exp2): 
    """
    A.B  or in other words   A dot B
    Implements the concat of to expressions:
    'a', 'b' -> 'ab'
    """
    if exp1 is None or exp2 is None: return None
    if exp1.is_empty() and not exp2.is_empty(): return exp2
    if exp2.is_empty() and not exp1.is_empty(): return exp1

    if isinstance(exp1, Literal) and isinstance(exp2, Literal):
        return Literal(f"{exp1}{exp2}")

    if isinstance(exp1, Literal) and isinstance(exp2, Concatenation) and isinstance(exp2.right, Literal):
        return Concatenation(Literal(str(exp1) + str(exp2.left)), str(exp2.right.value))

    if isinstance(exp2, Literal) and isinstance(exp1, Concatenation) and isinstance(exp1.right, Literal):
        return Concatenation(str(exp1.right.value), Literal(str(exp1.left.value) + str(exp2.value))) 

    return Concatenation(exp1, exp2)

def get_common_substring(exp1, exp2):
    """
    returns the LONGEST substring in both strings
    """
    string1 = str(exp1)
    string2 = str(exp2)
    match_id1, _, match_len = SequenceMatcher(None, string1, string2).find_longest_match(0, len(string1), 0, len(string2))
    if match_len == 0: return None
    return string1[match_id1 : match_id1+match_len]

def remove_common_substring(exp1, exp2):
    """
    remove longest common substring and 
    strip leading and ending whitespace.
    """
    if exp1 is None or exp2 is None: return exp1, exp2, None, False
    overlap = get_common_substring(exp1, exp2)
    if overlap is None: return exp1, exp2, None, False
    if exp1.starts_with(overlap) and exp2.starts_with(overlap):
        new_exp1 = exp1.remove_substring("start", overlap)
        new_exp2 = exp2.remove_substring("start", overlap)
        return new_exp1, new_exp2, overlap, True
    if exp1.ends_with(overlap) and exp2.ends_with(overlap):
        new_exp1 = exp1.remove_substring("end", overlap)
        new_exp2 = exp2.remove_substring("end", overlap)
        return new_exp1, new_exp2, overlap, False
    return exp1, exp2, None, False


def union(exp1_in, exp2_in): 
    """
    Implements the + operator also called union.
    """

    if exp1_in is None and exp2_in is None: 
        return None
    if exp1_in is None and not exp2_in is None: 
        return exp2_in  
    if not exp1_in is None and exp2_in is None: 
        return exp1_in 

    exp1 = exp1_in
    exp2 = exp2_in

    removed_end = False
    removed_start = False
    exp1, exp2, removed_s, is_start = remove_common_substring(exp1, exp2)
    if removed_s:
        if is_start:
            removed_start = removed_s
        else:
            removed_end = removed_s
        # if we can remove one end, we can maybe remove another string at the opposite end
        exp1, exp2, removed_s, is_start = remove_common_substring(exp1, exp2)
        if removed_s: 
            if is_start:
                removed_start = removed_s
            else:
                removed_end = removed_s

    res = None

    # if one is empty that means the other is an optional ''+'a' = a?
    if exp1.is_empty() or exp2.is_empty():
        if exp1.is_empty():
            res = Repetition(exp2, "?" )
        elif (isinstance(exp1, Repetition) and exp1.repetition_type == "*"):
            res = exp1
        elif (isinstance(exp2, Repetition) and exp2.repetition_type == "*"):
            res = exp2
        else:
            res = Repetition(exp1, "?" )
    elif (isinstance(exp1, Repetition) and exp1.repetition_type == "?"):
        rep_type = exp2.repetition_type if hasattr(exp2, 'repetition_type') else "?" 
        res = Repetition(Alternation([exp1.value, exp2]), rep_type)
    elif (isinstance(exp2, Repetition) and exp2.repetition_type == "?"):
        rep_type = exp2.repetition_type if hasattr(exp2, 'repetition_type') else "?" 
        res = Repetition(Alternation([exp1, exp2.value]), rep_type)
    else:
        # 'ab', 'c' -> [a-c]
        if exp1.is_character() and exp2.is_character():
            res = Char(exp1, exp2)
        else:
            res = Alternation(options = [exp1, exp2])

    # add the common substring again
    if removed_end: res = Concatenation(res, Literal(removed_end))
    if removed_start: res = Concatenation(Literal(removed_start), res)

    return res


def is_purely_char(string):
    """
    return True if input string consists only of chars
    """
    for char in string:
        ordinal = ord(char)
        if ordinal > 122 return False
        if ordinal < 65 return False
        

