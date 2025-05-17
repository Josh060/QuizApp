import tkinter as tk
from tkinter import ttk
from style import COLOR_THEME
 
class ReviewWindow(tk.Toplevel):
     def __init__(self, root, quiz_manager, on_restart, back_to_main_callback):
         super().__init__(root)
         self.withdraw()
         self.root = root
         self.quiz_manager = quiz_manager
         self.on_restart = on_restart
         self.back_to_main_callback = back_to_main_callback
         self.title("Quiz Review")
         self.attributes('-fullscreen', True)
         self.configure(bg=COLOR_THEME.question_bg)
         self.restart_callback = on_restart
         self.questions = self.quiz_manager.questions
         self.correct_answers = [q['correct_answer'] for q in self.questions]
         self.user_answers = [self.quiz_manager.user_answers.get(i) for i in range(len(self.questions))]
         self.final_score = self.quiz_manager.get_score()
         self.total_questions = self.quiz_manager.get_total_questions()
         self.filtered_indices = list(range(len(self.questions)))
         self.current_index = 0
         self.style = ttk.Style(self)
         self.style.configure("Review.TFrame", background=COLOR_THEME.question_bg)
         self.style.configure("Score.TLabel", font=("Helvetica", 20, "bold"), background=COLOR_THEME.question_bg, foreground=COLOR_THEME.text_inverse, padding=10, anchor="center")
         self.style.configure("Question.TLabel", font=("Helvetica", 18, "bold"), wraplength=self.winfo_screenwidth() - 200, background=COLOR_THEME.surface, foreground=COLOR_THEME.text, padding=15, justify="center")
         self.style.configure("UserAnswerCorrect.TLabel", font=("Helvetica", 14, "italic"), background=COLOR_THEME.correct, padding=10, justify="left")
         self.style.configure("UserAnswerIncorrect.TLabel", font=("Helvetica", 14, "italic"), background=COLOR_THEME.incorrect, padding=10, justify="left")
         self.style.configure("CorrectAnswer.TLabel", font=("Helvetica", 14, "bold"), background="#ddffdd", padding=10, justify="left")
         self.style.configure("Navigation.TFrame", background=COLOR_THEME.question_bg)
         self.style.configure("Bottom.TFrame", background=COLOR_THEME.question_bg)
         self.style.configure("TButton", font=("Helvetica", 14), padding=8)
         self.main_frame = ttk.Frame(self, padding=30, style="Review.TFrame")
         self.main_frame.pack(expand=True, fill="both", anchor="center")
         self.header_label = ttk.Label(self.main_frame, text="📋 Quiz Review", font=("Helvetica", 26, "bold"), background=COLOR_THEME.question_bg, foreground=COLOR_THEME.text_inverse, padding=10)
         self.header_label.pack(pady=(0, 10))
         self.score_label = ttk.Label(self.main_frame, text=f"Your Score: {self.final_score}/{self.total_questions}", style="Score.TLabel")
         self.score_label.pack(pady=(0, 20))
         self.counter_label = ttk.Label(self.main_frame, text="", font=("Helvetica", 14), background=COLOR_THEME.question_bg, foreground=COLOR_THEME.text_inverse)
         self.counter_label.pack(pady=(0, 10))
         self.filter_var = tk.BooleanVar(value=False)
         self.question_label = ttk.Label(self.main_frame, text="", style="Question.TLabel")
         self.question_label.pack(fill="x", pady=(10, 10))
         self.options_label = ttk.Label(self.main_frame, text="", font=("Helvetica", 14), background=COLOR_THEME.surface, justify="left", anchor="w")
         self.options_label.pack(fill="x", pady=(5, 5))
         self.user_answer_label = ttk.Label(self.main_frame, text="", style="UserAnswerCorrect.TLabel")
         self.user_answer_label.pack(fill="x", pady=5)
         self.correct_answer_label = ttk.Label(self.main_frame, text="", style="CorrectAnswer.TLabel")
         self.correct_answer_label.pack(fill="x", pady=5)
         self.navigation_frame = ttk.Frame(self.main_frame, style="Navigation.TFrame")
         self.navigation_frame.pack(pady=20)
         self.prev_button = ttk.Button(self.navigation_frame, text="Previous", command=self.show_previous, style="TButton")
         self.prev_button.grid(row=0, column=0, padx=10)
         self.next_button = ttk.Button(self.navigation_frame, text="Next", command=self.show_next, style="TButton")
         self.next_button.grid(row=0, column=1, padx=10)
         self.summary_button = ttk.Button(self.navigation_frame, text="Review Summary", command=self.show_summary, style="TButton")
         self.summary_button.grid(row=0, column=2, padx=10)
         self.bottom_frame = ttk.Frame(self.main_frame, style="Bottom.TFrame")
         self.bottom_frame.pack(pady=20)
         self.filter_checkbox = ttk.Checkbutton(
         self.bottom_frame,
              text="Show Only Unanswered/Incorrect",
              variable=self.filter_var,
              command=self.apply_filter,
              style="TButton"
          )
         self.filter_checkbox.pack(side="left", padx=10)
         self.back_to_main_button = ttk.Button(
              self.bottom_frame,
              text="Return to Language Selection",
              command=self.back_to_main,
              style="TButton"
          )
         self.back_to_main_button.pack(side="left", padx=10)
         self.update_review()
         self._update_navigation_buttons()
         self.bind("<Escape>", self._exit_fullscreen)
         self._fullscreen = True
         self.deiconify()
 
     def apply_filter(self):
         if self.filter_var.get():
             self.filtered_indices = [
                 i for i, ans in enumerate(self.user_answers)
                 if ans is None or ans.strip().lower() != self.correct_answers[i].strip().lower()
             ]
         else:
             self.filtered_indices = list(range(len(self.questions)))
         self.current_index = 0
         self.update_review()
 
     def update_review(self):
          if 0 <= self.current_index < len(self.filtered_indices):
               actual_index = self.filtered_indices[self.current_index]
               self.counter_label.config(text=f"Question {self.current_index + 1} of {len(self.filtered_indices)}")
               question_data = self.questions[actual_index]
               user_answer = self.user_answers[actual_index]
               correct_answer = self.correct_answers[actual_index]

        # For display purposes only
               if user_answer is None:
                    display_answer = "Not answered"
               elif user_answer == "⏱ Timeout!":
                    display_answer = "⏱ Timeout!"
               else:
                    display_answer = user_answer

               self.question_label.config(text=f"Question {actual_index + 1}: {question_data['question']}")
               options_text = ""
               for i, option in enumerate(question_data.get('options', [])):
                    prefix = f"({chr(ord('A') + i)}) "
                    option_clean = option.strip().lower()
                    user_clean = (user_answer or "").strip().lower()
                    correct_clean = correct_answer.strip().lower()
                    if option_clean == user_clean and option_clean == correct_clean:
                         mark = "✅"
                    elif option_clean == user_clean and option_clean != correct_clean:
                         mark = "❌"
                    elif option_clean == correct_clean:
                         mark = "✔"
                    else:
                         mark = "•"
                    options_text += f"{mark} {prefix}{option}  "
               self.options_label.config(text=options_text.strip())

               if user_answer is None or user_answer.strip().lower() != correct_answer.strip().lower():
                    self.user_answer_label.config(text=f"Your Answer: {display_answer}", style="UserAnswerIncorrect.TLabel")
               else:
                    self.user_answer_label.config(text=f"Your Answer: {display_answer}", style="UserAnswerCorrect.TLabel")
               self.correct_answer_label.config(text=f"Correct Answer: {correct_answer}")

     def show_next(self):
         if self.current_index < len(self.filtered_indices) - 1:
             self.current_index += 1
             self.update_review()
             self._update_navigation_buttons()
 
     def show_previous(self):
         if self.current_index > 0:
             self.current_index -= 1
             self.update_review()
             self._update_navigation_buttons()
 
     def _update_navigation_buttons(self):
         self.prev_button.config(state=tk.NORMAL if self.current_index > 0 else tk.DISABLED)
         self.next_button.config(state=tk.NORMAL if self.current_index < len(self.filtered_indices) - 1 else tk.DISABLED)
 
     def back_to_main(self):
        print("ReviewWindow: back_to_main called")  
        self.destroy() 
        self.back_to_main_callback()

     def _exit_fullscreen(self, event=None):
         self._fullscreen = False
         self.attributes("-fullscreen", False)
         
     def show_summary(self):
         summary_window = tk.Toplevel(self)
         summary_window.title("Answer Summary")
         summary_window.geometry("600x600")
         summary_window.configure(bg="white")
         canvas = tk.Canvas(summary_window, bg="white")
         scrollbar = ttk.Scrollbar(summary_window, orient="vertical", command=canvas.yview)
         scroll_frame = ttk.Frame(canvas)
         scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
         canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
         canvas.configure(yscrollcommand=scrollbar.set)
         canvas.pack(side="left", fill="both", expand=True)
         scrollbar.pack(side="right", fill="y")
         for i, question in enumerate(self.questions):
             user_answer = self.user_answers[i]
             correct_answer = self.correct_answers[i]
             status = "✅ Correct" if user_answer and user_answer.strip().lower() == correct_answer.strip().lower() else "❌ Incorrect"
             if user_answer is None:
                 status = "⚠️ Not Answered"
             frame = ttk.Frame(scroll_frame, padding=10)
             frame.pack(pady=5, fill="x")
             question_label = ttk.Label(frame, text=f"{i+1}. {question['question']}", wraplength=550, justify="left", font=("Helvetica", 12, "bold"))
             question_label.pack(fill="x")
             user_answer_label = ttk.Label(frame, text=f"Your Answer: {user_answer if user_answer else 'Not answered'}", justify="left", font=("Helvetica", 10, "italic"), foreground="#333")
             user_answer_label.pack(fill="x")
             correct_answer_label = ttk.Label(frame, text=f"Correct Answer: {correct_answer}", justify="left", font=("Helvetica", 10, "bold"), foreground="#008000") # Green
             correct_answer_label.pack(fill="x")
             status_label = ttk.Label(frame, text=f"Status: {status}", font=("Helvetica", 10), foreground="#000080") # Blue
             status_label.pack(fill="x")
             ttk.Separator(frame).pack(fill="x", pady=5)
