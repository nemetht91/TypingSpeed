import random

WORDS_fILE = "assets/words.txt"


class Words:
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

    def get_random_word(self):
        if not self.words:
            return None
        return random.choice(self.words)


words = Words()
print(words.get_random_word())