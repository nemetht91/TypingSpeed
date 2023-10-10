import tkinter as tk


class Timer:
    def __init__(self, window: tk.Tk, canvas: tk.Canvas, timer_text):
        self.window = window
        self.canvas = canvas
        self.timer_text = timer_text
        self.timer_count = 60
        self.timer = None

    def start_timer(self, timer_length=60):
        self.timer_count = timer_length
        self.count_down(self.timer_count)

    def count_down(self, count):
        if count >= 0:
            self.timer_count = count
            self.canvas.itemconfig(self.timer_text, text=self.timer_count)
            self.timer = self.window.after(1000, self.count_down, self.timer_count - 1)
        else:
            self.window.after_cancel(self.timer)

    def reset_timer(self):
        self.window.after_cancel(self.timer)
        self.timer_count = 60


