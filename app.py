import tkinter

from notifier import UpdateNotifier
from timer import Timer
from wordgenerator import WordGenerator
from frames import *


class App(tkinter.Tk):
    def __init__(self):
        # setup
        super().__init__()
        self.title(" Typing Speed Check")
        self.configure(padx=50, pady=50)
        self.configure(background=CREAM)
        self.geometry("650x800")

        self.word_generator = WordGenerator()
        self.words_buffer = self.get_starting_words()
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
        self.text_matrix = TextMatrixFrame(self, self.words_buffer)
        self.timer = Timer(self, self.stats_canvas, self.timer_text)
        self.start_button = self.create_start_button()
        self.reset_btn = self.create_reset_button()

        self.add_highlight()
        self.text_input_frame.text_box.focus()
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
        return self.word_generator.get_word_matrix(ROWS_OF_WORDS, WORDS_IN_ROW)

    def increase_word_counters(self):
        self.remove_highlight()
        if self.column_counter == WORDS_IN_ROW-1:
            self.row_counter += 1
            self.column_counter = 0
            self.new_row_required()
        else:
            self.column_counter += 1
        self.add_highlight()

    def new_row_required(self):
        if self.row_counter == self.text_matrix.get_number_of_rows():
            words = self.word_generator.get_word_list(WORDS_IN_ROW)
            self.text_matrix.add_new_row(words)
            #self.row_counter -= 1

    def decrease_word_counters(self):
        self.remove_highlight()
        if self.column_counter == 0 and self.row_counter != 0:
            self.row_counter -= 1
            self.column_counter = WORDS_IN_ROW - 1
        elif self.column_counter != 0:
            self.column_counter -= 1
        self.add_highlight()

    def remove_highlight(self):
        self.text_matrix.un_highlight_word(self.row_counter, self.column_counter)

    def add_highlight(self):
        self.text_matrix.highlight_word(self.row_counter, self.column_counter)

    def input_field_changed(self, current_input):
        self.text_matrix.check_word(current_input, self.row_counter, self.column_counter)


