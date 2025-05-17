# database.py
import mysql.connector
from mysql.connector import Error
import logging

class Database:
    def __init__(self, host="localhost", user="root", password="", database="quiz_db", table_prefix=""):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self.table_prefix = table_prefix
        self.connect()

    def connect(self):
        """Establish a connection to the MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                logging.info(f"Connected to MySQL database: {self.database}@{self.host}")
        except Error as e:
            logging.error(f"Error connecting to MySQL: {e}")
            raise

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            logging.info("MySQL connection closed.")

    def check_connection(self):
        """Check if the connection to the database is active."""
        if self.connection and self.connection.is_connected():
            return True
        return False

    def fetch_languages(self):
        """Fetch all available languages from the database."""
        try:
            if not self.check_connection():
                self.connect()
            cursor = self.connection.cursor()
            query = "SELECT TABLE_NAME FROM information_schema.tables WHERE table_schema = %s AND table_name IN ('cpp_questions', 'java_questions', 'javascript_questions', 'python_questions')"
            cursor.execute(query, (self.database,))
            results = cursor.fetchall()
            languages = [row[0].replace('_questions', '') for row in results]
            cursor.close()
            logging.info(f"Languages found: {languages}")
            return languages
        except Error as e:
            logging.error(f"Error fetching languages: {e}")
            return []

    def get_questions_by_language(self, language):
        """Fetch questions for a specific language from the database, including question type."""
        try:
            if not self.check_connection():
                self.connect()
            cursor = self.connection.cursor(dictionary=True)
            table_name = f"{self.table_prefix}{language}_questions"
            query = f"SELECT id, question, option1, option2, option3, option4, correct_answer, question_type FROM {table_name}"
            cursor.execute(query)
            questions = []
            for row in cursor.fetchall():
                question_data = {
                    "id": row['id'],
                    "question": row['question'],
                    "options": [row['option1'], row['option2'], row['option3'], row['option4']],
                    "correct_answer": row['correct_answer'],
                    "question_type": row['question_type']
                }
                questions.append(question_data)
            cursor.close()
            logging.debug(f"[DB Debug] Executing SQL: {query}")
            logging.debug(f"[DB Debug] Number of rows fetched: {len(questions)}")
            logging.debug(f"[DB Debug] Processed questions: {questions}")
            return questions
        except Error as e:
            logging.error(f"Error fetching questions for language {language}: {e}")
            return []

    def get_question_at_index(self, language, index):
        """Get a single question at a specific index for a language.  Adjusted for direct index access."""
        try:
            questions = self.get_questions_by_language(language)
            if questions and 0 <= index < len(questions):
                return questions[index]
            return None
        except Exception as e:
            logging.error(f"Error getting question at index {index} for language {language}: {e}")
            return None

    def save_user_score(self, username, language, score, total_questions, timestamp):
        """Save the user's score for a quiz."""
        try:
            if not self.check_connection():
                self.connect()
            cursor = self.connection.cursor()
            query = "INSERT INTO quiz_history (user_name, language, score, total_questions, timestamp) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (username, language, score, total_questions, timestamp))
            self.connection.commit()
            cursor.close()
            logging.info(f"Score saved for {username} in {language}: {score}/{total_questions} at {timestamp}")
        except Error as e:
            logging.error(f"Error saving score: {e}")
            raise

    def fetch_all_questions(self, language):
        """Fetch all questions for a specific language from the database for admin view."""
        try:
            if not self.check_connection():
                self.connect()
            cursor = self.connection.cursor(dictionary=True)
            table_name = f"{self.table_prefix}{language}_questions"
            query = f"SELECT id, question, option1, option2, option3, option4, correct_answer FROM {table_name}"
            cursor.execute(query)
            questions = []
            for row in cursor.fetchall():
                question_data = {
                    "id": row['id'],
                    "question": row['question'],
                    "options": [row['option1'], row['option2'], row['option3'], row['option4']],
                    "correct_answer": row['correct_answer']
                }
                questions.append(question_data)
            cursor.close()
            logging.debug(f"[DB Debug] Executing SQL: {query}")
            logging.debug(f"[DB Debug] Number of rows fetched: {len(questions)}")
            logging.debug(f"[DB Debug] Processed questions: {questions}")
            return questions
        except Error as e:
            logging.error(f"Error fetching all questions for language {language}: {e}")
            return []

    def add_new_question(self, language, question_data):
        """Add a new question to the database, including question type."""
        try:
            if not self.check_connection():
                self.connect()
            cursor = self.connection.cursor()
            table_name = f"{self.table_prefix}{language}_questions"
            query = f"INSERT INTO {table_name} (question, option1, option2, option3, option4, correct_answer, question_type) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (
                question_data['question'],
                question_data['option1'],
                question_data['option2'],
                question_data['option3'],
                question_data['option4'],
                question_data['correct_answer'],
                question_data.get('question_type', 'multiple_choice') 
            ))
            self.connection.commit()
            cursor.close()
            logging.info(f"New question added to {language}_questions: {question_data}")
            return True
        except Error as e:
            logging.error(f"Error adding new question to {language}: {e}")
            return False

    def update_question(self, language, question_id, question_data):
        """Update an existing question in the database, including question type."""
        try:
            if not self.check_connection():
                self.connect()
            cursor = self.connection.cursor()
            table_name = f"{self.table_prefix}{language}_questions"
            query = f"UPDATE {table_name} SET question = %s, option1 = %s, option2 = %s, option3 = %s, option4 = %s, correct_answer = %s, question_type = %s WHERE id = %s"
            cursor.execute(query, (
                question_data['question'],
                question_data['option1'],
                question_data['option2'],
                question_data['option3'],
                question_data['option4'],
                question_data['correct_answer'],
                question_data.get('question_type', 'multiple_choice'), 
                question_id
            ))
            self.connection.commit()
            cursor.close()
            logging.info(f"Question {question_id} updated in {language}_questions: {question_data}")
            return True
        except Error as e:
            logging.error(f"Error updating question {question_id} in {language}: {e}")
            return False

    def delete_question(self, language, question_id):
        """Delete a question from the database."""
        try:
            if not self.check_connection():
                self.connect()
            cursor = self.connection.cursor()
            table_name = f"{self.table_prefix}{language}_questions"
            query = f"DELETE FROM {table_name} WHERE id = %s"
            cursor.execute(query, (question_id,))
            self.connection.commit()
            cursor.close()
            logging.info(f"Question {question_id} deleted from {language}_questions")
            return True
        except Error as e:
            logging.error(f"Error deleting question {question_id} from {language}: {e}")
            return False

    def get_high_scores(self, limit=10):
        """Fetches the top high scores from the database."""
        try:
            if not self.check_connection():
                self.connect()
            cursor = self.connection.cursor(dictionary=True)  
            query = """
                SELECT user_name, score, language
                FROM quiz_history
                ORDER BY score DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))  
            scores = cursor.fetchall()
            cursor.close()
            logging.info(f"Fetched top {limit} high scores.")
            return scores
        except Error as e:
            logging.error(f"Error fetching high scores: {e}")
            return []
