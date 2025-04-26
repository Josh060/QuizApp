# main.py
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import json

from quiz_manager import QuizManager
from quiz_window import QuizWindow
from admin_window import AdminWindow
from style import *
from database import Database

# Window Constants
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
APP_TITLE = "Quiz App"

# Labels and Button Texts
USERNAME_LABEL_TEXT = "Username:"
START_BUTTON_TEXT = "Start Quiz"
RESTART_BUTTON_TEXT = "Restart App"
ADMIN_BUTTON_TEXT = "Admin Mode"

# Language Selection
LANGUAGE_SELECTION_TITLE = "Select Language"
CHOOSE_LANGUAGE_TEXT = "Choose a Language:"

# Error Messages
USERNAME_ERROR_EMPTY = "Please enter a valid username."
NO_QUESTIONS_ERROR = "No questions found for '{language}'."

# Load languages from config (optional)
try:
    with open("config.json", "r") as f:
        config = json.load(f)
        LANGUAGES = config.get("languages", ["Python", "Java", "C++", "JavaScript"])
except (FileNotFoundError, json.JSONDecodeError):
    LANGUAGES = ["Python", "Java", "C++", "JavaScript"]
    print("Warning: Could not load languages from config.json. Using defaults.")

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.configure(bg=COLOR_THEME["bg"])
        self.center_window(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.db = Database()  # Connect to database
        self.quiz_manager = None

        self.last_username = tk.StringVar()
        self.load_last_username()

        # Username Label
        self.username_label = tk.Label(self.root, text=USERNAME_LABEL_TEXT, font=("Helvetica", 14),
                                       bg=COLOR_THEME["bg"], fg="white")
        self.username_label.pack(pady=10)

        # Username Entry
        self.username_entry = tk.Entry(self.root, font=("Helvetica", 12), textvariable=self.last_username)
        self.username_entry.pack(pady=5)
        self.username_entry.bind("<Return>", lambda event: self.show_language_buttons())

        # Start Button
        self.start_button = tk.Button(self.root, text=START_BUTTON_TEXT, command=self.show_language_buttons,
                                      font=("Helvetica", 16),
                                      bg=COLOR_THEME["start_bg"], fg="white",
                                      activebackground=COLOR_THEME["start_active"],
                                      relief="flat", padx=20, pady=10)
        self.start_button.pack(pady=20)

        # Restart Button
        self.restart_button = tk.Button(self.root, text=RESTART_BUTTON_TEXT, command=self.restart_app,
                                        font=("Helvetica", 12),
                                        bg=COLOR_THEME["button_bg"], fg="white",
                                        activebackground=COLOR_THEME["button_active"],
                                        relief="flat", padx=10, pady=5)
        self.restart_button.pack(pady=10)

        # Admin Mode Button
        self.admin_button = tk.Button(self.root, text=ADMIN_BUTTON_TEXT, command=self.open_admin_login,
                                      font=("Helvetica", 12),
                                      bg=COLOR_THEME["button_bg"], fg="white",
                                      activebackground=COLOR_THEME["button_active"],
                                      relief="flat", padx=10, pady=5)
        self.admin_button.pack(pady=10)

        # Language Frame
        self.language_frame = tk.Frame(self.root, bg=COLOR_THEME["bg"])
        self.language_buttons = {}

        # Window Close
        self.root.protocol("WM_DELETE_WINDOW", self.exit_application)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def load_last_username(self):
        try:
            with open("last_username.txt", "r") as f:
                self.last_username.set(f.readline().strip())
        except FileNotFoundError:
            pass

    def save_last_username(self):
        username = self.username_entry.get().strip()
        if username:
            with open("last_username.txt", "w") as f:
                f.write(username)

    def show_language_buttons(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", USERNAME_ERROR_EMPTY)
            return

        self.save_last_username()

        # Hide initial widgets
        self.username_label.pack_forget()
        self.username_entry.pack_forget()
        self.start_button.pack_forget()

        # Display language options
        language_label = tk.Label(self.language_frame, text=CHOOSE_LANGUAGE_TEXT, font=("Helvetica", 14),
                                  bg=COLOR_THEME["bg"], fg="white")
        language_label.pack(pady=10)

        for lang in LANGUAGES:
            btn = tk.Button(self.language_frame, text=lang, font=("Helvetica", 12),
                            bg=COLOR_THEME["start_bg"], fg="white",
                            activebackground=COLOR_THEME["start_active"],
                            relief="flat", padx=10, pady=5,
                            command=lambda l=lang: self.start_quiz(username, l))
            btn.pack(pady=5)
            self.language_buttons[lang] = btn

        self.language_frame.pack(pady=20)

    def start_quiz(self, username, language):
        print(f"Starting quiz: {username} - {language}")
        try:
            quiz_manager = QuizManager(self.db, language, username)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred loading quiz for '{language}': {e}")
            return

        if quiz_manager.questions:
            self.quiz_manager = quiz_manager
            QuizWindow(self.root, self.quiz_manager, username, self.restart_app)
            self.root.withdraw()
        else:
            messagebox.showerror("Error", NO_QUESTIONS_ERROR.format(language=language))

    def open_admin_login(self):
        try:
            AdminWindow(self.root, self.db)  # <-- FIXED: pass self.db directly!
            self.root.withdraw()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred opening admin mode: {e}")

    def restart_app(self):
        self.root.destroy()
        new_root = tk.Tk()
        QuizApp(new_root)
        new_root.mainloop()

    def exit_application(self):
        self.save_last_username()
        self.db.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
