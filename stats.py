class Stat:
    def __init__(self, text: str, is_correct: bool):
        self.text = text
        self.is_correct = is_correct


class Statistics:
    def __init__(self):
        self.letters: list[Stat] = []
        self.words: list[Stat] = []

    def add_letters(self, letter: str, is_correct: bool):
        new_letter_stat = Stat(letter, is_correct)
        self.letters.append(new_letter_stat)

    def add_words(self, word: str, is_correct: bool):
        new_word_stat = Stat(word, is_correct)
        self.words.append(new_word_stat)

    def remove_last_letter(self):
        self.letters.pop()

    def remove_last_word(self):
        self.words.pop()

    def get_letter_count(self):
        return len(self.letters)

    def get_correct_letter_count(self):
        return self.count_correct(self.letters)

    def get_word_count(self):
        return len(self.letters)

    def get_correct_word_count(self):
        return self.count_correct(self.words)

    @staticmethod
    def count_correct(stat_list: list[Stat]):
        if not stat_list:
            return 0
        count = 0
        for stat in stat_list:
            if stat.is_correct:
                count += 1
        return count


