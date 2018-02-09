import gensim
import collections
import numpy as np
from gensim.similarities import WmdSimilarity


class Recommender(object):
    def __init__(self):
        self.model = gensim.models.KeyedVectors.load_word2vec_format('datasets/GoogleNews-vectors-negative300.bin',
                                                                     binary=True)
        self.model.init_sims(replace=True)

    def recommend(self, sentence, recommendations):
        similarity_distances = []
        recomendation_result = collections.defaultdict(dict)

        similarity_distances.extend(
            self.softmax(self._calculate_similarity_distance(sentence=sentence, corpus=recommendations)).tolist())

        for word, probability in zip(recommendations, similarity_distances):
            recomendation_result[sentence][word] = probability

        return recomendation_result

    def _calculate_similarity_distance(self, sentence, corpus):
        length_sentence = len(sentence.split(" "))
        minimum_length_corpus_sentence = len(min(corpus, key=lambda a: len(a.split(" "))).split(" "))

        new_corpus = []
        if minimum_length_corpus_sentence > length_sentence:
            for c in corpus:
                new_corpus.append(" ".join(c.split(" ")[-length_sentence:]))
            new_sentence = " ".join(sentence.split(" ")[-length_sentence:])
            corpus = new_corpus
            sentence = new_sentence
        else:
            for c in corpus:
                new_corpus.append(" ".join(c.split(" ")[-minimum_length_corpus_sentence:]))
            new_sentence = " ".join(sentence.split(" ")[-minimum_length_corpus_sentence:])
            corpus = new_corpus
            sentence = new_sentence

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

        # for i in len(similarities):
        #     print('sim = %.4f' % similarities[i][1])
        #     result.append(corpus[similarities[i][0]])
        #     result.append(similarities[i][1])

        return similarities

    def _calculate_raw_distance(self, first_sentence, second_sentence):
        distance = self.model.wmdistance(first_sentence, second_sentence)

        return distance

    def softmax(self, x):
        """Compute softmax values for each sets of scores in x."""
        return np.exp(x) / np.sum(np.exp(x), axis=0)
