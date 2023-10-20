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
        self.row_frames = self.init_rows(starting_words)

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

    def highlight_word(self, row_index, column_index):
        word = self.get_word(row_index, column_index)
        word.highlight()

    def un_highlight_word(self, row_index, column_index):
        word = self.get_word(row_index, column_index)
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

    def check_word(self, current_input, row, column):
        word = self.get_word(row, column)
        word.compare_input(current_input)

    def add_new_row(self, words: list[str]):
        self.hide_top_row()
        self.create_new_row(words)

    def hide_top_row(self):
        top_row_index = len(self.row_frames) - ROWS_OF_WORDS
        self.check_row_exist(top_row_index)
        top_row = self.row_frames[top_row_index]
        top_row.grid_forget()

    def create_new_row(self, words: list[str]):
        new_row = RowFrame(self, len(self.row_frames), words)
        self.row_frames.append(new_row)

    def get_number_of_rows(self):
        return len(self.row_frames) - 1


class RowFrame(tk.Frame):
    def __init__(self, parent, row_index, words: list[str]):
        super().__init__(master=parent, width=MATRIX_WIDTH, height=MATRIX_HEIGHT / ROWS_OF_WORDS)
        self.grid(column=0, row=row_index, sticky="")
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
            self.set_letter_color(i, CREAM)

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



