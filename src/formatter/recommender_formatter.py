from src.formatter.formatter import Formatter


class RecommenderFormatter(Formatter):
    def format(self, tokenized_words):
        dicts_of_words = []
        for tokenized_word in tokenized_words:
            sentence = ' '.join(tokenized_word)
            dicts_of_words.append({'sentence': sentence})

        return dicts_of_words

