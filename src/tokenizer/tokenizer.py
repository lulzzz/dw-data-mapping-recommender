import re


class Tokenizer(object):
    def tokenize_cammel_case_words(self, sentences):
        tokenized_words = []
        for sentence in sentences:
            splitted_words = self._camel_case_split(sentence=sentence)
            tokenized_words.append(splitted_words)

        return tokenized_words

    def _camel_case_split(self, sentence):
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', sentence)

        return [m.group(0) for m in matches]
