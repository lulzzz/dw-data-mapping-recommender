from src.formatter.formatter import Formatter


class RecommenderFormatter(Formatter):
    def format(self, tokenized_sentences):
        sentences = []
        for tokenized_sentence in tokenized_sentences:
            sentence = ' '.join(tokenized_sentence)
            sentences.append(sentence)

        return sentences

