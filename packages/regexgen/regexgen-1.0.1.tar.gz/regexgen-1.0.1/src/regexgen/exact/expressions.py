from typing import Type
from regexgen.exact.state import State


class InvalidStringError(Exception):
    pass


class InvalidRepetitionType(Exception):
    pass


class Expression():
    def __init__(self, precedence=None):
        self.precedence = precedence

    def __str__(self): raise NotImplementedError()

    def __len__(self): raise NotImplementedError()

    def __iter__(self): return self

    def is_empty(self): return len(self.__str__()) == 0

    def is_character(self):
        string = self.__str__()
        valid_char = string.isalpha() or string.isdigit()
        return len(string) == 1 and valid_char

    def parens(self, expr: 'Expression', parent: 'Expression') -> str:
        if isinstance(expr, str):
            return expr

        string = str(expr)
        # TODO this is a hack to fix alternations
        # Alternation would not get () if we dont put them
        # in the string method of Alternation
        # Why?
        if string.startswith("(?:") and string.endswith(")"):
            return string

        length = len(string)
        if (length == 0) or (length == 1) or expr.is_character():
            return string

        if (expr.precedence < parent.precedence):
            return f"(?:{string})"

        return string


class Literal(Expression):
    """
    Literal for example a string : `Peter` or a char '0'
    """

    def __init__(self, value=None, precedence=2):
        super().__init__(precedence)
        self.value = value

    def __len__(self): return len(self.value)

    def __eq__(self, other):
        if isinstance(other, Literal):
            return self.value == other.value
        return False

    def __hash__(self): return hash(self.value)

    def __str__(self):
        string = str(self.value)
        # we want to escape every special character
        if (len(string) == 1) and not string.isalpha() and not string.isdigit():
            return f"\{string}"
        return string

    def replace_string(self, what, with_what):
        self.value = str(self.value).replace(what, with_what)

    def get_literal(self): return self.value

    def starts_with(self, string):
        res = str(self.value).startswith(string)
        return res

    def ends_with(self, string):
        return str(self.value).endswith(string)

    def remove_substring(self, side, to_remove):
        string = str(self.value)
        if side == "start":
            if string.startswith(to_remove):
                return Literal(string.replace(to_remove, ""))
            else:
                print(
                    f"WARNING could not remove `{to_remove}` from `{string}`")

        elif side == "end":
            if string.endswith(to_remove):
                return Literal(string.replace(to_remove, ""))
            else:
                print(
                    f"WARNING could not remove `{to_remove}` from `{string}`")
        else:
            raise InvalidStringError(
                "Parameter 'side' must be ether 'start' or 'end'.")


class Repetition(Expression):
    """
    Represents a repetition (e.g. `a*` or `a?`)
    """

    def __init__(self, value, repetition_type, precedence=3):
        super().__init__(precedence)
        self.value = value
        if repetition_type not in ["*", "?"]:
            raise InvalidRepetitionType("Valid repitions types are: '*', '?' ")

        self.repetition_type = repetition_type

    def starts_with(self, string): return str(self.value).startswith(string)

    def ends_with(self, string): return str(self.value).endswith(string)

    def __str__(self):
        return self.parens(expr=self.value, parent=self) +\
            str(self.repetition_type)

    def remove_substring(self, side, to_remove):
        string = str(self.value)
        if side == "start":
            if string.startswith(to_remove):
                return Repetition(value=string.replace(to_remove, ""),
                                  repetition_type=self.repetition_type)
            else:
                print(
                    f"WARNING could not remove `{to_remove}` from `{string}`")
        elif side == "end":
            if string.endswith(to_remove):
                return Repetition(value=string.replace(to_remove, ""),
                                  repetition_type=self.repetition_type)
            else:
                print(
                    f"WARNING could not remove `{to_remove}` from `{string}`")
        else:
            raise InvalidStringError(
                "Parameter 'side' must be ether 'start' or 'end'.")


class Concatenation(Expression):
    def __init__(self, left_exp, right_exp, precedence=2):
        """
        Concatenated strings/chars
        'a'+'b' = 'ab'
        'a' + '' = a?
        """
        super().__init__(precedence=precedence)
        self.left = left_exp
        self.right = right_exp

    def __len__(self): return len(str(self.left)) + len(str(self.right))

    def __str__(self): return str(self.left) + str(self.right)

    def starts_with(self, string): return str(self.left).startswith(string)

    def ends_with(self, string): return str(self.right).endswith(string)

    def get_literal(self, side):
        if side == "start":
            return str(self.left)
        elif side == "end":
            return str(self.right)
        else:
            raise InvalidStringError(
                "Parameter 'side' must be ether 'start' or 'end'.")

    def set_value(self, value, side):
        if side == "start":
            self.left.value = Literal(value)
        elif side == "end":
            self.right.value = Literal(value)
        else:
            raise InvalidStringError(
                "Parameter 'side' must be ether 'start' or 'end'.")

    def remove_substring(self, side, string):
        if side == "start":
            return Concatenation(
                left_exp=self.left.remove_substring(side, string),
                right_exp=self.right)
        elif side == "end":
            return Concatenation(
                right_exp=self.right.remove_substring(side, string),
                left_exp=self.left)
        else:
            raise InvalidStringError(
                "Parameter 'side' must be ether 'start' or 'end'.")


class Char(Expression):
    """
    Single char representation
    'a', 'b' -> [ab]
    '[ab]' 'c' -> [a-c]
    '[a-c]',  [e-f] -> [a-ce-f]
    TODO there is a bug where the result is something [-ac]
    numbers can be treated as chars as well
    """

    def __init__(self, exp1, exp2, precedence=1):
        super().__init__(precedence=precedence)
        self.first = str(exp1)
        self.last = str(exp2)
        self.string = ""
        self.alphabet = set()

        if isinstance(exp1, Char):
            self.first = self.first.replace("[", "").replace("]", "")
        if isinstance(exp2, Char):
            self.last = self.last.replace("[", "").replace("]", "")

        for char in self.first:
            self.alphabet.add(char)
        for char in self.last:
            self.alphabet.add(char)

    def to_string(self, s):
        """
        convert a set of char to a regex describing any of them:
        [a cdef z] -> [ac-fz]
        """
        sorted_s = sorted(s)
        sorted_ascii = [ord(char) for char in sorted_s]
        if len(sorted_ascii) > 2:
            distances = [sorted_ascii[i+1]-sorted_ascii[i]
                         for i in range(len(sorted_ascii)-1)]
            # this shift is helpful to make the loop simple
            distances.insert(0, 0)
            subgroups = []
            last_el = ""
            for index, dist in enumerate(distances):
                if dist == 1:
                    last_el += sorted_s[index]
                else:
                    if not last_el == '':
                        subgroups.append(last_el)
                    last_el = sorted_s[index]
            if len(last_el) > 1:
                subgroups.append(last_el)
            if distances[-1] == 1:  # special treatment for last element
                if len(subgroups) > 0 and len(subgroups[-1]) == 1:
                    subgroups[-1] += last_el
            else:
                subgroups.append(last_el)
            new_subgroups = []
            for subgroup in subgroups:  # remove intemediate 'abc'->'a-c'
                if len(subgroup) > 2:
                    first = subgroup[0]
                    last = subgroup[-1]
                    subgroup = f"{first}-{last}"
                new_subgroups.append(subgroup)
            return f"[{''.join(new_subgroups)}]"
        else:
            return f"[{''.join(sorted_s)}]"

    def __str__(self):
        return self.to_string(self.alphabet)

    def __len__(self): return 1

    def has(self, char):
        if not len(char) == 1:
            return False
        if char in self.alphabet:
            return True
        else:
            return False
        return False

    def starts_with(self, string): return False

    def ends_with(self, string): return False

    def is_character(self): return True


class Alternation(Expression):
    """
    Represents an alternation (e.g. `foo|bar`)
    """

    def __init__(self, options, precedence=1):
        """
        options: unique list of expressions that can be alternated
                 [Literal, ...]
        """
        super().__init__(precedence=precedence)
        self.options = sorted(options, key=len)
        self.options = self.flatten_options()

    def starts_with(self, string):
        for option in self.options:
            if str(option).startswith(string):
                continue
            else:
                return False
        return True

    def ends_with(self, string):
        for option in self.options:
            if str(option).endswith(string):
                continue
            else:
                return False
        return True

    def remove_substring(self, side, string):
        newoptions = []
        for option in self.options:
            new_option = option.remove_substring(side, string)
            newoptions.append(new_option)
        return Alternation(options=newoptions)

    def flatten_options(self):
        """
        collapse all expressions that are alternations themselves
        and return the new (unique) list
        """
        new_options = set()
        for option in self.options:
            if isinstance(option, Alternation):
                sub_options = option.flatten_options()
                for sub_option in sub_options:
                    new_options.add(sub_option)
            else:
                new_options.add(option)

        return sorted(new_options, key=len)

    def __len__(self): return len(str(self.options[0]))  # longest option

    def is_character(self): return False

    def __str__(self):
        """ put '|' between all the possible expressions """
        s = "|".join([self.parens(expr, parent=self) for expr in self.options])
        # TODO this is a potential problem see parens() in Expression()
        return f"(?:{s})"
