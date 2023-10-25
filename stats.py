class WordStat:
    def __init__(self, word: str, is_correct: bool, correct_characters: int):
        self.word = word
        self.is_correct = is_correct
        self.correct_characters = correct_characters


class Statistics:
    def __init__(self):
        self.word_stats: list[WordStat] = []

    def add_words(self, word: str, is_correct: bool, correct_characters: int):
        new_word_stat = WordStat(word, is_correct, correct_characters)
        self.word_stats.append(new_word_stat)

    def get_char_count(self):
        if not self.word_stats:
            return 0
        char_counts = [len(stat.word) for stat in self.word_stats]
        return sum(char_counts)

    def get_word_count(self):
        return len(self.word_stats)

    def get_correct_words_count(self):
        correct_words = self.get_correct_words()
        return len(correct_words)

    def get_correct_char_count(self):
        if not self.word_stats:
            return 0
        correct_chars = [stat.correct_characters for stat in self.word_stats]
        return sum(correct_chars)

    def remove_last(self):
        self.word_stats.pop()

    def get_correct_words(self):
        if not self.word_stats:
            return []
        correct_words = [stat for stat in self.word_stats if stat.is_correct]
        return correct_words

    def get_correct_char_count(self):
        correct_words = self.get_correct_words()
        if not correct_words:
            return 0
        char_counts = [len(word_stat.word) for word_stat in correct_words]
        return sum(char_counts)
