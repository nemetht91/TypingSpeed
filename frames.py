import tkinter as tk
from settings import *
from notifier import UpdateNotifier
from wordgenerator import WordGenerator
from stats import Statistics
from timer import Timer

MATRIX_WIDTH = 500
MATRIX_HEIGHT = 400


class StatisticsFrame(tk.Frame):
    def __init__(self, parent, statistics: Statistics):
        super().__init__(master=parent)
        self.grid(column=0, row=1, sticky='', padx=10, pady=10)
        self.statistics = statistics
        self.create_leading_labels()
        self.cpm_label = self.create_cpm_label()
        self.wpm_label = self.create_wpm_label()
        self.timer_label = self.create_timer_label()

    def create_leading_labels(self):
        tk.Label(self, text="Corrected CPM:", padx=10).grid(column=0, row=0, sticky="w")
        tk.Label(self, text="WPM:", padx=10).grid(column=2, row=0, sticky="w")
        tk.Label(self, text="Time Left:", padx=10).grid(column=4, row=0, sticky="w")

    def create_cpm_label(self):
        cpm_label = tk.Label(self, text=0)
        cpm_label.grid(column=1, row=0, sticky="w")
        return cpm_label

    def create_wpm_label(self):
        wpm_label = tk.Label(self, text=0)
        wpm_label.grid(column=3, row=0, sticky="w")
        return wpm_label

    def create_timer_label(self):
        timer_label = tk.Label(self, text=TIMER_LENGTH)
        timer_label.grid(column=5, row=0, sticky="w")
        return timer_label

    def update_labels(self):
        cpm = self.statistics.get_correct_char_count()
        self.cpm_label.configure(text=cpm)
        wpm = self.statistics.get_correct_words_count()
        self.wpm_label.configure(text=wpm)

    def update_timer_label(self, timer_count):
        self.timer_label.configure(text=timer_count)


class TextMatrixFrame(tk.Frame):
    def __init__(self, parent, starting_words: list[list[str]], statistics: Statistics):
        super().__init__(master=parent)
        self.grid(column=0, row=2, sticky='', padx=10, pady=10)
        self.configure(width=MATRIX_WIDTH, height=MATRIX_HEIGHT)
        self.word_generator = WordGenerator()
        self.statistics = statistics
        self.row_frames = self.init_rows(starting_words)
        self.column_counter = 0
        self.row_counter = 0
        self.highlight_word()

    def init_rows(self, starting_words: list[list[str]]):
        self.check_starting_words(starting_words)
        rows = []
        for i in range(ROWS_OF_WORDS):
            words = starting_words[i]
            row = RowFrame(self, i, words)
            rows.append(row)
        return rows

    def check_starting_words(self, starting_words: list[list[str]]):
        if len(starting_words) != ROWS_OF_WORDS:
            raise ValueError(f"Unexpected number of rows in starting words! Expected: {ROWS_OF_WORDS}; "
                             f"received: {len(starting_words)}")

    def highlight_word(self):
        word = self.get_word(self.row_counter, self.column_counter)
        word.highlight()

    def un_highlight_word(self):
        word = self.get_word(self.row_counter, self.column_counter)
        word.un_highlight()

    def get_word(self, row_index, column_index):
        row = self.get_row(row_index)
        return row.get_word(column_index)

    def get_row(self, row_index):
        self.check_row_exist(row_index)
        return self.row_frames[row_index]

    def check_row_exist(self, row_index):
        if row_index < 0 or row_index >= len(self.row_frames):
            raise IndexError(f"Row doesn't exist at index: {row_index}")

    def check_word(self, current_input):
        word = self.get_word(self.row_counter, self.column_counter)
        word.compare_input(current_input)

    def hide_row(self, index):
        row = self.get_row(index)
        row.hide()

    def show_row(self, index):
        row = self.get_row(index)
        row.show()

    def create_new_row(self):
        words = self.word_generator.get_word_list(WORDS_IN_ROW)
        new_row = RowFrame(self, len(self.row_frames), words)
        self.row_frames.append(new_row)

    def get_number_of_rows(self):
        return len(self.row_frames) - 1

    def move_to_next_word(self, current_input):
        self.final_check(current_input)
        self.un_highlight_word()
        self.increment_counters()
        self.highlight_word()

    def final_check(self, current_input):
        self.add_statistics(current_input)
        word = self.get_word(self.row_counter, self.column_counter)
        word.check_remainder(current_input, RED)

    def add_statistics(self, current_input: str):
        word = self.get_word(self.row_counter, self.column_counter)
        if word.word == current_input:
            self.statistics.add_words(word.word, True, len(word.word))
            return
        self.statistics.add_words(word.word, False, word.get_correct_letter_count())

    def increment_counters(self):
        if self.is_last_in_row():
            self.hide_current_rows()
            self.row_counter += 1
            self.column_counter = 0
            self.check_to_add_new_row()
            self.show_current_rows()
        else:
            self.column_counter += 1

    def is_last_in_row(self):
        return self.column_counter == WORDS_IN_ROW-1

    def move_to_previous_word(self):
        self.statistics.remove_last()
        self.un_highlight_word()
        self.decrement_counters()
        self.highlight_word()

    def decrement_counters(self):
        if self.column_counter == 0 and self.row_counter != 0:
            self.hide_current_rows()
            self.row_counter -= 1
            self.column_counter = WORDS_IN_ROW - 1
            self.show_current_rows()
        elif self.column_counter != 0:
            self.column_counter -= 1

    def check_to_add_new_row(self):
        if self.is_last_row():
            self.create_new_row()

    def hide_current_rows(self):
        start, end = self.get_current_row_range()
        for i in range(start, end):
            self.hide_row(i)

    def get_current_row_range(self):
        if self.row_counter < (ROWS_OF_WORDS - 1):
            start = 0
            end = ROWS_OF_WORDS
        else:
            start = self.row_counter - 1
            end = self.row_counter + 2
        return start, end

    def show_current_rows(self):
        start, end = self.get_current_row_range()
        for i in range(start, end):
            self.show_row(i)

    def is_last_row(self):
        return self.row_counter == self.get_number_of_rows()


class RowFrame(tk.Frame):
    def __init__(self, parent, row_index, words: list[str]):
        super().__init__(master=parent, width=MATRIX_WIDTH, height=MATRIX_HEIGHT / ROWS_OF_WORDS)
        self.row_index = row_index
        self.show()
        self.word_frames = self.fill(words)

    def fill(self, words: list[str]):
        if not words:
            return
        word_frames = []
        for i, word in enumerate(words):
            word_frames.append(self.create_word_frame(word, i))
        return word_frames

    def create_word_frame(self, text, column):
        word_frame = WordFrame(self, column, text)
        word_frame.grid(row=0, column=column, sticky="w")
        return word_frame

    def shift(self, new_index):
        self.grid(column=0, row=new_index, sticky="")

    def get_word(self, index):
        self.check_word_exist(index)
        return self.word_frames[index]

    def check_word_exist(self, index):
        if index < 0 or index >= len(self.word_frames):
            raise IndexError(f"Word doesn't exist at index: {index}")

    def show(self):
        self.grid(column=0, row=self.row_index, sticky="")

    def hide(self):
        self.grid_remove()


class WordFrame(tk.Frame):
    def __init__(self, parent, column, word):
        super().__init__(master=parent)
        self.grid(row=0, column=column, sticky="w", padx=5)
        self.word = word
        self.letter_labels = self.create_labels()

    def create_labels(self):
        labels = []
        for i, letter in enumerate(self.word):
            label = tk.Label(self, text=letter, foreground=BLUE, padx=0, font=(FONT_NAME, 12, "bold"))
            label.grid(row=0, column=i, sticky="w")
            labels.append(label)
        return labels

    def highlight(self):
        for label in self.letter_labels:
            label.configure(background=BLUE, foreground=CREAM)

    def un_highlight(self):
        for label in self.letter_labels:
            color = label.cget("foreground")
            if color == RED or color == GREEN:
                label.configure(background="white")
            else:
                label.configure(background="white", foreground=BLUE)

    def compare_input(self, current_input):
        for i, letter in enumerate(current_input):
            if self.is_out_of_range(i):
                self.set_word_color(RED)
                break
            self.compare_letter(letter, i)
        self.check_remainder(current_input, CREAM)

    def compare_letter(self, letter, index):
        if self.is_correct(letter, index):
            self.set_letter_color(index, GREEN)
        else:
            self.set_letter_color(index, RED)

    def is_out_of_range(self, index):
        return index >= len(self.word)

    def is_correct(self, letter, index):
        return letter == self.word[index]

    def set_letter_color(self, index, color):
        letter_label = self.letter_labels[index]
        letter_label.configure(foreground=color)

    def set_word_color(self, color):
        for letter in self.letter_labels:
            letter.configure(foreground=color)

    def check_remainder(self, current_input, remainder_color):
        if self.is_input_shorter(current_input):
            self.set_color_for_remainder(current_input, remainder_color)

    def set_color_for_remainder(self, current_input, color):
        for i in range(len(current_input), len(self.word)):
            self.set_letter_color(i, color)

    def is_input_shorter(self, current_input):
        return len(current_input) < len(self.word)

    def is_input_longer(self, current_input):
        return len(current_input) > len(self.word)

    def get_correct_letter_count(self):
        correct_letters = [letter for letter in self.letter_labels if letter.cget("foreground") == GREEN]
        return len(correct_letters)


class TextInputFrame(tk.Frame):
    def __init__(self, parent, update_notifier: UpdateNotifier):
        super().__init__(master=parent)
        #self.grid(column=0, row=3, sticky="")
        self.current_input = tk.StringVar(value="")
        self.text_box = tk.Entry(self, textvariable=self.current_input, foreground=BLUE)
        self.text_box.grid(column=0, row=0, sticky="")
        self.typed_in_words = []
        self.last_value = ""
        self.is_reset = False
        # self.text_box.bind("<space>", self.word_finished)
        self.text_box.bind("<BackSpace>", self.check_word_cleared)
        self.text_box.bind("<Key>", self.set_last_value)
        self.update_notifier: UpdateNotifier = update_notifier
        self.add_trace()

    def add_trace(self):
        self.current_input.trace_add(mode='write', callback=self.check_input)

    def check_input(self, var, index, mode):
        current_input = self.current_input.get()
        if current_input == " ":
            self.clear_space()
            return
        if self.is_input_submitted():
            self.word_finished()
            return
        if self.is_reset:
            self.is_reset = False
            return
        self.send_notifier()

    def set_last_value(self, event):
        self.last_value = self.current_input.get()

    def send_notifier(self):
        self.update_notifier.text_updated(self.current_input.get())

    def is_input_submitted(self):
        return " " in self.current_input.get()

    def word_finished(self):
        self.last_value = self.current_input.get().strip()
        self.typed_in_words.append(self.last_value)
        self.current_input.set("")
        self.update_notifier.word_submitted(self.last_value)

    def check_word_cleared(self, event):
        current_value = self.text_box.get()
        if current_value == "" and self.last_value != "":
            self.last_value = ""
        if current_value == "" and self.last_value == "":
            self.get_last_word()

    def clear_space(self):
        self.current_input.set("")
        self.text_box.update()

    def get_last_word(self):
        if not self.typed_in_words:
            return
        self.is_reset = True
        self.current_input.set(self.typed_in_words[-1] + "*")
        self.text_box.icursor(len(self.typed_in_words[-1]) + 1)
        self.typed_in_words.pop()
        self.text_box.update()
        self.update_notifier.field_cleared()

    def show(self):
        self.current_input.set("")
        self.grid(column=0, row=3, sticky="")

    def hide(self):
        self.grid_forget()



