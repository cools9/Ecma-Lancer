import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import random

class Study_stuff:
    nltk.download('punkt')
    nltk.download('wordnet')

    def add_punctuation(sentence):
        punctuation = ['.', '!', '?']
        sentence = sentence.strip()
        if not sentence.endswith(tuple(punctuation)):
            sentence += random.choice(punctuation)
        return sentence

    def add_newline(sentence, words_per_line=10):
        words = word_tokenize(sentence)
        lines = []
        for i in range(0, len(words), words_per_line):
            line = ' '.join(words[i:i+words_per_line])
            lines.append(line)
        return '\n'.join(lines)

    def count_words(sentence):
        words = word_tokenize(sentence)
        num_words = len(words)
        return num_words

    def shorten_sentence(sentence, max_length=None):
        if max_length is None:
            max_length = count_words(sentence) // 2
        words = word_tokenize(sentence)
        if len(words) <= max_length:
            return sentence
        shortened_words = words[:max_length]
        shortened_sentence = ' '.join(shortened_words)
        return add_newline(add_punctuation(shortened_sentence))

    def sentence_longer(sentence):
        """Makes a sentence longer by adding synonyms and related words.

        Args:
            sentence: The sentence to make longer.

        Returns:
            A longer version of the sentence.
        """

        # Tokenize the sentence.
        tokens = word_tokenize(sentence)

        # Find synonyms and related words for each token.
        synonyms = []
        for token in tokens:
            synonyms.extend(wordnet.synsets(token))

        # Create a new sentence by adding synonyms and related words.
        new_sentence = sentence
        for synonym in synonyms:
            if synonym.lemmas()[0].name() not in tokens:
                new_sentence += ' ' + synonym.lemmas()[0].name()

        return new_sentence

