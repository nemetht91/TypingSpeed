import tkinter as tk
from settings import *
from timer import Timer
from words import Words
from frames import *

word_generator = Words()
starting_words = []
for i in range(ROWS_OF_WORDS):
    word_row = []
    for j in range(WORDS_IN_ROW):
        word_row.append(word_generator.get_random_word())
    starting_words.append(word_row)

window = tk.Tk()
window.title(" Typing Speed Check")
window.configure(padx=50, pady=50)
window.configure(background=CREAM)
window.geometry("650x800")

title_label = tk.Label(window, text=TITLE, foreground=BLUE,
                       background=CREAM, padx=10, font=(FONT_NAME, 35, "bold"))
title_label.grid(column=0, row=0, sticky="")

canvas = tk.Canvas(window, width=200, height=100)
canvas.configure(background=BEIGE, highlightthickness=0)
timer_text = canvas.create_text(100, 50, text=60, fill=BLUE, font=(FONT_NAME, 35, "bold"))
canvas.grid(column=0, row=1, sticky="")

text_input_frame = TextInputFrame(window)

text_matrix = TextMatrixFrame(window, starting_words)
text_matrix.highlight_label(1, 1)
text_matrix.un_highlight_label(1, 1)


timer = Timer(window, canvas, timer_text)

start_button = tk.Button(text="Start", font=(FONT_NAME, 8, "bold"), highlightthickness=0, command=timer.start_timer)
start_button.grid(column=0, row=4)

reset_btn = tk.Button(text="Reset", font=(FONT_NAME, 8, "bold"), highlightthickness=0, command=timer.reset_timer)
reset_btn.grid(column=0, row=5)

window.mainloop()
