from regexgen import to_regEx

class TestUsingThePackage():
    def test_string_to_regex(self):
        res = to_regEx(["My", "hovercraft", "is", "full", "of", "eels"])
        assert "(?:i|eel)s" in res
        #assert (res == "/(?:My|of|full|(?:i|eel)s|hovercraft)/") or (res == "/(?:of|My|full|(?:i|eel)s|hovercraft)/") or (res=="/(?:My|of|full|hovercraft|(?:i|eel)s)/")