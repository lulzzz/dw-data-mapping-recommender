from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource

from src.formatter.recommender_formatter import RecommenderFormatter
from src.recommender.recommender import Recommender
from src.tokenizer.tokenizer import Tokenizer

app = Flask(__name__)
api = Api(app)

recommender = Recommender()
tokenizer = Tokenizer()
recommender_formatter = RecommenderFormatter()


class DwRecommender(Resource):
    def get(self):
        return "Hello World!"

    def post(self):
        json = request.get_json()
        mappings = json['mappings']
        for mapping in mappings:
            input_1_tokenized_words = tokenizer.tokenize_cammel_case_words(sentences=mapping['input'])
            output_1_tokenized_words = tokenizer.tokenize_cammel_case_words(sentences=mapping['output'])

            input_1_recommender_sentences_dict = recommender_formatter.format(tokenized_words=input_1_tokenized_words)
            output_1_recommender_sentence_dict = recommender_formatter.format(tokenized_words=output_1_tokenized_words)

            recommended_words = []
            for sentence_dict in input_1_recommender_sentences_dict:
                # TODO: I THINK THE RECOMMEND DOESNT NEED TO KNOW ABOUT THE DICT STRUCTURE AND JUST RECEIVE A SENTENCE AND A LIST OF SENTENCES
                recommended_words.append(
                    recommender.recommend(sentence_dict=sentence_dict,
                                          recommendation_list=output_1_recommender_sentence_dict))

        return jsonify(recommended_words)


api.add_resource(DwRecommender, '/recommender')

if __name__ == '__main__':
    app.run(debug=True)
