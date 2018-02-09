import collections
import numpy as np

from flask import Flask, request, jsonify
from flask_restful import Api, Resource

from src.classifiers.classifiers import MaximumProbabilityClassifier
from src.formatter.recommender_formatter import RecommenderFormatter
from src.parser.sample_pairs_parser import SamplePairsParser
from src.recommender.recommender import Recommender
from src.tokenizer.tokenizer import Tokenizer

app = Flask(__name__)
api = Api(app)

recommender = Recommender()
tokenizer = Tokenizer()
recommender_formatter = RecommenderFormatter()
maximum_probability_classifier = MaximumProbabilityClassifier()


class DwRecommender(Resource):
    def get(self):
        return "Hello World!"

    def post(self):
        json = request.get_json()
        X = [json['incoming']]
        y = [json['expected']]

        recommended_words = maximum_probability_classifier.classify(X=X, y=y, recommender=recommender)

        # parsed_recommended_words = collections.defaultdict(dict)
        # i = 0
        # for s in recommended_words:
        #     for (key, value) in s.items():
        #         for (_key, _value) in value.items():
        #
        #             parsed_y = tokenizer.tokenize_by(sentences=y, method='cammel_case_words')
        #             processed_input_sentences_tokens = []
        #             for _y_p in parsed_y:
        #                 parsed_y = tokenizer.split_by(tokens=_y_p, delimiter="/")
        #                 parsed_y = tokenizer.normalize_tokens(tokens=parsed_y)
        #                 processed_input_sentences_tokens.append(parsed_y)
        #
        #             parsed_recommended_words[X[0][i]][_key] = _value
        #     i += 1

        return jsonify(recommended_words)


class xxx(Resource):
    def post(self):
        sample_pairs_parser = SamplePairsParser()
        dataframe = sample_pairs_parser.parse(path='raw-datasets/sample_most_recent_pairs.xlsx')
        dataframe = dataframe[(dataframe.Feedback == 'OK')]
        number_of_dataweave_scripts = dataframe.block_num.nunique()

        X = []
        y = []
        for i in range(number_of_dataweave_scripts):
            if not dataframe[(dataframe.block_num == (i + 1))]['map_from'].empty:
                X.append(dataframe[(dataframe.block_num == (i + 1))]['map_from'])
                y.append(dataframe[(dataframe.block_num == (i + 1))]['map_to'])

        aux_X = []
        aux_y = []
        for _X, _y in zip(X, y):
            if len(_X) > 15:
                aux_X.append(_X[:15])
                aux_y.append(_y[:15])
            else:
                aux_X.append(_X)
                aux_y.append(_y)

        X = aux_X
        y = aux_y

        score = maximum_probability_classifier.score(X=X, y=y, recommender=recommender)

        mean = np.mean(score)
        std = np.std(score)

        return "Performance metric: Accuracy. Mean: {}, STD: {}".format(mean, std)


api.add_resource(DwRecommender, '/recommender')
api.add_resource(xxx, '/compareAlgorithms')

if __name__ == '__main__':
    app.run(debug=False)
