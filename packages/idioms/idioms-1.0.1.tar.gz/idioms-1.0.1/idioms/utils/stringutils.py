import re


def tabs_to_spaces(s):
    return re.sub(r"\t", r"    ", s)