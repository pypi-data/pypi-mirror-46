from regexgen.exact.expressions import Literal, Repetition, Concatenation, Char, Alternation


class TestAlteration():
    def test_alteration(self):
        alt = Alternation(options= [Alternation(options=[Literal("Inner"),
                                                 Literal("Inner"),
                                                 Literal("Inner2~!&")]),
                            Literal("Outer"),
                            Literal("Outer2"),
                            Literal("Inner")
                           ])
        #FIXME the order here is not deterministic meh
        #assert str(alt) == "(?:Outer|Inner|Outer2|Inner2~!&)", str(alt)

        alt = Alternation(options= [Alternation(options=[Literal("a"),
                                                         Literal("b")]),
                                    Literal("a"),
                                   ])
        assert (str(alt) == '(?:a|b)') or (str(alt) == '(?:b|a)'),  str(alt)

        alt = Alternation(options= [Alternation(options=[Literal("abc"),
                                                         Literal("def")]),
                                    Literal("degfgh"),
                                   ])
        #assert str(alt) == '(?:abc|def|degfgh)', str(alt)

class TestChar():
    def test_char(self):
        #TODO this covers not all cases there is still something weird

        char = Char(Literal("a"), Literal("b"))
        assert str(char) == '[ab]'

        char = Char(Literal("a"), Literal("a"))
        assert str(char) == '[a]'

        char = Char(Char(Literal("a"),
                         Literal("b")),
                    Literal("c"))
        assert str(char) ==   '[a-c]'

        char = Char(Char(Literal("a"), Literal("b")), Char(Literal("f"), Literal("g")))

        assert str(char) ==   '[abfg]'

        ################### Test the string function
        c = Char("a", "b") # doesnt matter here

        s = c.to_string(s = set(['c']))
        assert s == '[c]'

        s = c.to_string(s = set(['c', 'f']))
        assert s == '[cf]'

        s = c.to_string(s = set(['a', 'b', 'c']))
        assert s == '[a-c]'

        s = c.to_string(s = set(['a', 'b', 'c', 'd', 'g', 'i','j','k','z']))
        assert s == '[a-dgi-kz]'

        s = c.to_string(s = set(['a', 'b', 'c', 'd', 'g', 'i','j','k','z']))
        assert s == '[a-dgi-kz]'

        s = c.to_string(s = set(['a', 'b', 'c', 'd', 'g', 'i','j','k','z', '0','1','2','3','9']))
        assert s == '[0-39a-dgi-kz]'



class TestConcatenartion():
    def test_concatenation(self):
        l1 = Literal("a")
        l2 = Literal("b")
        assert str(Concatenation(l1, l2)) == 'ab'

        l1 = Literal("a")
        l2 = Literal("")
        assert str(Concatenation(l1, l2)) == 'a'

        l1 = Literal("a")
        l2 = Literal("b")
        l3 = Literal("c")
        c = Concatenation(l1, l2)
        c = Concatenation(c, l3)
        assert 'abc' == str(c)

        r = Repetition(Literal("ab"), "*")
        l = Literal("c")
        c = Concatenation(r, l)
        assert str(c) == '(?:ab)*c'

        l1 = Literal("abs")
        l2 = Literal("def")
        assert str(Concatenation(l1, l2)) == 'absdef'

        r = Repetition(Literal("a"), "?")
        l = Literal("c")
        c = Concatenation(r, l)
        str(c) == 'a?c'
        assert str(c) == 'a?c'

class TestRepetition():
    def test_repetition(self):
        r = Repetition(Literal("a"), repetition_type='*')
        assert str(r) == 'a*'

        r = Repetition(Literal("ab"), repetition_type='*')
        assert str(r) == '(?:ab)*'

        r = Repetition(Literal("ab"), repetition_type='?')
        assert str(r) == '(?:ab)?'

        r = Repetition(Literal("a"), repetition_type='?')
        assert str(r) == 'a?'