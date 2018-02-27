from fuzzywuzzy import fuzz
from gensim.similarities import WmdSimilarity

from src.math_stuff.math_is_great_again import MathIsGreatAgain

math_is_great_again = MathIsGreatAgain()


class ShallowExtractors(object):
    def __init__(self, model):
        self.model = model

    def calculate_similarity_distance(self, sentence, corpus):
        # length_sentence = len(sentence.split(" "))
        # minimum_length_corpus_sentence = len(min(corpus, key=lambda a: len(a.split(" "))).split(" "))
        #
        # new_corpus = []
        # if minimum_length_corpus_sentence > length_sentence:
        #     for c in corpus:
        #         new_corpus.append(" ".join(c.split(" ")[-length_sentence:]))
        #     new_sentence = " ".join(sentence.split(" ")[-length_sentence:])
        #     corpus = new_corpus
        #     sentence = new_sentence
        # else:
        #     for c in corpus:
        #         new_corpus.append(" ".join(c.split(" ")[-minimum_length_corpus_sentence:]))
        #     new_sentence = " ".join(sentence.split(" ")[-minimum_length_corpus_sentence:])
        #     corpus = new_corpus
        #     sentence = new_sentence

        # if len(corpus) > 10:
        #     similarities = []
        #     similarity_query_response = WmdSimilarity(corpus, self.model, normalize_w2v_and_replace=False,
        #                                               num_best=10)
        #     similarity_query_answer = similarity_query_response[sentence]
        #     for i in range(10):
        #         similarities.append(similarity_query_answer[i][1])
        # else:
        #     similarity_query_response = WmdSimilarity(corpus, self.model, normalize_w2v_and_replace=False)
        #     similarities = similarity_query_response[sentence]

        similarity_query_response = WmdSimilarity(corpus, self.model, normalize_w2v_and_replace=False)
        similarities = similarity_query_response[sentence]

        return math_is_great_again.softmax(similarities)

    # Actually not using it
    def calculate_raw_distance(self, first_sentence, second_sentence):
        distance = self.model.wmdistance(first_sentence, second_sentence)

        return distance

    # TODO: PLEASE REFACTOR!!
    def edit_distance_ratio(self, sentence, corpus):
        fuzzy_ratios = []

        for word in corpus:
            fuzzy_ratios.append(fuzz.ratio(sentence, word))

        similarities = self._make_fuzzy_great_again(fuzzy_ratios)

        return math_is_great_again.softmax(similarities)

    def edit_distance_partial_ratio(self, sentence, corpus):
        fuzzy_ratios = []

        for word in corpus:
            fuzzy_ratios.append(fuzz.partial_ratio(sentence, word))

        similarities = self._make_fuzzy_great_again(fuzzy_ratios)

        return math_is_great_again.softmax(similarities)

    def edit_distance_token_set_ratio(self, sentence, corpus):
        fuzzy_ratios = []

        for word in corpus:
            fuzzy_ratios.append(fuzz.token_set_ratio(sentence, word))

        similarities = self._make_fuzzy_great_again(fuzzy_ratios)

        return math_is_great_again.softmax(similarities)

    def _make_fuzzy_great_again(self, fuzzy_ratios):
        great_fuzzy_ratios = []

        for fuzzy_ratio in fuzzy_ratios:
            great_fuzzy_ratio = fuzzy_ratio / 100
            great_fuzzy_ratios.append(great_fuzzy_ratio)

        return great_fuzzy_ratios
