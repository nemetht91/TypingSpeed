import tkinter
from timer import Timer
from frames import *
from stats import Statistics
from settings import *


class App(tkinter.Tk):
    def __init__(self):
        # setup
        super().__init__()
        self.title("Typing Speed Check")
        self.configure(padx=50, pady=50)
        self.configure(background=BLUE)
        self.word_generator = WordGenerator()
        self.words_buffer = self.get_starting_words()
        self.update_notifier = UpdateNotifier(word_submitted=self.next_word_request,
                                              field_cleared=self.previous_word_request,
                                              text_update=self.input_field_changed)
        self.statistics = Statistics()

        # layout
        self.create_title_label()
        self.stats_frame = StatisticsFrame(self, self.statistics)
        self.text_input_frame = TextInputFrame(self, self.update_notifier)
        self.text_matrix = TextMatrixFrame(self, self.words_buffer, self.statistics)
        self.button_frame = ButtonFrame(self, self.start, self.reset)
        self.timer = Timer(self, label_update_func=self.stats_frame.update_timer_label, stop_func=self.stop)
        self.ready = True
        self.text_input_frame.text_box.focus()
        self.mainloop()

    def create_title_label(self):
        title_label = tk.Label(self, text=TITLE, foreground=CREAM,
                               background=BLUE, padx=10, font=(FONT_NAME, TITLE_SIZE, "bold"))
        title_label.grid(column=0, row=0, sticky="")

    def get_starting_words(self):
        return self.word_generator.get_word_matrix(ROWS_OF_WORDS, WORDS_IN_ROW)

    def next_word_request(self, current_input):
        if not self.ready:
            return
        self.text_matrix.move_to_next_word(current_input)
        self.stats_frame.update_labels()

    def previous_word_request(self):
        if not self.ready:
            return
        self.text_matrix.move_to_previous_word()

    def input_field_changed(self, current_input):
        if not self.ready:
            return
        if not self.timer.timer_running:
            self.start()
        self.text_matrix.check_word(current_input)

    def start(self):
        self.timer.start_timer()

    def stop(self):
        self.ready = False
        self.button_frame.stop()
        self.button_frame.reset_button.focus()

    def reset(self):
        self.statistics.clear()
        self.text_matrix.grid_forget()
        self.text_matrix = TextMatrixFrame(self, self.get_starting_words(), self.statistics)
        self.stats_frame.update_labels()
        self.stats_frame.update_timer_label(TIMER_LENGTH)
        self.text_input_frame.clear()
        self.text_input_frame.text_box.focus()
        self.ready = True

    def print_statistics(self):
        print(f"Words: {self.statistics.get_correct_words_count()}/{self.statistics.get_word_count()}")
        print(f"Chars: {self.statistics.get_correct_char_count()}/{self.statistics.get_char_count()}")


