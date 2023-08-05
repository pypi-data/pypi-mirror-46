

class Pattern():
    def __init__(self, length): self.length = length

    def increment(self): self.length += 1


class DigitPattern(Pattern):
    def __init__(self, length): super().__init__(length)

    def __str__(self):
        if self.length > 1:
            return f"\d{{{self.length}}}"
        return r"\d"

    def __eq__(self, other):
        return (self.length == other.length) and\
            isinstance(other, DigitPattern)


class WordPattern(Pattern):
    def __init__(self, length): super().__init__(length)

    def __str__(self):
        if self.length > 1:
            return f"\w{{{self.length}}}"
        return r"\w"

    def __eq__(self, other):
        return (self.length == other.length) and\
            isinstance(other, WordPattern)


class SpecialPattern(Pattern):
    """
    Essentially everything that is not char or numeric.
    It does not hurt to escape all special characters.
    "." -> "\."
    """

    def __init__(self, char):
        super().__init__(length=1)
        self.char = char

    def __eq__(self, other):
        same_char = str(self) == str(other)
        same_length = self.length == other.length
        return same_char and same_length

    def __str__(self):
        return self.char


class MatchWord():
    def __init__(self, string):
        self.length = len(string)
        self.string = string

        self.patterns = []
        self.determine_pattern(string)

    def determine_pattern(self, word):
        patterns = []
        last_pattern = None
        for char in word:
            if char.isalpha():
                if isinstance(last_pattern, WordPattern):
                    last_pattern.increment()
                else:
                    if not last_pattern is None:
                        patterns.append(last_pattern)
                    last_pattern = WordPattern(1)
                continue
            if char.isdigit():
                if isinstance(last_pattern, DigitPattern):
                    last_pattern.increment()
                else:
                    if not last_pattern is None:
                        patterns.append(last_pattern)
                    last_pattern = DigitPattern(1)
                continue

            if not last_pattern is None:
                patterns.append(last_pattern)

            # fall back to special cases
            last_pattern = SpecialPattern(char)

        if not last_pattern is None:
            patterns.append(last_pattern)
        self.patterns = patterns

    def __str__(self):
        string = r""
        for pattern in self.patterns:
            string += str(pattern)
        return string


class MatchWordFromFuzzyRegEx(MatchWord):
    """"
    Matchword pattern that may contain a regEx.
    `aaa?` -> `\w{2}\w?`
    """

    def __init__(self, string):
        super().__init__(string)

    def determine_pattern(self, word):
        patterns = []
        last_pattern = None
        word_len = len(word)
        for index, char in enumerate(word):
            # if a character in [a-z] is followed by a question mark we assume
            # this is a regex, unless it is excaped
            next_index = index + 1
            prev_index = index - 1
            next_char = ""
            prev_char = ""
            if next_index < word_len:
                next_char = word[next_index]
            if prev_index >= 0:
                prev_char = word[prev_index]
            if char.isalpha():
                if isinstance(last_pattern, WordPattern):
                    if not next_char == "?":
                        last_pattern.increment()
                    else:
                        if not last_pattern is None:
                            patterns.append(last_pattern)
                        last_pattern = WordPattern(1)
                else:
                    if not last_pattern is None:
                        patterns.append(last_pattern)
                    last_pattern = WordPattern(1)
                continue
            if char.isdigit():
                if isinstance(last_pattern, DigitPattern):
                    if not next_char == "?":
                        last_pattern.increment()
                    else:
                        if not last_pattern is None:
                            patterns.append(last_pattern)
                        last_pattern = DigitPattern(1)
                else:
                    if not last_pattern is None:
                        patterns.append(last_pattern)
                    last_pattern = DigitPattern(1)
                continue

            if not last_pattern is None:
                patterns.append(last_pattern)

            # fall back to special cases
            last_pattern = SpecialPattern(char)

        if not last_pattern is None:
            patterns.append(last_pattern)
        self.patterns = patterns
