from regexgen import to_fuzzy_regEx
from regexgen.fuzzy.util import string_to_fuzzy_string
from regexgen.fuzzy.util import replace_fuzzystring_with_regex
from regexgen.fuzzy.patterns import MatchWord
from regexgen.fuzzy.regEx import NonMinimalRegEx


class TestNonminimalFuzzy():
    def test_fuzzymatch(self):
        word1 = "123qwe1.23"
        word2 = "df12"

        match_word1 = MatchWord(word1)
        match_word2 = MatchWord(word2)

        regEx = NonMinimalRegEx()
        regEx.add_word(match_word1)
        regEx.add_word(match_word2)

        assert str(regEx) == r'/(?:\d{3}\w{3}\d.\d{2})|(?:\w{2}\d{2})/'

    def test_fuzzymatch_singleword(self):
        word1 = "asd"
        match_word1 = MatchWord(word1)
        regEx = NonMinimalRegEx()
        regEx.add_word(match_word1)
        res = str(regEx)
        assert res == r'/(?:\w{3})/', res


class TestFuzzyStringGeneration():
    def test_string_generation(self):
        s = "123..123.bdf)asd"
        res = string_to_fuzzy_string(s)
        assert res == "000..000.aaa)aaa"


class TestFuzzyStringReplacement():
    def test_string_generation(self):
        """
        The minimisation will put out aa? This is a regex!
        ? has to be excaped if it is a char in that sense
        """
        s = "aa?"
        res = replace_fuzzystring_with_regex(s)
        assert res == r"\w\w?"
        s = "aa\?"
        res = replace_fuzzystring_with_regex(s)
        assert res == r"\w{2}\?"


class TestFuzzyRegEx():
    def test_fuzzy_string_finding(self):
        strings = ["123", "123"]
        res = to_fuzzy_regEx(strings)
        assert r"/\d{3}/" == res, res

    def test_fuzzy_string_alternation(self):
        strings = ["123", "asd"]
        res = to_fuzzy_regEx(strings)
        assert (r"/(?:\w{3}|\d{3})/" ==
                res) or (r"/(?:\d{3}|\w{3})/" == res), res


class TestSpecialChars():

    def test_correctHandlingOfSpecialChars(self):
        """
        Make sure all special characters are escaped
        """
        strings = ["123+", "asd?"]
        res = to_fuzzy_regEx(strings)
        assert (r"/(?:\w{3}\?|\d{3}\+)/" ==
                res) or (r"/(?:\d{3}\+|\w{3}\?)/" == res), res

        strings = ["123", "123?"]
        res = to_fuzzy_regEx(strings)
        assert res == "/\d{3}(?:\?)?/"
