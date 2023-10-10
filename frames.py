import tkinter as tk
from settings import *


class TextMatrixFrame(tk.Frame):
    def __init__(self, parent, starting_words: list[list[str]]):
        super().__init__(master=parent)
        self.grid(column=0, row=2, sticky='', padx=10, pady=10)
        self.configure(width=500, height=400)
        self.labels: list[list[tk.Label]] = self.create_labels(starting_words)

    def create_labels(self, words: list[list[str]]):
        labels = []
        for i in range(ROWS_OF_WORDS):
            label_row = []
            for j in range(WORDS_IN_ROW):
                word = words[i][j] if words[i][j] else ""
                label_row.append(self.create_label(word, i, j))
            labels.append(label_row)
        return labels

    def create_label(self, text, row, column):
        return tk.Label(self, text=text, foreground=BLUE, padx=5, font=(FONT_NAME, 12, "bold")).grid(row=row, column=column)
