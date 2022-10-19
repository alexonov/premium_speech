import random
from nltk.corpus import wordnet as wn
from itertools import islice


TOTAL_NOUNS = 82_115


def main():
    # ind = random.randint(0, TOTAL_NOUNS)
    # print(ind)
    # random_noun,  = islice(wn.all_synsets('n'), ind, ind+1)

    random_noun = wn.synsets('measure')[1]

    print(random_noun)
    print(random_noun.definition())
    print(random_noun.hypernyms())
    print(random_noun.hyponyms())


if __name__ == '__main__':
    main()
