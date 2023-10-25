import tkinter
from timer import Timer
from frames import *
from stats import Statistics


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
        self.update_notifier = UpdateNotifier(word_submitted=self.next_word_request,
                                              field_cleared=self.previous_word_request,
                                              text_update=self.input_field_changed)
        self.statistics = Statistics()

        # layout
        self.create_title_label()
        self.stats_canvas = self.create_stats_canvas()
        self.timer_text = self.stats_canvas.create_text(100, 50, text=60, fill=BLUE, font=(FONT_NAME, 35, "bold"))
        self.text_input_frame = TextInputFrame(self, self.update_notifier)
        self.text_matrix = TextMatrixFrame(self, self.words_buffer, self.statistics)
        self.timer = Timer(self, self.stats_canvas, self.timer_text)
        self.start_button = self.create_start_button()
        self.reset_btn = self.create_reset_button()

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

    def next_word_request(self, current_input):
        self.text_matrix.move_to_next_word(current_input)
        self.print_statistics()

    def previous_word_request(self):
        self.text_matrix.move_to_previous_word()

    def input_field_changed(self, current_input):
        self.text_matrix.check_word(current_input)

    def print_statistics(self):
        print(f"Words: {self.statistics.get_correct_words_count()}/{self.statistics.get_word_count()}")
        print(f"Chars: {self.statistics.get_correct_char_count()}/{self.statistics.get_char_count()}")


