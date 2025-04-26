import tkinter as tk
from tkinter import messagebox
from style import COLOR_THEME
from database import Database  # Import Database class from database.py
import datetime

class AdminWindow:
    def __init__(self, root, db_manager):
        # Initialize the admin window
        self.top = tk.Toplevel(root)
        self.top.title("Admin Mode - Add Questions")
        self.top.configure(bg=COLOR_THEME["bg"])
        self.db_manager = db_manager

        # Question Section
        self.question_label = tk.Label(self.top, text="Question:", font=("Helvetica", 12), bg=COLOR_THEME["bg"], fg="white")
        self.question_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.question_entry = tk.Entry(self.top, width=50)
        self.question_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Options Section
        self.options_labels = []
        self.options_entries = []
        for i in range(4):
            label = tk.Label(self.top, text=f"Option {chr(65 + i)}:", font=("Helvetica", 12), bg=COLOR_THEME["bg"], fg="white")
            label.grid(row=i + 1, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(self.top, width=50)
            entry.grid(row=i + 1, column=1, padx=5, pady=5, sticky="ew")
            self.options_labels.append(label)
            self.options_entries.append(entry)

        # Correct Answer Section
        self.correct_answer_label = tk.Label(self.top, text="Correct Answer (A, B, C, or D):", font=("Helvetica", 12), bg=COLOR_THEME["bg"], fg="white")
        self.correct_answer_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.correct_answer_entry = tk.Entry(self.top, width=5)
        self.correct_answer_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Language Section
        self.language_label = tk.Label(self.top, text="Language:", font=("Helvetica", 12), bg=COLOR_THEME["bg"], fg="white")
        self.language_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.language_entry = tk.Entry(self.top, width=20)
        self.language_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # Add Button
        self.add_button = tk.Button(self.top, text="Add Question", command=self.add_new_question, font=("Helvetica", 12),
                                     bg=COLOR_THEME["button_bg"], fg="white", activebackground=COLOR_THEME["button_active"], relief="flat")
        self.add_button.grid(row=7, column=0, columnspan=2, pady=20)

        # Close Button
        self.close_button = tk.Button(self.top, text="Close Admin", command=self.top.destroy, font=("Helvetica", 12),
                                      bg=COLOR_THEME["exit_bg"], fg="white", activebackground=COLOR_THEME["exit_active"], relief="flat")
        self.close_button.grid(row=8, column=0, columnspan=2, pady=10)

        # View Scores Button
        self.view_scores_button = tk.Button(self.top, text="View Scores", command=self.view_scores, font=("Helvetica", 12),
                                             bg=COLOR_THEME["button_bg"], fg="white", activebackground=COLOR_THEME["button_active"], relief="flat")
        self.view_scores_button.grid(row=9, column=0, columnspan=2, pady=10)

        self.top.grid_columnconfigure(1, weight=1)  # Make the entry fields expand

    def add_new_question(self):
        question_text = self.question_entry.get()
        options = [entry.get() for entry in self.options_entries]
        correct_answer_letter = self.correct_answer_entry.get().upper()
        language = self.language_entry.get()

        # Validate that the language is supported
        if not language.isalpha() or len(language) > 20:
            messagebox.showerror("Error", f"Invalid language '{language}'. Please enter a valid language.")
            return

        if not question_text or not all(options) or not correct_answer_letter or not language:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if correct_answer_letter not in ["A", "B", "C", "D"]:
            messagebox.showerror("Error", "Correct answer must be A, B, C, or D.")
            return

        correct_answer = options[ord(correct_answer_letter) - ord('A')]

        try:
            # Add question to the database
            self.db_manager.add_question(question_text, options[0], options[1], options[2], options[3], correct_answer, language)
            messagebox.showinfo("Success", "Question added successfully!")
            # Clear the fields after adding
            self.question_entry.delete(0, tk.END)
            for entry in self.options_entries:
                entry.delete(0, tk.END)
            self.correct_answer_entry.delete(0, tk.END)
            self.language_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Error adding question to database: {e}")

    def view_scores(self):
        scores_window = tk.Toplevel(self.top)
        scores_window.title("User Scores")
        scores_window.configure(bg=COLOR_THEME["bg"])

        try:
            # Fetch all raw scores
            raw_scores = self.db_manager.get_all_scores()
            if not raw_scores:
                messagebox.showinfo("Info", "No scores available yet.")
                scores_window.destroy()
                return
        except Exception as e:
            messagebox.showerror("Error", f"Error loading scores: {e}")
            scores_window.destroy()
            return

        # Filter to only latest score per user+language
        latest_scores = {}
        for username, score, total_questions, timestamp, language in raw_scores:
            key = (username, language)
            if key not in latest_scores or timestamp > latest_scores[key][3]:
                latest_scores[key] = (username, score, total_questions, timestamp, language)

        sorted_scores = sorted(latest_scores.values(), key=lambda x: x[3], reverse=True)  # sort by timestamp desc

        for idx, (username, score, total_questions, timestamp, language) in enumerate(sorted_scores, start=1):
            if isinstance(timestamp, str):
                try:
                    formatted_time = datetime.datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    formatted_time = "Invalid time"
            elif isinstance(timestamp, (datetime.datetime, datetime.date)):
                formatted_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            else:
                formatted_time = "Invalid time"

            label = tk.Label(scores_window, 
                             text=f"{idx}. {username} [{language}] - {score}/{total_questions} pts - {formatted_time}",
                             font=("Helvetica", 12), 
                             bg=COLOR_THEME["bg"], 
                             fg="white", 
                             anchor="w")
            label.pack(fill="both", padx=10, pady=2)

def create_db_manager():
    try:
        db_manager = Database(host="localhost", user="root", password="", database="quiz_db")
        if not db_manager.check_connection():
            messagebox.showerror("Error", "Database connection failed.")
            return None
        return db_manager
    except Exception as e:
        messagebox.showerror("Error", f"Error initializing database: {e}")
        return None

if __name__ == "__main__":
    root = tk.Tk()

    # Create and check database manager
    db_manager = create_db_manager()
    if db_manager is None:
        root.quit()  # Quit if database manager creation fails
    else:
        admin_window = AdminWindow(root, db_manager)
        root.mainloop()

    db_manager.close()  # Close the database connection properly when exiting
