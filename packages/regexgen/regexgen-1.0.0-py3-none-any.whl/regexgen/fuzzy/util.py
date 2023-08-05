from regexgen.fuzzy.patterns import MatchWordFromFuzzyRegEx

def string_to_fuzzy_string(string):
    """
    Turn a string `abc`->`aaa` (\w{3}) 
    into a string representing the lietrals we want to use 
    `abc.123`->`aaa.000` 
    so that we can minimize this for our regex
    """
    new_string = r""
    for char in string:
        if char.isalpha():
            new_string += "a"
            continue
        if char.isdigit():
            new_string += "0"
            continue
        # for special characters
        new_string += char
    return new_string

def replace_fuzzystring_with_regex(string):
    """
    Replace series of char with matching regex
    Ignore special chars like `.` `(` etc.
    "0000...000()abc" -> "\d{4}...\d{3}()\w(3)" 
    """
    return f"{str(MatchWordFromFuzzyRegEx(string))}"
