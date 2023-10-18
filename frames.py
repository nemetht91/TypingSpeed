import tkinter as tk
from settings import *
from notifier import UpdateNotifier

MATRIX_WIDTH = 500
MATRIX_HEIGHT = 400


class TextMatrixFrame(tk.Frame):
    def __init__(self, parent, starting_words: list[list[str]]):
        super().__init__(master=parent)
        self.grid(column=0, row=2, sticky='', padx=10, pady=10)
        self.configure(width=MATRIX_WIDTH, height=MATRIX_HEIGHT)
        self.row_frames = self.create_row_frames()
        self.word_frames: list[list[WordFrame]] = self.create_word_frames(starting_words)

    def create_row_frames(self):
        rows = []
        for i in range(ROWS_OF_WORDS):
            row = tk.Frame(self, width=MATRIX_WIDTH, height=MATRIX_HEIGHT / ROWS_OF_WORDS)
            row.grid(column=0, row=i, sticky="")
            rows.append(row)
        return rows

    def create_word_frames(self, words: list[list[str]]):
        labels = []
        for i in range(ROWS_OF_WORDS):
            label_row = []
            row_frame = self.row_frames[i]
            for j in range(WORDS_IN_ROW):
                word = words[i][j] if words[i][j] else ""
                label_row.append(self.create_word_frame(word, j, row_frame))
            labels.append(label_row)
        return labels

    def create_word_frame(self, text, column, row_frame):
        word_frame = WordFrame(row_frame, column, text)
        word_frame.grid(row=0, column=column, sticky="w")
        return word_frame

    def highlight_word(self, row, column):
        word = self.word_frames[row][column]
        word.highlight()

    def un_highlight_word(self, row, column):
        word = self.word_frames[row][column]
        word.un_highlight()

    def check_word(self, current_input, row, column):
        word = self.word_frames[row][column]
        word.compare_input(current_input)


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
            label.configure(background="white")

    def compare_input(self, current_input):
        for i, letter in enumerate(current_input):
            if self.is_out_of_range(i):
                break
            self.compare_letter(letter, i)
        if self.is_input_shorter(current_input):
            self.reset_color(current_input)

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

    def reset_color(self, current_input):
        for i in range(len(current_input), len(self.word)):
            self.set_letter_color(i, BLUE)

    def is_input_shorter(self, current_input):
        return len(current_input) < len(self.word)


class TextInputFrame(tk.Frame):
    def __init__(self, parent, update_notifier: UpdateNotifier):
        super().__init__(master=parent)
        self.grid(column=0, row=3, sticky="")
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
        self.update_notifier.word_submitted()

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



