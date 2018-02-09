from sklearn.metrics import accuracy_score

from src.formatter.recommender_formatter import RecommenderFormatter
from src.tokenizer.tokenizer import Tokenizer

tokenizer = Tokenizer()
recommender_formatter = RecommenderFormatter()


class MaximumProbabilityClassifier(object):
    def classify(self, X, y, recommender):
        recommended_dataset_words = []

        for _X, _y in zip(X, y):
            recommended_words = []
            input_1_tokenized_words = tokenizer.tokenize_by(sentences=_X, method='cammel_case_words')
            output_1_tokenized_words = tokenizer.tokenize_by(sentences=_y, method='cammel_case_words')

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
            recommended_dataset_words.append(recommended_words)

        return recommended_dataset_words

    def score(self, X, y, recommender):
        classifications = self.classify(X=X, y=y, recommender=recommender)
        maximum_probability_results = []
        for classification in classifications:
            maximum_probability_results.append(self.get_maximum_probability_sentences(sentences=classification))

        accuracy_scores = []
        for i in range(len(y)):
            accuracy_scores.append(accuracy_score(y[i], maximum_probability_results[i]))

        return accuracy_scores

    def get_maximum_probability_sentences(self, sentences):
        result = []
        for sentence in sentences:
            aux = []
            for (key, value) in sentence.items():
                minumum_value_key = max(value, key=lambda key: value[key])
                # minimum_value_value = value[min(value, key=lambda a: a[1])]
                aux.append(minumum_value_key)
            result.extend(aux)

        return result
