import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import inflect
from typing import NamedTuple
import spacy


stop_words_list = set(stopwords.words('english'))

p = inflect.engine()

sp = spacy.load('en_core_web_sm')


txt = """I live in a house near the mountains. I have two brothers and one sister, and I was born last. My father
teaches mathematics, and my mother is a nurse at a big hospital. My brothers are very smart and
work hard in school. My sister is a nervous girl, but she is very kind. My grandmother also lives with us.
She came from Italy when I was two years old. She has grown old, but she is still very strong. She
cooks the best food!
My family is very important to me. We do lots of things together. My brothers and I like to go on long
walks in the mountains. My sister likes to cook with my grandmother. On the weekends we all play
board games together. We laugh and always have a good time. I love my family very much."""


# sent_tokenize is one of instances of
# PunktSentenceTokenizer from the nltk.tokenize.punkt module


class Token(NamedTuple):
    word: str
    pos: str

    def __repr__(self):
        return f'{self.word}: {self.pos}'


def tokenize_nltk(text):
    tokenized = sent_tokenize(text)
    result = []
    for i in tokenized:
        # Word tokenizers is used to find the words
        # and punctuation in a string
        wordsList = nltk.word_tokenize(i)

        # Using a Tagger. Which is part-of-speech
        # tagger or POS-tagger.
        tagged = nltk.pos_tag(wordsList)

        # adding tag for stopwords
        tagged = [Token(*token) if token[0] not in stop_words_list else Token(token[0], 'STOP') for token in tagged]

        result.append(tagged)

    return result


def make_singular_noun(word):
    return p.singular_noun(word)


def transform_verb():
    from pattern.text.en import conjugate, lemma, lexeme, PRESENT, SG
    try:
        print(lexeme('gave'))
    except:
        pass
    print(lemma('gave'))
    print(lexeme('gave'))
    print(conjugate(verb='give', tense=PRESENT, number=SG))  # he / she / it


def tokenize_spacy(text):
    pass


if __name__ == '__main__':
    # sentences = tokenize_nltk(txt)
    #
    # print(sentences)
    #
    # for sentence in sentences:
    #     for token in sentence:
    #         if token.pos == 'NNS':
    #             print(f'{token.word} -> {make_singular_noun(token.word)}')
    transform_verb()