import re

_RE_COMBINE_WHITESPACE = re.compile(r"(?a:\s+)")
_RE_STRIP_WHITESPACE = re.compile(r"(?a:^\s+|\s+$)")


def remove_unknown_charset(elem):
    elem = re.sub(r'[^\x00-\x7F]+', '', elem)
    elem = _RE_COMBINE_WHITESPACE.sub(" ", elem)
    elem = _RE_STRIP_WHITESPACE.sub("", elem)

    if elem == "" or elem.isspace():
        elem = None

    return elem