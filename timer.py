# timer.py
import tkinter as tk
import logging

class TimerManager:
    def __init__(self, root, duration=15, on_tick=None, on_timeout=None):
        self.root = root
        self.duration = duration
        self.remaining = duration
        self.on_tick = on_tick      
        self.on_timeout = on_timeout  
        self._running = False
        self._timer_id = None

    def start(self):
        self.stop()  
        self.remaining = self.duration
        self._running = True
        self._tick()

    def pause(self):
        if self._running:
            self._running = False
            if self._timer_id:
                self.root.after_cancel(self._timer_id)
                self._timer_id = None

    def resume(self):
        if not self._running and self.remaining > 0:
            self._running = True
            self._tick()

    def stop(self):
        self._running = False
        if self._timer_id:
            self.root.after_cancel(self._timer_id)
            self._timer_id = None

    def _tick(self):
        if self._running:
            if self.on_tick:
                self.on_tick(self.remaining)

            if self.remaining > 0:
                self.remaining -= 1
                self._timer_id = self.root.after(1000, self._tick)
            else:
                self._running = False
                if self.on_timeout:
                    self.on_timeout()
                self.stop()

    @property
    def is_running(self):
        return self._running

    @property
    def time_left(self):
        return self.remaining
