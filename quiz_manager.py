# quiz_manager.py
from datetime import datetime
from tkinter import messagebox
import logging
from mysql.connector import Error
from database import Database
import tkinter as tk
import random

class QuizManager:
    def __init__(self, root, db: Database, language, username):
        self.root = root
        self.db = db
        self.language = language
        self.username = username
        self.questions = []
        self.total_questions = 0
        self.current_question_index = 0
        self.score = 0
        self.user_answers = {}
        self.correct_answers = []
        self.quiz_ended = False
        self.timed_out_answers = []
        self._load_questions()
        self.question_timers = {}
        logging.info(f"Quiz started for {username} in {language} with {self.total_questions} questions.")

    def _load_questions(self):
        """Load a random subset of questions from the database for the selected language."""
        num_questions_to_display = 10
        try:
            if not self.db.check_connection():
                raise ValueError("Database connection is not available.")
            all_questions = self.db.get_questions_by_language(self.language)
            logging.debug(f"All raw questions for {self.language}: {all_questions}")

            if not all_questions:
                logging.error(f"No questions found for language: {self.language}")
                messagebox.showerror("No Questions", "No questions available for the selected language.")
                self.quiz_ended = True
                return
            if len(all_questions) > num_questions_to_display:
                self.questions = random.sample(all_questions, num_questions_to_display)
            else:
                self.questions = all_questions

            for q in self.questions:
                if 'options' in q and isinstance(q['options'], list):
                    random.shuffle(q['options'])
                    sanitized_correct_answer = q['correct_answer'].strip().lower()
                    try:
                        sanitized_options = [opt.strip().lower() for opt in q['options']]
                        q['correct_option_index'] = sanitized_options.index(sanitized_correct_answer)
                    except ValueError:
                        logging.error(f"Correct answer '{q['correct_answer']}' not found in options for question: {q.get('question', 'unknown question')}")
                        q['correct_option_index'] = -1
                else:
                    logging.error(f"Question missing 'options' or 'options' is not a list: {q}")
                    self.questions.remove(q)
                    continue
            self.total_questions = len(self.questions)
            logging.info(f"Quiz started for {self.username} in {self.language} with {self.total_questions} random questions.")
            logging.debug(f"Selected and processed questions: {self.questions}")


        except Exception as e:
            logging.error(f"Failed to start quiz for {self.language}: {e}")
            messagebox.showerror("Quiz Error", f"Failed to load quiz questions: {e}")
            self.quiz_ended = True
            raise

    def reset(self):
        """Reset the quiz state for a new session with random questions."""
        self.questions = []
        self.current_question_index = 0
        self.score = 0
        self.total_questions = 0
        self.user_answers = {}
        self.quiz_ended = False
        self._load_questions()

    def get_current_question_data(self):
        """Returns the data for the current question, including the randomized options."""
        if 0 <= self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None

    def check_answer(self, selected_answer_text):
        if not self.quiz_ended and 0 <= self.current_question_index < len(self.questions):
            current_question = self.questions[self.current_question_index]
            correct_answer = current_question['correct_answer']
            logging.debug(f"Question {self.current_question_index + 1}: DB Correct Answer: '{correct_answer}', User Selected: '{selected_answer_text}'")
            correct_answer_processed = correct_answer.strip().lower()
            selected_answer_processed = selected_answer_text.strip().lower()
            is_correct = False
            if selected_answer_processed == correct_answer_processed:
                self.score += 1
                logging.info(f"Question {self.current_question_index + 1}: Correct answer by {self.username}.")
                is_correct = True
            else:
                logging.info(f"Question {self.current_question_index + 1}: Incorrect answer by {self.username}. Correct was '{correct_answer}'.")
            return is_correct
        return False

    def initialize_timer_for_question(self, index, default_time=15):
        if index not in self.question_timers:
            self.question_timers[index] = {
                "time_left": default_time,
                "start_time": None
            }
    def update_time_left(self, index, remaining_time):
        if index in self.question_timers:
            self.question_timers[index]["time_left"] = remaining_time

    def get_remaining_time(self, index):
        return self.question_timers.get(index, {}).get("time_left", 15)

    def has_next_question(self):
        """Check if there are more questions."""
        return self.current_question_index < len(self.questions) - 1

    def advance_to_next_question(self):
        """Move to the next question."""
        if self.has_next_question():
            self.current_question_index += 1

    def decrement_question_index(self):
        """Move to the previous question."""
        if self.current_question_index > 0:
            self.current_question_index -= 1

    def finalize_quiz(self, user_answers):
        self.user_answers = user_answers
        self.correct_answers = [q['correct_answer'] for q in self.questions]
        self.score = 0
        for i, user_answer in self.user_answers.items():
            if user_answer is None:  # Mark this as a timed-out question
                self.timed_out_answers.append(i)
            else:
                try:
                    correct_answer = self.questions[int(i)]['correct_answer']
                    user_answer_processed = user_answer.strip().lower()
                    correct_answer_processed = correct_answer.strip().lower()
                    if user_answer_processed == correct_answer_processed:
                        self.score += 1
                except IndexError:
                    logging.error(f"IndexError in finalize_quiz for question index: {i}")
        logging.debug(f"User Answers: {self.user_answers}")
        logging.debug(f"Correct Answers (from questions): {self.correct_answers}")
        self.end_quiz()
        return {
            "score": self.score,
            "total_questions": self.total_questions,
            "answers": self.user_answers,
            "correct_answers": self.correct_answers,
            "timed_out_answers": self.timed_out_answers,  # Include timed-out answers here
            "username": self.username,
            "language": self.language,
            "quiz_data": self.questions
        }


    def end_quiz(self):
        """End the quiz, save the score."""
        if not self.quiz_ended:
            self._save_score()
            print(f"Quiz completed! {self.username} scored {self.score}/{self.total_questions}.")
            self.quiz_ended = True
        else:
            print("Quiz already ended, skipping further actions.")

    def _save_score(self):
        """Save the user's score to the database (quiz_history)."""
        timestamp = datetime.now()
        try:
            self.db.save_user_score(self.username, self.language, self.score, self.total_questions, timestamp)
            print(f"Score saved for {self.username} in {self.language}: {self.score}/{self.total_questions} at {timestamp}")
        except Error as e:
            logging.error(f"Error saving score: {e}")
            messagebox.showerror("Database Error", "Could not save your score.")

    def get_current_question_index(self):
        """Returns the current question index (0-based)."""
        return self.current_question_index

    def get_total_questions(self):
        """Returns the total number of questions in the quiz."""
        return self.total_questions

    def get_score(self):
        """Returns the current score."""
        return self.score

    def record_answer(self, question_index, selected_option_text, user_answers: dict) -> bool:
        """
        Record the user's answer for a specific question.
        Returns True if all questions have been answered.
        """
        user_answers[question_index] = selected_option_text
        return len(user_answers) == self.get_total_questions()

    def _highlight_true_false_feedback(self, selected_index, correct_index, is_correct):
        light_green = "#90EE90"
        red_color = "red"
        if hasattr(self, 'option_buttons') and self.option_buttons:
            self.option_buttons[correct_index].config(bg=light_green, activebackground=light_green)
            if not is_correct and selected_index != correct_index:
                self.option_buttons[selected_index].config(bg=red_color, activebackground=red_color)

    def _highlight_answer_feedback(self, options, correct_answer, selected_index, is_correct, correct_index_for_highlight):
        light_green = "#90EE90"
        red_color = "red"
        if hasattr(self, 'option_buttons') and self.option_buttons:
            try:
                self.option_buttons[correct_index_for_highlight].config(bg=light_green, activebackground=light_green)
                if not is_correct and selected_index != correct_index_for_highlight:
                    self.option_buttons[selected_index].config(bg=red_color, activebackground=red_color)
            except IndexError:
                logging.error(f"Index out of bounds in option buttons for index: {correct_index_for_highlight}")
        logging.debug(f"Raw Correct Answer: '{correct_answer}', Raw Options: {options}")
        sanitized_options = [opt.strip().lower() for opt in options]
        sanitized_correct_answer = correct_answer.strip().lower()
        logging.debug(f"Sanitized Correct Answer: '{sanitized_correct_answer}', Sanitized Options: {sanitized_options}")

    def get_current_results(self):
        """Returns a dictionary containing the current quiz state."""
        return {
            'username': self.username,
            'language': self.language,
            'answers': self.user_answers
        }
