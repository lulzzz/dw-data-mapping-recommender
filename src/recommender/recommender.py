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

        for metric_name in metric_results.values():
            for word in recommendations:
                recomendation_result[sentence][word] = list(metric_name.values())

        return recomendation_result
