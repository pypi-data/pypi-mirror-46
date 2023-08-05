# regexgen
Package to calculate a regEx that minimally represents a set of strings.

Example:

    exact matching:
        "Peter" , "Parker" -> "/P(?:et|ark)er/"
    
    fuzzy matching:
        "Peter" , "Parker" -> (?:\\w{5})|(?:\\w{6})

Transforms the the strings into an automaton, minimizes the automaton and finally turns the automaton back into a string.
- case sensitive
- emojis not suported/tested

## Installation
sh install.sh

## Usage
    # exact matching of strings
    # if you put in "abc" this will only match exactly the characters
    import regexgen
    result = regexgen.to_regEx(["My", "hovercraft", "is", "full", "of", "eels"])
    result = "/(?:My|of|full|(?:i|eel)s|hovercraft)/" # order is random

    # fuzzy matching of patterns
    # matches chars and digits 
    # "asd123" -> "\w{3}\d{3}"
    from regexgen import to_fuzzy_regEx
    strings = ["123", "asd"]
    res = to_fuzzy_regEx(strings)
    res = "/(?:\w{3}|\d{3})/"

