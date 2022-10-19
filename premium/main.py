import random
from enum import Enum
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import WordNetError
from pprint import pprint
from premium.brown import get_text, pretty_format
from tools import preprocess


def recursive_lemmas(word, pos, max_depth=3, current_level=0) -> list:
    """
    collects all the lemmas of a word recursively
    limited by the recursion depth
    :param pos:
    :param word:
    :param max_depth:
    :param current_level:
    :return:
    """
    result = []

    # reached required depth - stop
    if current_level > max_depth:
        return result
    else:
        # 1. get all synsets of the word
        lemma_names = []
        for synset in wn.synsets(word, pos):

            # take part of speech from the first synset if it's not given
            pos = pos or synset.pos()

            lemma_names += [lemma.name() for lemma in synset.lemmas()]
        unique_lemmas = list(set(lemma_names))
        return list(set(unique_lemmas + [l for ll in unique_lemmas for l in recursive_lemmas(ll, pos, max_depth, current_level+1)]))


SYNONYMS_CACHE = {}


def get_synonyms(word, pos=None, depth=1) -> list:
    try:
        return SYNONYMS_CACHE[(word, pos, depth)]
    except KeyError:
        lemmas = recursive_lemmas(word, max_depth=depth, pos=pos)
        SYNONYMS_CACHE[(word, pos, depth)] = [l for l in lemmas if l != word and '_' not in l]
        return SYNONYMS_CACHE[(word, pos, depth)]


class SimilarityMethod(Enum):
    PATH = 'path_similarity'
    LEACOCK_CHODOROW = 'lch_similarity'
    WU_PALMER = 'wup_similarity'

    def __str__(self):
        return self.value


def get_similarity(word_a: str, word_b: str, pos: str, method: SimilarityMethod = SimilarityMethod.PATH) -> dict:
    """
    gets the highest possible similarity
    by comparing all possible synsets between each other
    :param pos:
    :param method:
    :param word_a:
    :param word_b:
    :return:
    """
    def _similarity(obj_a, obj_b):
        similarity_func = getattr(obj_a, str(method))
        return similarity_func(obj_b)

    scores = []
    for synset_a in wn.synsets(word_a, pos):
        for synset_b in wn.synsets(word_b, pos):
            try:
                scores.append(_similarity(synset_a, synset_b))
            except WordNetError:
                pass

    return max(scores)


def get_synonym_scores(word, pos, method=SimilarityMethod.PATH):
    synonyms = get_synonyms(word, pos)
    return {s: get_similarity(word, s, pos=pos, method=method) for s in synonyms}


def test():
    word = 'express'
    pos = wn.VERB

    synonyms = get_synonyms(word, pos, 1)

    print(f'Original word: {word}')

    for sim_type in SimilarityMethod:
        print('\n')
        print(f'Similarity: {sim_type}')
        scores = {s: get_similarity(word, s, pos=pos, method=sim_type) for s in synonyms}
        pprint(scores)


POS_WEIGHTS = {
    'RB': 0,  # "Adverb", e.g. 'However', 'unequivocally', 'far', 'primarily'
    'VBN': 0,  # "Verb, past participle", e.g. 'burned', 'continued', 'killed', 'formed'
    'VBD': 0,  # "Verb, past tense", e.g. 'worked', 'had', 'suggested', 'led'
    'VB': 0.5,  # "Verb, base form", e.g. 'wish', 'congratulate', 'help', 'turn'
    'VBZ': 0,  # "Verb,3rd ps. sing. present", e.g. 'Defends', 'sounds', 'waits', 'has'
    'NNS': 0,  # "Noun, plural", e.g. 'troops', 'automobiles', 'automobiles', 'customers'
    'JJ': 0.5,  # "Adjective", e.g. 'efficient', 'horrible', 'quiet'
    'NN': 0.5,  # "Noun, singular or masps", e.g. 'town', 'editor', 'police', 'city'
    'NNP': 0,  # "Noun, plural"
    'JJR': 0,  # "Adjective, comparative", e.g. 'fewer', 'less', 'fewer', 'bigger'
    'RBS': 0,  # "Adverb, superlative", e.g. 'most'
    'VBG': 0,  # "Verb, gerund/present participle", e.g. 'cleaning', 'shopping', 'carrying', 'hogging'
}

POS_MAPPING = {
    'RB': wn.ADV,
    'VBN': wn.VERB,
    'VBD': wn.VERB,
    'VB': wn.VERB,
    'VBZ': wn.VERB,
    'NNS': wn.NOUN,
    'JJ': wn.ADJ,
    'NN': wn.NOUN,
    'JJR': wn.ADJ,
    'RBS': wn.ADV,
    'VBG': wn.VERB,
    'NNP': wn.NOUN
}


Word = str
PartOfSpeech = str


def make_token_rigid(token: tuple[Word, PartOfSpeech], rigidness=0.5, highlighter=None):
    weight = POS_WEIGHTS.get(token[1], 0)
    word = token[0]

    if random.random() > (1 - weight):
        pos = POS_MAPPING[token[1]]

        synonym_scores = get_synonym_scores(word=word, pos=pos)

        if synonym_scores:
            # randomly for now, apply rigidness factor later
            new_word = random.choice(list(synonym_scores.keys()))
            if highlighter is not None:
                new_word = highlighter(new_word, word)
            return new_word
        else:
            return word
    else:
        return word


def apply_premium_speak(text, rigidness=0.5, highlighter=None):
    sentences = preprocess(text)
    rigid_words = [make_token_rigid(t, rigidness=rigidness, highlighter=highlighter) for s in sentences for t in s]
    return ' '.join(rigid_words)


def main():
    words = get_text()
    text = ' '.join(words)

    print(pretty_format(text))

    rigid_text = apply_premium_speak(text)

    print(pretty_format(rigid_text))


if __name__ == '__main__':
    main()
