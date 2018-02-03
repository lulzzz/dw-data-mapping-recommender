import gensim
import collections


class Recommender(object):
    def __init__(self):
        self.model = gensim.models.KeyedVectors.load_word2vec_format('../datasets/GoogleNews-vectors-negative300.bin',
                                                                     binary=True)

    def recommend(self, sentence_dict, recommendation_list):
        probabilities = []
        for word_to_recommend in recommendation_list:
            probabilities.append(
                self._calculate_distance(first_sentence=sentence_dict['sentence'],
                                         second_sentence=word_to_recommend['sentence']))
        recomendation_result = collections.defaultdict(dict)
        for word, probability in zip(recommendation_list, probabilities):
            recomendation_result[sentence_dict['sentence']][word['sentence']] = probability

        return recomendation_result

    def _calculate_distance(self, first_sentence, second_sentence):
        distance = self.model.wmdistance(first_sentence, second_sentence)

        return distance
