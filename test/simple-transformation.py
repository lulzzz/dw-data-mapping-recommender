from src.formatter.recommender_formatter import RecommenderFormatter
from src.recommender.recommender import Recommender
from src.tokenizer.tokenizer import Tokenizer

input_1 = ["body", "listAllFlightsResponse", "return", "airlineName", "code", "departureDate", "destination",
           "emptySeats", "origin", "planeType", "price", "attributes", "protocolHeaders", "variables"]

output_1 = ["airline", "flightCode", "fromAirportCode", "toAirportCode", "departureDate", "emptySeats", "price",
            "planeType"]

tokenizer = Tokenizer()
input_1_tokenized_words = tokenizer.tokenize_cammel_case_words(sentences=input_1)
output_1_tokenized_words = tokenizer.tokenize_cammel_case_words(sentences=output_1)

recommender_formatter = RecommenderFormatter()
input_1_recommender_sentences_dict = recommender_formatter.format(tokenized_words=input_1_tokenized_words)
output_1_recommender_sentence_dict = recommender_formatter.format(tokenized_words=output_1_tokenized_words)

recommender = Recommender()
recommended_words = []
for sentence_dict in input_1_recommender_sentences_dict:
    # TODO: I THINK THE RECOMMEND DOESNT NEED TO KNOW ABOUT THE DICT STRUCTURE AND JUST RECEIVE A SENTENCE AND A LIST OF SENTENCES
    recommended_words.append(
        recommender.recommend(sentence_dict=sentence_dict, recommendation_list=output_1_recommender_sentence_dict))

print(recommended_words)
