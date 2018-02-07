import re


class Tokenizer(object):
    def tokenize_by(self, sentences, method):
        return getattr(self, method)(sentences=sentences)

    def cammel_case_words(self, sentences):
        tokenized_words = []
        for sentence in sentences:
            splitted_words = self._camel_case_split(sentence=sentence)
            tokenized_words.append(splitted_words)

        return tokenized_words

    def _camel_case_split(self, sentence):
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', sentence)

        return [m.group(0) for m in matches]

    def split_by(self, tokens, delimiter):
        splitted_tokens = []
        for token in tokens:
            splitted_token = token.split(delimiter)
            # joined_splitted_sentence = ' '.join(splitted_sentence)
            # splitted_sentences.append(joined_splitted_sentence)
            splitted_tokens.extend(splitted_token)

        return splitted_tokens

    def normalize_tokens(self, tokens):
        normalized_tokens = []
        for token in tokens:
            normalized_tokens.append(token.lower())

        return normalized_tokens
