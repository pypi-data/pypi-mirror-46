import re


class StringMatcher(object):

    pattern = "@string@"

    @classmethod
    def match(self, value):
        return type(value) == str and not not re.search(r"^.+$", value)
