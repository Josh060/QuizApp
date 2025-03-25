import tkinter as tk
from tkinter import messagebox
from languages.python import get_python_questions
from languages.java import get_java_questions
from languages.javascript import get_javascript_questions
from languages.cpp import get_cpp_questions
from languages.php import get_php_questions

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IT Quiz App")

        self.language = tk.StringVar(value="Python")

        tk.Label(root, text="Select Language:", font=("Arial", 12)).pack(pady=5)
        languages = ["Python", "Java", "JavaScript", "C++", "PHP"]

        for lang in languages:
            tk.Radiobutton(root, text=lang, variable=self.language, value=lang, font=("Arial", 10)).pack(anchor="w")

        tk.Button(root, text="Start Quiz", command=self.start_quiz, font=("Arial", 12)).pack(pady=10)

    def start_quiz(self):
        language = self.language.get()
        question_fetcher = {
            "Python": get_python_questions,
            "Java": get_java_questions,
            "JavaScript": get_javascript_questions,
            "C++": get_cpp_questions,
            "PHP": get_php_questions
        }

        questions = question_fetcher.get(language, lambda: [])()

        if not questions:
            messagebox.showerror("Error", f"No questions found for {language}.")
            return

        QuizWindow(self.root, questions)

class QuizWindow:
    def __init__(self, root, questions):
        self.root = root
        self.questions = questions
        self.question_index = 0
        self.score = 0

        for widget in root.winfo_children():
            widget.destroy()

        self.question_label = tk.Label(root, text="", wraplength=500, font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.options = []
        for i in range(4):
            btn = tk.Button(root, text="", font=("Arial", 12), command=lambda i=i: self.check_answer(i))
            btn.pack(pady=5, padx=20, anchor="w")
            self.options.append(btn)

        self.display_question()

    def display_question(self):
        if self.question_index < len(self.questions):
            question, *options, _ = self.questions[self.question_index]
            self.question_label.config(text=f"Q{self.question_index + 1}: {question}")

            for i, option in enumerate(options):
                self.options[i].config(text=option)
        else:
            messagebox.showinfo("Quiz Completed", f"Your score: {self.score}/{len(self.questions)}")
            self.root.destroy()

    def check_answer(self, selected_index):
        _, *options, correct_answer = self.questions[self.question_index]
        if options[selected_index] == correct_answer:
            self.score += 1

        self.question_index += 1
        self.display_question()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
