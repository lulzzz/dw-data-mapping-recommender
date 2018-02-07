import gensim
import collections


class Recommender(object):
    def __init__(self):
        self.model = gensim.models.KeyedVectors.load_word2vec_format('../datasets/GoogleNews-vectors-negative300.bin',
                                                                     binary=True)

    def recommend(self, sentence, recommendations):
        distances = []
        recomendation_result = collections.defaultdict(dict)
        for word_to_recommend in recommendations:
            distances.append(
                self._calculate_distance(first_sentence=sentence,
                                         second_sentence=word_to_recommend))
        for word, probability in zip(recommendations, distances):
            recomendation_result[sentence][word] = probability

        return recomendation_result

    def _calculate_distance(self, first_sentence, second_sentence):
        distance = self.model.wmdistance(first_sentence, second_sentence)

        return distance
