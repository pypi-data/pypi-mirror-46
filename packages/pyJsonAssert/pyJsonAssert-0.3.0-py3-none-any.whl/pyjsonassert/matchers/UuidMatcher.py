import re
from . import StringMatcher


class UuidMatcher(object):

    pattern = "@uuid@"

    @staticmethod
    def match(value):
        return StringMatcher.match(value) and not not re.search(r"^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$", value)
