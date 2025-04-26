# quiz_window.py — don't remove this line

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import random
from style import COLOR_THEME

# Define button size constants
BUTTON_WIDTH = 20
BUTTON_HEIGHT = 2

class QuizWindow:
    def __init__(self, root, quiz_manager, username, restart_callback):
        self.quiz_manager = quiz_manager
        self.username = username
        self.restart_callback = restart_callback
        self.current_question_index = 0

        # Window Setup
        self.top = tk.Toplevel(root)
        self.top.attributes('-fullscreen', True)
        self.top.configure(bg=COLOR_THEME["question_bg"])
        self.top.title("Quiz Time!")

        # Timer Setup
        self.time_left = 15
        self.timer_id = None

        # Widgets
        self.timer_label = tk.Label(self.top, text="", font=("Helvetica", 14),
                                    bg=COLOR_THEME["question_bg"], fg="black")
        self.timer_label.pack()

        self.progress_label = tk.Label(self.top, text="", font=("Helvetica", 12),
                                       bg=COLOR_THEME["question_bg"], fg="black")
        self.progress_label.pack()

        self.question_label = tk.Label(self.top, text="", wraplength=900,
                                       font=("Helvetica", 16, "bold"), bg=COLOR_THEME["question_bg"])
        self.question_label.pack(pady=30, fill="x", expand=True)

        self.options = [self.create_option_button(i) for i in range(4)]

        # Navigation Buttons
        self.nav_frame = tk.Frame(self.top, bg=COLOR_THEME["question_bg"])
        self.nav_frame.pack(pady=10)

        self.prev_btn = tk.Button(self.nav_frame, text="Previous", command=self.show_previous_question,
                                  font=("Helvetica", 12), bg=COLOR_THEME["button_bg"], fg="white",
                                  activebackground=COLOR_THEME["button_active"], relief="flat",
                                  width=BUTTON_WIDTH // 2, height=BUTTON_HEIGHT // 2, cursor="hand2")
        self.prev_btn.pack(side=tk.LEFT, padx=10)
        self.prev_btn.config(state=tk.DISABLED)

        self.next_btn = tk.Button(self.nav_frame, text="Next", command=self.show_next_question,
                                  font=("Helvetica", 12), bg=COLOR_THEME["button_bg"], fg="white",
                                  activebackground=COLOR_THEME["button_active"], relief="flat",
                                  width=BUTTON_WIDTH // 2, height=BUTTON_HEIGHT // 2, cursor="hand2")
        self.next_btn.pack(side=tk.LEFT, padx=10)

        self.exit_btn = tk.Button(self.top, text="❌ Exit Quiz", command=self.confirm_exit,
                                  font=("Helvetica", 12), bg=COLOR_THEME["exit_bg"], fg="white",
                                  activebackground=COLOR_THEME["exit_active"], relief="flat", cursor="hand2")
        self.exit_btn.pack(pady=20)

        self.display_question()

    # ----------------- Button and UI helpers -----------------
    def create_option_button(self, idx):
        btn = tk.Button(self.top, text="", font=("Helvetica", 12),
                        width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                        bg=COLOR_THEME["button_bg"], fg="white",
                        activebackground=COLOR_THEME["button_active"],
                        relief="flat", bd=0, cursor="hand2")
        btn.config(command=lambda b=btn: self.check_answer(b["text"]))
        btn.pack(pady=10)
        return btn

    def update_timer(self):
        timer_icon = "⏱️ "
        self.timer_label.config(text=f"{timer_icon}Time left: {self.time_left}s")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.top.after(1000, self.update_timer)
        else:
            self.check_answer(None)

    # ----------------- Quiz Navigation -----------------
    def display_question(self):
        if self.timer_id:
            self.top.after_cancel(self.timer_id)
            self.timer_id = None

        if 0 <= self.current_question_index < len(self.quiz_manager.questions):
            data = self.quiz_manager.get_question_at_index(self.current_question_index)
            if data:
                question, *options, correct_answer = data

                if options and isinstance(options[0], list):
                    options = options[0]

                self.correct_answer = correct_answer
                random.shuffle(options)

                self.time_left = 15
                self.update_timer()

                total_questions = len(self.quiz_manager.questions)
                current_question_number = self.current_question_index + 1

                self.progress_label.config(text=f"Question: {current_question_number}/{total_questions}")
                self.question_label.config(text=question)

                for btn, opt in zip(self.options, options):
                    btn.config(text=opt, state="normal", bg=COLOR_THEME["button_bg"], fg="white",
                               font=("Helvetica", 12))

            # Update navigation buttons
            self.prev_btn.config(state=tk.NORMAL if self.current_question_index > 0 else tk.DISABLED)
            self.next_btn.config(state=tk.NORMAL if self.current_question_index < len(self.quiz_manager.questions) - 1 else tk.DISABLED)
        else:
            self.show_results()

    def show_previous_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.display_question()

    def show_next_question(self):
        if self.current_question_index < len(self.quiz_manager.questions) - 1:
            self.current_question_index += 1
            self.display_question()

    # ----------------- Answer Handling -----------------
    def check_answer(self, selected_option):
        if self.timer_id:
            self.top.after_cancel(self.timer_id)
            self.timer_id = None

        for btn in self.options:
            btn.config(state="disabled", font=("Helvetica", 12))

        correct_icon = " ✅"
        incorrect_icon = " ❌"
        light_green = COLOR_THEME["correct_bg"]

        if selected_option:
            is_correct = self.quiz_manager.check_answer(selected_option, self.correct_answer)
            for btn in self.options:
                original_text = btn['text'].split(" ", 1)[-1] if " " in btn['text'] else btn['text']

                if btn['text'] == selected_option:
                    btn.config(bg=light_green if is_correct else "red",
                               text=(correct_icon if is_correct else incorrect_icon) + original_text,
                               font=("Helvetica", 12, "bold"))
                elif btn['text'] == self.correct_answer and not is_correct:
                    btn.config(bg=light_green,
                               text=correct_icon + original_text,
                               font=("Helvetica", 12, "bold"))

            self.top.after(3000, self.display_next_or_results)
        else:
            # Timeout case
            for btn in self.options:
                original_text = btn['text'].split(" ", 1)[-1] if " " in btn['text'] else btn['text']
                if btn['text'] == self.correct_answer:
                    btn.config(bg=light_green,
                               text=correct_icon + original_text,
                               font=("Helvetica", 12, "bold"))

            self.top.after(3000, self.display_next_or_results)

    def display_next_or_results(self):
        if self.current_question_index < len(self.quiz_manager.questions) - 1:
            self.current_question_index += 1
            self.display_question()
        else:
            self.show_results()

    # ----------------- End of Quiz -----------------
    def show_results(self):
        total = len(self.quiz_manager.questions)
        score = self.quiz_manager.score
        percent = (score / total) * 100

        message = (
            f"🎉 {self.username}, your score: {score}/{total}\n"
            f"Accuracy: {percent:.2f}%\n"
            + ("🔥 Great job!" if percent >= 80 else "👍 Keep practicing!")
        )
        messagebox.showinfo("Quiz Completed", message)
        self.quiz_manager.save_score()
        self.ask_replay()

    def ask_replay(self):
        self.show_leaderboard()
        if messagebox.askyesno("Play Again?", "Would you like to play again?"):
            self.top.destroy()
            self.restart_callback()
        else:
            self.top.destroy()

    def confirm_exit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit the quiz?"):
            self.quiz_manager.save_score()
            self.top.destroy()

    # ----------------- Leaderboard -----------------
    def show_leaderboard(self):
        all_scores = self.quiz_manager.db.get_all_scores(self.quiz_manager.language)

        if not all_scores:
            return

        user_rank = None

        for i, (name, score, total, timestamp) in enumerate(all_scores):
            if name == self.username and score == self.quiz_manager.score and total == self.quiz_manager.total_questions:
                user_rank = i + 1
                break

        lb_window = tk.Toplevel(self.top)
        lb_window.title("🏅 Leaderboard")
        lb_window.configure(bg=COLOR_THEME["question_bg"])

        title_label = tk.Label(lb_window, text=f"Top Scores - {self.quiz_manager.language}",
                               font=("Helvetica", 16, "bold"), bg=COLOR_THEME["question_bg"])
        title_label.pack(pady=10)

        lb_text_widget = tk.Text(lb_window, font=("Helvetica", 12), bg="white", fg="black", width=40, height=10)
        lb_text_widget.pack(padx=20, pady=10)

        lb_text_widget.config(state=tk.NORMAL)
        lb_text_widget.delete(1.0, tk.END)
        lb_text_widget.insert(tk.END, "Rank | Name                 | Score     | Date & Time\n")
        lb_text_widget.insert(tk.END, "----------------------------------------------------\n")

        for idx, (name, score, total, timestamp) in enumerate(all_scores[:5]):
            try:
                timestamp = int(timestamp) if isinstance(timestamp, str) else timestamp
                formatted_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                formatted_time = "Invalid time"

            lb_text_widget.insert(tk.END, f"{idx+1:<4} | {name:<20} | {score}/{total:<4} | {formatted_time}\n")

        lb_text_widget.config(state=tk.DISABLED)

        if user_rank is not None:
            rank_label = tk.Label(lb_window, text=f"Your Rank: {user_rank} out of {len(all_scores)}",
                                  font=("Helvetica", 12, "italic"), bg=COLOR_THEME["question_bg"])
            rank_label.pack(pady=5)

        close_button = tk.Button(lb_window, text="Close", command=lb_window.destroy,
                                 font=("Helvetica", 12), bg=COLOR_THEME["button_bg"], fg="white",
                                 activebackground=COLOR_THEME["button_active"], relief="flat", cursor="hand2")
        close_button.pack(pady=10)
