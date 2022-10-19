from nltk.corpus import gutenberg
from random import choice


BOOKS = gutenberg.fileids()


def get_text(name=None):
    name = name or choice(BOOKS)
    return gutenberg.raw(name)


def get_random_snippet(name=None, snippet_max_length=500):
    text = get_text(name)
    start_pos = choice(range(len(text)))
    snippet_raw = text[start_pos:start_pos + snippet_max_length]
    return snippet_raw
