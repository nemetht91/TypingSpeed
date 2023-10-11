import tkinter as tk
from settings import *

MATRIX_WIDTH = 500
MATRIX_HEIGHT = 400


class TextMatrixFrame(tk.Frame):
    def __init__(self, parent, starting_words: list[list[str]]):
        super().__init__(master=parent)
        self.grid(column=0, row=2, sticky='', padx=10, pady=10)
        self.configure(width=MATRIX_WIDTH, height=MATRIX_HEIGHT)
        self.row_frames = self.create_row_frames()
        self.labels: list[list[LabelFrame]] = self.create_labels(starting_words)

    def create_row_frames(self):
        rows = []
        for i in range(ROWS_OF_WORDS):
            row = tk.Frame(self, width=MATRIX_WIDTH, height=MATRIX_HEIGHT / ROWS_OF_WORDS)
            row.grid(column=0, row=i, sticky="")
            rows.append(row)
        return rows

    def create_labels(self, words: list[list[str]]):
        labels = []
        for i in range(ROWS_OF_WORDS):
            label_row = []
            row_frame = self.row_frames[i]
            for j in range(WORDS_IN_ROW):
                word = words[i][j] if words[i][j] else ""
                label_row.append(self.create_label(word, j, row_frame))
            labels.append(label_row)
        return labels

    def create_label(self, text, column, row_frame):
        label = LabelFrame(row_frame, column, text)
        label.grid(row=0, column=column, sticky="w")
        return label

    def highlight_label(self, row, column):
        label = self.labels[row][column]
        label.highlight()

    def un_highlight_label(self, row, column):
        label = self.labels[row][column]
        label.un_highlight()


class LabelFrame(tk.Frame):
    def __init__(self, parent, column, word):
        super().__init__(master=parent)
        self.grid(row=0, column=column, sticky="w", padx=5)
        self.word = word
        self.letter_labels = self.create_labels()

    def create_labels(self):
        labels = []
        for i, letter in enumerate(self.word):
            label = tk.Label(self, text=letter, foreground=color, padx=0, font=(FONT_NAME, 12, "bold"))
            label.grid(row=0, column=i, sticky="w")
            labels.append(label)
        return labels

    def highlight(self):
        for label in self.letter_labels:
            label.configure(background=BLUE, foreground=CREAM)

    def un_highlight(self):
        for label in self.letter_labels:
            label.configure(background="white", foreground=BLUE)


class TextInputFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.grid(column=0, row=3, sticky="")
        self.current_input = tk.StringVar(value="")
        self.text_box = tk.Entry(self, textvariable=self.current_input, foreground=BLUE)
        self.text_box.grid(column=0, row=0, sticky="")
