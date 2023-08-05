class NonMinimalRegEx():
    def __init__(self):
        self.match_words = []

    def add_word(self, word):
        self.match_words.append(word)

    def get_expression(self):
        """
        get the RegEx #TODO use python regEx obj?

        """
        return self.logical_or_str(self.match_words)

    def logical_or_str(self, patterns):
        """
        Nonminimal regEx just the logical of of the options we have.
        """
        return "|".join([f"(?:{str(word)})" for word in patterns])

    def __str__(self):
        return f"/{self.get_expression()}/"


class MinimalFuzzyRegEx():
    def __init__(self, strings=None):
        self.words = []
        if not strings is None:
            self.words = strings

    def add_words(self, word):
        self.words.append(word)

    def get_fuzzy_strings(self):
        from regexgen.fuzzy.util import string_to_fuzzy_string
        return [string_to_fuzzy_string(input_string) for input_string in self.words]

    def minimise(self):
        """
        For the fuzzy minimisation we just build dummies to have the 3 different classes of chars
        (alpha, numeric, special) represented by the same char, except the special one is just the char.
        For example `abc+-!?123`->'aaa\+\-\!\?111',

        This way we dont have to rewrite all the exact operators.
        """
        from regexgen.exact.brzozowski import trie_to_regex
        from regexgen.exact.hopcroft import mini
        from regexgen.exact.trie import TrieBuilder
        return trie_to_regex(mini(TrieBuilder(self.get_fuzzy_strings())))

    def __str__(self):
        from regexgen.fuzzy.util import replace_fuzzystring_with_regex
        minimal_fuzzy_str = self.minimise()
        return replace_fuzzystring_with_regex(minimal_fuzzy_str)
