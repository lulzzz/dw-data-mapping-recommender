import collections

from src.math_stuff.math_is_great_again import MathIsGreatAgain


class Recommender(object):
    def __init__(self, recommendation_metrics):
        self.math_is_great_again = MathIsGreatAgain()
        self.recommendation_metrics = recommendation_metrics

    def recommend(self, sentence, recommendations):
        metric_results = collections.defaultdict(dict)
        recomendation_result = collections.defaultdict(dict)

        for recommendation_metric in self.recommendation_metrics:
            similarity_distance = self.math_is_great_again.softmax(
                recommendation_metric(sentence=sentence, corpus=recommendations)).tolist()
            metric_results[sentence][recommendation_metric.__name__] = similarity_distance

        for word, metric_result in zip(recommendations, metric_results.values()):
            for k, v in metric_result.values():
                recomendation_result[sentence][word] = metric_result

        return recomendation_result
