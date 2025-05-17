# main.py
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Optional, List, Dict, Callable
from quiz_manager import QuizManager
from quiz_window import QuizWindow
from admin_window import AdminWindow
from database import Database
from config import Config
from admin_login import AdminLogin
from review_window import ReviewWindow
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("quiz_app.log"),
        logging.StreamHandler()
    ]
)
class QuizApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Quiz App")
        self.root.attributes('-fullscreen', True)
        self._fullscreen = True
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.grid(row=0, column=0) 
        self.language_frame = ttk.Frame(self.root, style="Language.TFrame")
        self.language_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.tkraise()
        self.language_frame.lower()
        self._configure_styles()
        self._bind_event_handlers()
        self._create_main_ui()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        primary_color = "#4a6baf"
        secondary_color = "#3a5a9f"
        accent_color = "#2a4a8f"
        background_color = "#f5f5f5"
        card_color = "#ffffff"
        text_color = "#333333"
        style.configure('.', background=background_color, foreground=text_color)
        style.configure('Card.TFrame', background=card_color, borderwidth=2, relief="solid", bordercolor="#e0e0e0")
        style.configure('TButton', font=("Helvetica", 12), padding=10, borderwidth=1, relief="flat")
        style.configure('Accent.TButton', background=primary_color, foreground="white", font=("Helvetica", 12, "bold"))
        style.map('Accent.TButton', background=[('active', secondary_color), ('pressed', accent_color)])
        style.configure('TEntry', fieldbackground=card_color, font=("Helvetica", 12))
        style.configure('Header.TLabel', font=("Helvetica", 24, "bold"), foreground=primary_color)
        style.configure('Subheader.TLabel', font=("Helvetica", 16), foreground=text_color)
        style.configure('Footer.TLabel', font=("Helvetica", 10), foreground="#666")
        style.configure('Language.TFrame', background="lightgray")

    def _bind_event_handlers(self):
        self.root.bind("<F11>", self._toggle_fullscreen)
        self.root.bind("<Escape>", self._exit_fullscreen)

    def _create_main_ui(self):
        self.main_frame.grid_columnconfigure(0, weight=1) 
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_rowconfigure(2, weight=0)
        self.main_frame.grid_rowconfigure(3, weight=1)
        content_frame = ttk.Frame(self.main_frame)
        content_frame.grid(row=1, column=0) 
        self._create_header(content_frame)
        self._create_username_section(content_frame)
        self._create_button_section(content_frame)
        self._create_footer(self.main_frame) 

    def _create_header(self, parent):
        header_frame = ttk.Frame(parent)
        header_frame.pack(pady=(0, 20)) 
        ttk.Label(header_frame, text="CYJ IT QUIZ APPLICATION", style='Header.TLabel', anchor="center").pack(fill="x")
        ttk.Label(header_frame, text="Test your IT knowledge", style='Subheader.TLabel', anchor="center").pack(fill="x")

    def _create_username_section(self, parent):
        self.username_frame = ttk.Frame(parent, padding=20, style='Card.TFrame')
        self.username_frame.pack(pady=10)
        ttk.Label(self.username_frame, text=f"{Config.USERNAME_LABEL_TEXT}: ", font=("Helvetica", 14)).grid(row=0, column=0, sticky="e", padx=(0, 10))
        self.username_entry = ttk.Entry(self.username_frame, font=("Helvetica", 14), width=25)
        self.username_entry.grid(row=0, column=1, sticky="w")
        self.username_entry.focus_set()
        self.username_entry.bind("<Return>", lambda e: self.start_quiz())

    def _create_button_section(self, parent):
        self.button_frame = ttk.Frame(parent)
        self.button_frame.pack(pady=20) 
        self.button_frame.grid_columnconfigure((0, 1), weight=1, uniform="cols")
        btn_opts = {'style': 'Accent.TButton', 'padding': 12}
        ttk.Button(self.button_frame, text=Config.START_BUTTON_TEXT, command=self.start_quiz, **btn_opts).grid(row=0, column=0, sticky="ew", pady=5, padx=(0, 5))
        ttk.Button(self.button_frame, text=Config.ADMIN_BUTTON_TEXT, command=self.open_admin_login, **btn_opts).grid(row=0, column=1, sticky="ew", pady=5, padx=(5, 0))
        ttk.Button(self.button_frame, text="View High Scores", command=self._show_high_scores, **btn_opts).grid(row=1, column=0, columnspan=2, sticky="ew", pady=(5, 0))
        ttk.Button(self.button_frame, text="Exit", command=self._safe_exit, **btn_opts).grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))

    def _create_footer(self, parent):
        ttk.Label(parent, text="Press F11 for fullscreen | Esc to exit fullscreen", style='Footer.TLabel', anchor="center").grid(row=3, column=0, pady=(20, 0), sticky="ew")

    def _show_high_scores(self):
        try:
            all_scores = self.db.get_high_scores()
            if not all_scores:
                messagebox.showinfo("High Scores", "No high scores available.")
                return
            top_score_window = tk.Toplevel(self.root)
            top_score_window.title("High Scores")
            top_score_window.grab_set()
            top_score_window.resizable(False, False)
            self.displayed_scores = tk.IntVar(value=10)
            score_limit_options = [10, 20, 50, "All"]
            limit_frame = ttk.Frame(top_score_window, padding=5)
            limit_frame.pack(pady=(5, 0))
            ttk.Label(limit_frame, text="Show Top:").pack(side="left", padx=5)
            limit_combo = ttk.Combobox(limit_frame, textvariable=self.displayed_scores, values=score_limit_options, state="readonly")
            limit_combo.bind("<<ComboboxSelected>>", self._update_displayed_scores)
            limit_combo.pack(side="left")
            limit_combo.set(10)
            self.scores_tree = ttk.Treeview(top_score_window, columns=("Rank", "Username", "Score", "Language"), show="headings")
            self.scores_tree.heading("Rank", text="Rank")
            self.scores_tree.heading("Username", text="Username")
            self.scores_tree.heading("Score", text="Score")
            self.scores_tree.heading("Language", text="Language")
            self.scores_tree.column("Rank", width=50, anchor="center")
            self.scores_tree.column("Username", width=150)
            self.scores_tree.column("Score", width=100, anchor="center")
            self.scores_tree.column("Language", width=100, anchor="center")
            scrollbar = ttk.Scrollbar(top_score_window, orient="vertical", command=self.scores_tree.yview)
            self.scores_tree.configure(yscrollcommand=scrollbar.set)
            self.scores_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            scrollbar.pack(side="right", fill="y")
            self._update_treeview_with_scores(all_scores)
            close_button = ttk.Button(top_score_window, text="Close", command=top_score_window.destroy)
            close_button.pack(pady=5)
            self._center_window_toplevel(top_score_window)
        except Exception as e:
            logging.error(f"Failed to fetch high scores: {e}")
            messagebox.showerror("Error", "Could not fetch high scores.")

    def _update_displayed_scores(self, event):
        selected_limit = self.displayed_scores.get()
        all_scores = self.db.get_high_scores()
        if selected_limit == "All":
            self._update_treeview_with_scores(all_scores)
        else:
            try:
                limit = int(selected_limit)
                self._update_treeview_with_scores(all_scores[:limit])
            except ValueError:
                logging.error(f"Invalid score limit: {selected_limit}")
                messagebox.showerror("Error", "Invalid score limit selected.")

    def _update_treeview_with_scores(self, scores, limit="All"):
        for item in self.scores_tree.get_children():
            self.scores_tree.delete(item)
        if limit == "All":
            scores_to_display = scores
        else:
            try:
                num_limit = int(limit)
                scores_to_display = scores[:num_limit]
            except ValueError:
                logging.error(f"Invalid score limit: {limit}")
                messagebox.showerror("Error", "Invalid score limit selected.")
                return
        for i, row in enumerate(scores_to_display):
            self.scores_tree.insert("", tk.END, values=(i + 1, row['user_name'], row['score'], row['language']))

    def _center_window_toplevel(self, top_level):
        top_level.update_idletasks()
        w = top_level.winfo_width()
        h = top_level.winfo_height()
        sw = top_level.winfo_screenwidth()
        sh = top_level.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        top_level.geometry(f'+{x}+{y}')


    def start_quiz(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showwarning("Input Error", "Please enter a valid username.")
            self.username_entry.focus_set()
            return
        self.username = username
        logging.info(f"Starting quiz for user: {username}")
        self._show_language_selection()

    def _show_language_selection(self):
        self._clear_main_ui()
        for widget in self.language_frame.winfo_children():
            widget.destroy()
        self.language_frame.configure(padding="30")
        self.language_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.language_frame.grid_rowconfigure(1, weight=1)
        self.language_frame.grid_columnconfigure(0, weight=1)
        ttk.Label(self.language_frame, text="Select Quiz Language", style='Header.TLabel', anchor="center").grid(row=0, column=0, sticky="n", pady=(0, 20))
        languages = self._fetch_languages_from_database()
        if not languages:
            messagebox.showerror("Error", "No quiz languages available. Please contact admin.")
            self._back_to_main_from_language_selection()
            return
        self._create_language_buttons(languages)
        self._create_action_buttons()
        self.language_frame.tkraise()

    def _fetch_languages_from_database(self) -> List[str]:
        try:
            return self.db.fetch_languages()
        except Exception as e:
            logging.error(f"Error fetching languages: {e}")
            messagebox.showerror("Database Error", "Could not fetch available languages.")
            return []

    def _create_language_buttons(self, languages: List[str]):
        button_frame = ttk.Frame(self.language_frame)
        button_frame.grid(row=1, column=0, pady=(15, 30))
        self.language_buttons = {}
        for i, lang in enumerate(languages):
            btn = ttk.Button(button_frame, text=lang.capitalize(), style='Accent.TButton', padding=20,
                             command=lambda l=lang: self._select_language(l),
                             state=tk.DISABLED if hasattr(self, 'quiz_window_active') and self.quiz_window_active else tk.NORMAL)
            btn.grid(row=i, column=0, pady=5, padx=20)
            self.language_buttons[lang] = btn

    def _create_action_buttons(self):
        button_bar = ttk.Frame(self.language_frame)
        button_bar.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        button_bar.grid_columnconfigure((0, 1), weight=1, uniform="cols")
        ttk.Button(button_bar, text="Back to Main", command=self._back_to_main_from_language_selection, style='TButton', padding=8).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(button_bar, text="Admin Login", command=self.open_admin_login, style='TButton', padding=8).grid(row=0, column=1, sticky="ew", padx=(5, 0))

    def _back_to_main_from_language_selection(self):
        print("Switching back to the main frame...")
        self.language_frame.grid_forget()
        self._create_main_ui()
        self.main_frame.tkraise()
        self.root.after(100, self.root.update)

    def _select_language(self, language: str):
        if hasattr(self, 'quiz_window_active') and self.quiz_window_active:
            return
        try:
            questions = self.db.get_questions_by_language(language)
            if not questions:
                messagebox.showwarning("No Questions", f"No questions available for {language}.")
                return
            self._start_quiz_window(questions, language)
        except Exception as e:
            logging.error(f"Error starting quiz: {e}")
            messagebox.showerror("Error", f"Could not start quiz: {str(e)}")

    def _start_quiz_window(self, questions: List, language: str):
        logging.info(f"Starting quiz window for {language} with {len(questions)} questions")
        self.quiz_manager = QuizManager(self.root, self.db, language, self.username)
        self.quiz_window = QuizWindow(self.root, self.quiz_manager, on_quiz_finish=self.handle_quiz_completion)
        self.quiz_window_active = True
        self._disable_language_buttons()
        self.language_frame.grid_forget()
        self.root.attributes('-fullscreen', True)

    def _on_quiz_finished(self, results: Dict):
        logging.info(f"Quiz finished for {self.username} in {results['language']} with score: {results['score']}/{results['total']}")
        messagebox.showinfo("Quiz Finished", f"Your score: {results['score']}/{results['total']}")
        self._restart_quiz()

    def _restart_quiz(self):
        logging.info("Restarting quiz process")
        if hasattr(self, 'quiz_window'):
            self.quiz_window.destroy()
            self.quiz_window = None
        self.quiz_window_active = False
        self.quiz_manager = None
        self._enable_language_buttons()
        self._show_language_selection()

    def _disable_language_buttons(self):
        if hasattr(self, 'language_buttons'):
            for button in self.language_buttons.values():
                button.config(state=tk.DISABLED)

    def _enable_language_buttons(self):
        if hasattr(self, 'language_buttons'):
            for button in self.language_buttons.values():
                button.config(state=tk.NORMAL)

    def open_admin_login(self):
        def on_admin_login_success():
            logging.info("Admin login successful, opening admin window")
            self.root.withdraw()  
            admin_window = AdminWindow(self.root, self.db)
            admin_window.attributes("-fullscreen", True)  
            admin_window.protocol("WM_DELETE_WINDOW", lambda: self._return_from_admin(admin_window))
            admin_window.grab_set()
        AdminLogin(self.root, success_callback=on_admin_login_success)

    def _clear_main_ui(self):
        for widget in self.main_frame.winfo_children():
            widget.grid_forget()

    def back_to_main(self):
        print("QuizApp: back_to_main called")
        if hasattr(self, 'review_window') and self.review_window.winfo_exists():
            self.review_window.destroy()  
        self.root.deiconify()  
        self._restart_quiz()  

    def _safe_exit(self):
        logging.info("Exiting the application...")
        self.root.quit()
        self.root.destroy()

    def _toggle_fullscreen(self, event=None):
        self._fullscreen = not self._fullscreen
        self.root.attributes("-fullscreen", self._fullscreen)

    def _exit_fullscreen(self, event=None):
        if self._fullscreen:
            self._toggle_fullscreen()

    def _center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")


    def handle_quiz_completion(self, results, exited=False):
        print("Quiz Completion Callback Received:")
        print(f"Username: {results.get('username')}")
        print(f"Language: {results.get('language')}")
        print(f"User Answers: {results.get('answers')}")
        self.root.withdraw()
    
        if hasattr(self, 'quiz_window') and self.quiz_window.winfo_exists():
            self.quiz_window.destroy()
        self.quiz_window_active = False

        if not exited:
            print(f"Correct Answers: {results.get('correct_answers')}")
            print(f"Score: {results.get('score')}")
            print(f"Total Questions: {results.get('total_questions')}")
            print("Quiz completed. Showing review window.")

            self.review_window = ReviewWindow(
                self.root, self.quiz_manager, self._restart_quiz, self.back_to_main
            )
            self.root.withdraw()
            self.review_window.protocol("WM_DELETE_WINDOW", self._on_review_close)
        else:
            print("Quiz exited early. Returning to language selection.")
            self.quiz_manager = None
            self._enable_language_buttons()
            self.language_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            self.language_frame.tkraise()
            self.root.attributes('-fullscreen', True)
            self.root.deiconify()

    def _on_review_close(self):
        """Handles the closing of the quiz review window."""
        print("Review window closed.")
        self.root.deiconify()
        self._restart_quiz()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    print("Starting...")
    try:
        print("Initializing Database...")
        db = Database()
        print("Database initialized.")
        print("Creating root window...")
        root = tk.Tk()
        print("Root window created.")
        try:
            test_frame = ttk.Frame(root, background="red")
            test_frame.pack()
            test_frame.destroy()
            print("ttk.Frame background option seems to be working.")
        except tk.TclError as e:
            print(f"Error testing ttk.Frame background: {e}")
        print("Initializing QuizApp...")
        app = QuizApp(root, db)
        print("QuizApp initialized.")
        print("Running mainloop...")
        app.run()
        print("Mainloop finished.")
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Startup Error", f"Failed to start application: {e}")
    finally:
        if 'db' in locals() and db:
            db.close()
        print("Exiting.")
