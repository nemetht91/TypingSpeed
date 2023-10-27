import tkinter as tk
from settings import TIMER_LENGTH
from typing import Callable


class Timer:
    def __init__(self, window: tk.Tk, label_update_func: Callable, stop_func: Callable):
        self.window = window
        self.label_update = label_update_func
        self.timer_count = TIMER_LENGTH
        self.timer = None
        self.timer_running = False
        self.stopped = stop_func

    def start_timer(self, timer_length=TIMER_LENGTH):
        self.timer_count = timer_length
        self.timer_running = True
        self.count_down(self.timer_count)

    def count_down(self, count):
        if count >= 0:
            self.timer_count = count
            self.label_update(self.timer_count)
            self.timer = self.window.after(1000, self.count_down, self.timer_count - 1)
        else:
            self.window.after_cancel(self.timer)
            self.timer_running = False
            self.stopped()

    def reset_timer(self):
        self.window.after_cancel(self.timer)
        self.timer_running = False
        self.timer_count = 60


