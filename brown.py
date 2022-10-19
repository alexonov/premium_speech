from nltk.corpus import brown
from random import choice, seed

seed(8)

CATEGORIES = brown.categories()


def get_category():
    return choice(CATEGORIES)


def get_text(category=None):
    category = category or get_category()
    filename = choice(brown.fileids(categories=category))
    return brown.words(fileids=filename)


def pretty_format(s):
    length = 100
    formatted = ''
    for i in range(0, len(s), length):
        formatted += s[i:i+length] + '\n'
    return formatted


if __name__ == '__main__':
    category = 'romance'
    print(category)

    text = get_text()
    text = ' '.join(text)
    text = pretty_format(text)
    print(text)
