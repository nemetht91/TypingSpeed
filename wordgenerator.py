import random

WORDS_fILE = "assets/words.txt"


class WordGenerator:
    def __init__(self):
        self.words_file = WORDS_fILE
        self.words = self._get_words_list()

    def _open_file(self):
        try:
            with open(self.words_file) as file:
                return file.read()
        except FileNotFoundError:
            return None

    def _get_words_list(self):
        raw_text = self._open_file()
        if raw_text is None:
            return []
        return raw_text.split("\n")

    def get_word(self):
        if not self.words:
            return None
        return random.choice(self.words)

    def get_word_list(self, number_of_words):
        words = []
        for i in range(number_of_words):
            words.append(self.get_word())
        return words

    def get_word_matrix(self, rows, columns):
        matrix = []
        for i in range(rows):
            matrix.append(self.get_word_list(columns))
        return matrix

