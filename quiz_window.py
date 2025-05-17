import tkinter as tk
from tkinter import ttk, messagebox
from style import FONTS, COLOR_THEME, DIMENSIONS, COMPONENT_STYLES, configure_styles
from timer import TimerManager
from quiz_manager import QuizManager
from database import Database
import logging
import random

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
class QuizWindow(tk.Toplevel):
    QUESTION_HEADER_FORMAT = "Question {} of {}"
    def __init__(self, root, quiz_manager: QuizManager, on_quiz_finish):
        super().__init__(root)
        self.title("IT Quiz")
        self.geometry("800x600")
        self.configure(bg=COLOR_THEME.question_bg)
        self.current_question_index = 0
        self.user_answers = {}
        self.timer_manager = None
        self.on_quiz_finish = on_quiz_finish
        self.quiz_manager = quiz_manager
        self.quiz_ended = False
        self.attributes('-fullscreen', True)
        self._create_widgets()
        self._display_question() 
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _create_widgets(self):
        self.header_label = ttk.Label(self, text="", style='Header.TLabel', anchor='center')
        self.header_label.pack(pady=DIMENSIONS["padding_medium"], fill='x')
        self.question_frame = ttk.Frame(self, style='Card.TFrame', padding=DIMENSIONS["padding_large"])
        self.question_frame.pack(pady=DIMENSIONS["padding_medium"], padx=DIMENSIONS["padding_medium"], fill='both', expand=True)
        self.question_frame.grid_columnconfigure(0, weight=1)
        self.question_text = tk.Label(
            self.question_frame,
            text="",
            font=("Helvetica", 24, "bold"),
            bg=COLOR_THEME.surface,
            fg=COLOR_THEME.text,
            justify='left',
            wraplength=600
        )
        self.question_text.grid(row=0, column=0, sticky='ew', pady=(0, DIMENSIONS["padding_medium"]))
        self.answer_frame = ttk.Frame(self.question_frame, padding=DIMENSIONS["padding_medium"])
        self.answer_frame.grid(row=1, column=0, sticky='ew')
        self.selected_answer = tk.StringVar(value="")
        self.answer_radiobuttons = []
        for i in range(4):
            answer_radiobutton = tk.Radiobutton(
                self.answer_frame,
                text=f"Option {chr(65 + i)}",
                variable=self.selected_answer, 
                value="",  
                font=("Helvetica", 16),
                bg=COLOR_THEME.surface,
                fg=COLOR_THEME.text,
                anchor="w",
                wraplength=550,
                command=self._record_answer
            )
            answer_radiobutton.grid(row=i, column=0, sticky='w', pady=(0, DIMENSIONS["padding_small"]))
            self.answer_radiobuttons.append(answer_radiobutton)
        self.navigation_frame = ttk.Frame(self, padding=DIMENSIONS["padding_medium"])
        self.navigation_frame.pack(pady=DIMENSIONS["padding_medium"], fill='x')
        self.exit_button = ttk.Button(self.navigation_frame, text="Exit Quiz", command=self._exit_quiz)
        self.exit_button.pack(side='left', padx=DIMENSIONS["padding_small"])
        self.prev_button = ttk.Button(self.navigation_frame, text="Previous", command=self._prev_question, state='disabled')
        self.prev_button.pack(side='left', padx=DIMENSIONS["padding_small"])
        self.submit_button = ttk.Button(self.navigation_frame, text="Submit Quiz", command=self._submit_quiz, style='Start.TButton')
        self.submit_button.pack(side='right', padx=DIMENSIONS["padding_small"])
        self.submit_button.config(state='disabled')
        self.next_button = ttk.Button(self.navigation_frame, text="Next", command=self._next_question)
        self.next_button.pack(side='right', padx=DIMENSIONS["padding_small"])
        self.timer_label = ttk.Label(self, text="", style='Timer.TLabel')
        self.timer_label.pack(pady=DIMENSIONS["padding_small"])
        self.unanswered_label = ttk.Label(self, text="", style='Unanswered.TLabel')
        self.unanswered_label.pack(pady=DIMENSIONS["padding_small"])
        self.progress = ttk.Progressbar(self, orient='horizontal', mode='determinate', length=400)
        self.progress.pack(pady=(0, DIMENSIONS["padding_small"]))

    def _display_question(self):
        question_data = self.quiz_manager.get_current_question_data()
        current_index = self.quiz_manager.get_current_question_index()
        if question_data:
            if current_index in self.user_answers and self.user_answers[current_index] is None:
                self._highlight_timeout_question()
            self.header_label.config(text=self.QUESTION_HEADER_FORMAT.format(
                current_index + 1,
                self.quiz_manager.get_total_questions()
            ))
            self.question_text.config(text=question_data['question'])
            options = question_data.get('options', [])
            for i in range(len(self.answer_radiobuttons)):
                self.answer_radiobuttons[i].config(
                    state='normal',
                    bg='SystemButtonFace'  
                )
            if len(options) == len(self.answer_radiobuttons):
                for i, option_text in enumerate(options):
                    self.answer_radiobuttons[i].config(text=option_text, value=option_text, state='normal')
                if current_index in self.user_answers:
                    self.selected_answer.set(self.user_answers[current_index])
                else:
                    self.selected_answer.set("")
            self.prev_button.config(state='normal' if self.quiz_manager.get_current_question_index() > 0 else 'disabled')
            self.next_button.config(state='normal' if self.quiz_manager.has_next_question() else 'disabled')
            self.progress['maximum'] = self.quiz_manager.get_total_questions()
            self.progress['value'] = current_index + 1
            self._update_unanswered_label()
            self._start_timer()  
        else:
            self._submit_quiz()
    
    def _on_closing(self):
        if self.quiz_ended or messagebox.askyesno("Exit Quiz", "Are you sure you want to exit the quiz without submitting?"):
            self.stop_timer()
            self.destroy()

    def _record_answer(self):
        current_index = self.quiz_manager.get_current_question_index()
        selected_option = self.selected_answer.get()
        if selected_option == "" and current_index not in self.user_answers:
            self.user_answers[current_index] = None
        self.user_answers[current_index] = selected_option
        logging.debug(f"User answered question {current_index + 1}: {selected_option}")
        for rb in self.answer_radiobuttons:
            rb.config(bg=COLOR_THEME.surface) 
        for rb in self.answer_radiobuttons:
            if rb.cget("value") == selected_option:
                rb.config(bg="lightblue")
        all_answered = len(self.user_answers) == self.quiz_manager.get_total_questions()
        self.submit_button.config(state='normal' if all_answered else 'disabled')
        self.next_button.config(state='normal' if self.quiz_manager.has_next_question() else 'disabled')
        self._update_unanswered_label()

    def _next_question(self):
        self.stop_timer()
        if self.quiz_manager.has_next_question():
            self.quiz_manager.advance_to_next_question()
            self._display_question()  
        else:
            self._submit_quiz()

    def _prev_question(self):
        self.stop_timer()
        if self.quiz_manager.get_current_question_index() > 0:
            self.quiz_manager.decrement_question_index()
            self._display_question()

    def _exit_quiz(self):
        if messagebox.askyesno("Exit Quiz", "Are you sure you want to exit the quiz? Your progress will be lost."):
            self.quiz_ended = True
            self.stop_timer()
            results = self.quiz_manager.get_current_results()
            self.on_quiz_finish(results, exited=True) 
            self.destroy()

    def _start_timer(self):
        if self.timer_manager:
            self.timer_manager.stop()
        current_index = self.quiz_manager.get_current_question_index()
        self.quiz_manager.initialize_timer_for_question(current_index)
        remaining_time = self.quiz_manager.get_remaining_time(current_index)
        self.timer_manager = TimerManager(
            self,
            duration=remaining_time,
            on_tick=self._on_tick,
            on_timeout=self._handle_timeout
        )
        self.timer_manager.start()

    def _update_timer_label(self, remaining_time):
        color = 'red' if remaining_time <= 5 else COLOR_THEME.text
        font_size = 28 if remaining_time <= 5 else 20 
        self.timer_label.config(
            text=f"⏱ Time left: {remaining_time} sec",
            foreground=color,
            font=("Helvetica", font_size, "bold")
        )

    def _on_tick(self, remaining_time):
        self._update_timer_label(remaining_time)
        current_index = self.quiz_manager.get_current_question_index()
        self.quiz_manager.update_time_left(current_index, remaining_time)

    def _handle_timeout(self):
        logging.info(f"Timeout for question {self.quiz_manager.get_current_question_index() + 1}")
        self._disable_inputs()
        current_index = self.quiz_manager.get_current_question_index()
        if current_index not in self.user_answers:
            self.user_answers[current_index] = None
            self._update_unanswered_label()
        self.quiz_manager.update_time_left(current_index, 0)
        if self.quiz_manager.has_next_question():
            self._next_question()
        else:
            self._submit_quiz()

    def _disable_inputs(self):
        for radio in self.answer_radiobuttons:
            radio.config(state='disabled')
        self.next_button.config(state='disabled')
        self.prev_button.config(state='disabled')

    def _enable_inputs(self):
        for radio in self.answer_radiobuttons:
            radio.config(state='normal')
        self.next_button.config(state='normal' if self.quiz_manager.has_next_question() else 'disabled')
        self.prev_button.config(state='normal' if self.quiz_manager.get_current_question_index() > 0 else 'disabled')

    def stop_timer(self):
        if self.timer_manager:
            self.timer_manager.stop()

    def _submit_quiz(self):
        if self.quiz_ended or not self.winfo_exists():
            return
        self.quiz_ended = True
        self.stop_timer()
        final_results = self.quiz_manager.finalize_quiz(self.user_answers)
        self.on_quiz_finish(final_results)
        self.destroy()

    def _update_unanswered_label(self):
        total = self.quiz_manager.get_total_questions()
        answered = len(self.user_answers)
        unanswered = total - answered
        self.unanswered_label.config(text=f"Unanswered: {unanswered}")
