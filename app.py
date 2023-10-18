import tkinter

from notifier import UpdateNotifier
from timer import Timer
from words import Words
from frames import *


class App(tkinter.Tk):
    def __init__(self):
        # setup
        super().__init__()
        self.title(" Typing Speed Check")
        self.configure(padx=50, pady=50)
        self.configure(background=CREAM)
        self.geometry("650x800")

        self.word_generator = Words()
        self.words_matrix = self.get_starting_words()
        self.column_counter = 0
        self.row_counter = 0
        self.update_notifier = UpdateNotifier(word_submitted=self.increase_word_counters,
                                              field_cleared=self.decrease_word_counters,
                                              text_update=self.input_field_changed)

        # layout
        self.create_title_label()
        self.stats_canvas = self.create_stats_canvas()
        self.timer_text = self.stats_canvas.create_text(100, 50, text=60, fill=BLUE, font=(FONT_NAME, 35, "bold"))
        self.text_input_frame = TextInputFrame(self, self.update_notifier)
        self.text_matrix = TextMatrixFrame(self, self.words_matrix)
        self.timer = Timer(self, self.stats_canvas, self.timer_text)
        self.start_button = self.create_start_button()
        self.reset_btn = self.create_reset_button()

        self.mainloop()

    def create_title_label(self):
        title_label = tk.Label(self, text=TITLE, foreground=BLUE,
                               background=CREAM, padx=10, font=(FONT_NAME, 35, "bold"))
        title_label.grid(column=0, row=0, sticky="")

    def create_stats_canvas(self):
        canvas = tk.Canvas(self, width=200, height=100)
        canvas.configure(background=BEIGE, highlightthickness=0)
        canvas.grid(column=0, row=1, sticky="")
        return canvas

    def create_start_button(self):
        start_button = tk.Button(text="Start", font=(FONT_NAME, 8, "bold"), highlightthickness=0,
                                 command=self.timer.start_timer)
        start_button.grid(column=0, row=4)
        return start_button

    def create_reset_button(self):
        reset_btn = tk.Button(text="Reset", font=(FONT_NAME, 8, "bold"), highlightthickness=0,
                              command=self.timer.reset_timer)
        reset_btn.grid(column=0, row=5)
        return reset_btn

    def get_starting_words(self):
        starting_words = []
        for i in range(ROWS_OF_WORDS):
            word_row = []
            for j in range(WORDS_IN_ROW):
                word_row.append(self.word_generator.get_random_word())
            starting_words.append(word_row)
        return starting_words

    def increase_word_counters(self):
        current_row = self.words_matrix[self.row_counter]
        if self.column_counter == len(current_row)-1:
            self.row_counter += 1
            self.column_counter = 0
        else:
            self.column_counter += 1

    def decrease_word_counters(self):
        if self.column_counter == 0 and self.row_counter != 0:
            self.row_counter -= 1
            row = self.words_matrix[self.row_counter]
            self.column_counter = len(row) - 1
        elif self.column_counter != 0:
            self.column_counter -= 1

    def input_field_changed(self, current_input):
        self.text_matrix.check_word(current_input, self.row_counter, self.column_counter)


