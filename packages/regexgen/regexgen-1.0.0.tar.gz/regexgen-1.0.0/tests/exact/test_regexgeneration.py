
from regexgen.exact.brzozowski import trie_to_regex
from regexgen.exact.hopcroft import mini
from regexgen.exact.trie import TrieBuilder
from regexgen import to_regEx


class TestRegExGeneration():
    def test_regexgen(self):
        input_strings = ["0", "c", ]
        res = trie_to_regex(mini(TrieBuilder(input_strings)))
        assert ("/[0c]/" == str(res)) or ("/[c0]/" ==
                                          str(res)), f"Result : `{str(res)}`"

        input_strings = ["foo", "foo", ]
        res = trie_to_regex(mini(TrieBuilder(input_strings)))
        assert str(res) == "/foo/", f"Result : `{str(res)}`"

        input_strings = ["ab", "c", ]
        res = trie_to_regex(mini(TrieBuilder(input_strings)))
        assert (
            str(res) == '/(?:c|ab)/') or ('/(?:ab|c)/'), f"Result : `{str(res)}`"

        input_strings = ["ab", "cd", ]
        res = trie_to_regex(mini(TrieBuilder(input_strings)))
        assert (
            str(res) == '/(?:ab|cd)/') or ('/(?:cd|ab)/'), f"Result : `{str(res)}`"

        input_strings = ["barf", "bar", ]
        res = trie_to_regex(mini(TrieBuilder(input_strings)))
        assert (str(res) == '/barf?/'), f"Result : `{str(res)}`"

        input_strings = ["foo", "bar", ]
        root = mini(TrieBuilder(input_strings))
        res = trie_to_regex(root)
        assert (res == "/(?:foo|bar)/") or (res == "/(?:bar|foo)/")

        input_strings = ["abc", "ac", ]
        root = mini(TrieBuilder(input_strings))
        res = trie_to_regex(root)
        assert res == "/ab?c/"

        input_strings = ["barfoobar", "foobarzap", "foobar"]
        root = mini(TrieBuilder(input_strings))
        res = trie_to_regex(root)
        assert res == "/(?:barfoobar|foobar(?:zap)?)/"

        input_strings = ["Peter", "Parker", ]
        root = mini(TrieBuilder(input_strings))
        res = trie_to_regex(root)
        assert res == "/P(?:et|ark)er/"

        # FIXME
        input_strings = ["c", 'b', 'd', "D"]
        res = trie_to_regex(mini(TrieBuilder(input_strings)))
        print(res)


class TestExactWithSpecialChars():
    def test_special_chars(self):
        # the backslash is not escaped here
        # it also does not escape the others.
        # its a normal backslash
        strings = [r"\|", r"\+"]
        res = to_regEx(strings)
        assert res == (r"/\\(?:\||\+)/") or (res == r"/\\(?:\+|\|)/"), res
