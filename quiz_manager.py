from datetime import datetime
from database import Database
from tkinter import messagebox
import tkinter as tk
from mysql.connector import Error


class QuizManager:
    def __init__(self, db, language, username):
        self.db = db
        self.language = language
        self.username = username
        self.questions = []
        self.current_question_index = 0
        self.score = 0
        self.total_questions = 0
        
        if not language:
            raise ValueError("Language must be provided")
        
        # Load questions
        self.load_questions(language)

    def load_questions(self, language):
        """Load questions from the database for the selected language."""
        try:
            if not self.db.connection:  # Check if the connection exists
                raise Exception("Database connection is not established.")
            
            print(f"Loading questions for language: {language}")

            # Check if the language is empty
            if not language:
                raise ValueError("No language selected")
        
            table_name = f"{language.lower()}_questions"  # Dynamically set the table name
            query = f"SELECT question, option1, option2, option3, option4, correct_answer FROM {table_name}"

            # Check if the table exists (using SHOW TABLES)
            cursor = self.db.connection.cursor()
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            if not cursor.fetchone():
                raise Exception(f"Table '{table_name}' does not exist.")
            
            # Now execute the SELECT query
            cursor.execute(query)
            rows = cursor.fetchall()

            if rows:
                # Process the rows into a dictionary format
                self.questions = [{"question": row[0], "options": [row[1], row[2], row[3], row[4]], "correct_answer": row[5]} for row in rows]
                self.total_questions = len(self.questions)
            else:
                print(f"No questions found for {language}")
                raise Exception(f"No questions found for '{language}'")
        except Exception as e:
            print(f"Error loading questions for {language}: {e}")
            raise Exception(f"An error occurred while loading questions: {e}")

    def get_questions(self, language):
        table_name = f"{language}_questions"  # This dynamically selects the correct table
        query = f"SELECT question, option1, option2, option3, option4, correct_answer FROM {table_name}"
        self.db.execute(query)
        return self.db.fetchall()

    def get_question_at_index(self, index):
        """Get the question at a specific index."""
        if 0 <= index < len(self.questions):
            data = self.questions[index]
            return data["question"], data["options"], data["correct_answer"]
        return None

    def record_answer(self, selected_option, correct_answer):
        """Record the answer and update the score."""
        if selected_option == correct_answer:
            self.score += 1

    def has_next_question(self):
        """Check if there is a next question."""
        return self.current_question_index + 1 < self.total_questions

    def advance_to_next_question(self, question_label, option_buttons):
        """Move to the next question."""
        if self.has_next_question():
            self.current_question_index += 1
            self.show_question(question_label, option_buttons)

    def check_answer(self, selected_option, correct_answer):
        """Check if the selected option is correct."""
        if selected_option == correct_answer:
            self.score += 1
            return True
        return False

    def get_next_question(self):
        """Get the next question."""
        return self.get_question()

    def end_quiz(self):
        """End the quiz and save the score."""
        self.save_score()
        print(f"Quiz completed! {self.username} scored {self.score}/{self.total_questions}.")
        messagebox.showinfo("Quiz Completed", f"You scored {self.score}/{self.total_questions}")
        
    def save_score(self):
        """Save the final score to the database."""
        if not self.db.connection:
            print("Error: No database connection.")
            return

        try:
            query = "INSERT INTO scores (username, language, score, total_questions) VALUES (%s, %s, %s, %s)"
            cursor = self.db.connection.cursor()
            cursor.execute(query, (self.username, self.language, self.score, self.total_questions))
            self.db.connection.commit()
            print(f"Score saved for {self.username} in {self.language}: {self.score}/{self.total_questions} at {datetime.now()}")
        except Exception as err:
            print(f"Error saving score: {err}")
            
    def get_top_scores_with_time(self):
        return self.db.get_top_scores(self.language)

    def show_next_question(self):
        """Show the next question in the quiz."""
        question, options, correct_answer = self.get_next_question()
