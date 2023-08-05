import pytest

from regexgen.exact.operators import union, concat, get_common_substring, remove_common_substring
from regexgen.exact.expressions import Literal, Repetition, Concatenation

class TestUnionOperator():
    def test_union(self):

        u = union(Literal("Parker"), Literal("Peter"))
        assert str(u) == 'P(?:et|ark)er', str(u)

        u = union(Literal("Tom"), 
                  Literal("Tommy"))
        assert str(u) == 'Tom(?:my)?', str(u)

        u = union(Literal("as"), Literal('a'))
        assert str(u)=='as?', str(u)

        u = union(Literal('a'), None)
        assert str(u) == 'a', str(u)

        u = union(None, Literal('a'))
        assert str(u) == 'a', str(u)

        u = union(Repetition(Literal("as"), repetition_type="*"), Literal("as"))
        assert str(u) == 'as*', str(u)

        u = union(Literal(''), Literal('a'))
        assert str(u) == 'a?', str(u)

        u = union(Repetition(Literal("a"), repetition_type="*"), Literal("a"))
        assert str(u) == 'a*', str(u) 

class TestDotOperator():
    def test_dotoperator(self):
        res  = concat(Literal("a"), Concatenation(Repetition("b","?"), Literal("c")))
        assert str(res) == "ab?c"
    def test_compressionsOfregex(self):
        pass
        #TODO implement this feature
        #e1 = Repetition(Literal("a"), "*")
        #e2 = Literal("a")
        #c = concat(e1, e2)
        #assert str(c) == "a+"

class TestCommonSubstring():
    def test_commonsubtring(self):
        s1 = Literal("Peter Pater dog cat hold")
        s2 = Literal("peter Peter dog cat horse")
        match = get_common_substring(s1, s2)
        assert match == 'ter dog cat ho'
        s1 = ""
        s2 = "asdasd"
        match = get_common_substring(s1, s2)
        assert match is None

class TestRemoveCommonSubstring():
    def test_removeCommonSubstring(self):
        # TODO 
        # implement remove_common_substring
        pass
