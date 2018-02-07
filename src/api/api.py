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
            recommended_words = []
            input_1_tokenized_words = tokenizer.tokenize_by(sentences=mapping['input'], method='cammel_case_words')
            output_1_tokenized_words = tokenizer.tokenize_by(sentences=mapping['output'], method='cammel_case_words')

            processed_input_sentences_tokens = []
            processed_output_sentences_tokens = []
            for input_tokens in input_1_tokenized_words:
                input_1_tokenized_words = tokenizer.split_by(tokens=input_tokens, delimiter="/")
                input_1_tokenized_words = tokenizer.normalize_tokens(tokens=input_1_tokenized_words)
                processed_input_sentences_tokens.append(input_1_tokenized_words)
            for output_tokens in output_1_tokenized_words:
                output_1_tokenized_words = tokenizer.split_by(tokens=output_tokens, delimiter="/")
                output_1_tokenized_words = tokenizer.normalize_tokens(tokens=output_1_tokenized_words)
                processed_output_sentences_tokens.append(output_1_tokenized_words)

            processed_input_sentences = recommender_formatter.format(
                tokenized_sentences=processed_input_sentences_tokens)
            processed_output_sentences = recommender_formatter.format(
                tokenized_sentences=processed_output_sentences_tokens)

            for input_sentence in processed_input_sentences:
                recommended_words.append(
                    recommender.recommend(sentence=input_sentence,
                                          recommendations=processed_output_sentences))

        return jsonify(recommended_words)


api.add_resource(DwRecommender, '/recommender')

if __name__ == '__main__':
    app.run(debug=True)
