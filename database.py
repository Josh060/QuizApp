import mysql.connector
from mysql.connector import Error
from datetime import datetime

class Database:
    def __init__(self, host="localhost", user="root", password="", database="quiz_db"):
        self.connection = None
        self.cursor = None
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.connection.is_connected():
                print(f"Connected to MySQL database: {database}@{host}")
                self.cursor = self.connection.cursor()
            else:
                print("Failed to connect to the database.")
        except Error as err:
            print(f"Error: {err}")
            self.connection = None
            self.cursor = None

    def close(self):
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection closed.")
        else:
            print("Connection was not open.")

    def check_connection(self):
        """Check if the database connection is still open."""
        if self.connection and self.connection.is_connected():
            return True
        print("Database is not connected.")
        return False

    def get_questions_by_language(self, language):
        """Retrieve all questions for a specific language."""
        if not self.check_connection():
            print("Error: No database connection.")
            return []

        try:
            table_name = f"{language.lower()}_questions"
            sql = f"SELECT id, question, option1, option2, option3, option4, answer FROM {table_name}"
            print(f"[DB Debug] Executing SQL: {sql}")
            self.cursor.execute(sql)
            questions = self.cursor.fetchall()
            print(f"[DB Debug] Number of rows fetched: {len(questions)}")

            processed_questions = []
            for q in questions:
                processed_questions.append({
                    "id": q[0],
                    "question": q[1],
                    "options": [q[2], q[3], q[4], q[5]],
                    "correct_answer": q[6]
                })

            print(f"[DB Debug] Processed questions: {processed_questions}")
            return processed_questions
        except Error as err:
            print(f"Error getting questions for {language}: {err}")
            return []

    def save_user_score(self, username, language, score, total_questions, timestamp):
        """Save the user's score to the database."""
        if not self.check_connection():
            print("Error: No database connection.")
            return None

        try:
            sql = """
            INSERT INTO scores (username, language, score, total_questions, submitted_at)
            VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(sql, (username, language, score, total_questions, timestamp))
            self.connection.commit()
            print(f"Score saved for {username} in {language}: {score}/{total_questions} at {timestamp}")
            return self.cursor.lastrowid
        except Error as err:
            print(f"Error saving score: {err}")
            return None

    def get_top_scores(self, language, limit=5, with_time=False):
        """Retrieve the top scores for a given language, optionally with timestamps."""
        if not self.check_connection():
            print("Error: No database connection.")
            return []

        order_by = "score DESC"
        if with_time:
            order_by += ", submitted_at ASC"

        try:
            sql = f"""
                SELECT username, score, total_questions, submitted_at
                FROM scores
                WHERE language = %s
                ORDER BY {order_by}
                LIMIT %s
            """
            self.cursor.execute(sql, (language, limit))
            scores = self.cursor.fetchall()
            return scores
        except Error as err:
            print(f"Error getting scores for {language}: {err}")
            return []

    def get_all_scores(self, language=None):
        """Retrieve all scores, optionally filtered by language."""
        if not self.check_connection():
            print("Error: No database connection.")
            return []

        try:
            if language:
                sql = "SELECT username, score, total_questions, submitted_at, language FROM scores WHERE language = %s"
                self.cursor.execute(sql, (language,))
            else:
                sql = "SELECT username, score, total_questions, submitted_at, language FROM scores"
                self.cursor.execute(sql)

            scores = self.cursor.fetchall()
            print(f"Fetched raw scores: {scores}")

            formatted_scores = []
            for s in scores:
                try:
                    timestamp_value = s[3]

                    if isinstance(timestamp_value, datetime):
                        formatted_timestamp = timestamp_value.strftime('%Y-%m-%d %H:%M:%S')
                    elif isinstance(timestamp_value, str):
                        try:
                            formatted_timestamp = datetime.fromisoformat(timestamp_value).strftime('%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            formatted_timestamp = "Invalid time"
                    elif isinstance(timestamp_value, float):
                        formatted_timestamp = datetime.utcfromtimestamp(timestamp_value).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        formatted_timestamp = "Invalid time"

                    formatted_scores.append((
                        s[0],  # username
                        s[1],  # score
                        s[2],  # total_questions
                        formatted_timestamp,
                        s[4]   # language
                    ))
                except Exception as e:
                    print(f"Error formatting timestamp: {e}")
                    continue

            return formatted_scores

        except Error as err:
            print(f"Error getting scores: {err}")
            return []

    def edit_question(self, question_id, language, question, options, correct_answer):
        """Edit an existing question in the database."""
        if not self.check_connection():
            print("Error: No database connection.")
            return 0

        try:
            table_name = f"{language.lower()}_questions"
            sql = f"""
                UPDATE {table_name}
                SET question = %s, option1 = %s, option2 = %s, option3 = %s, option4 = %s, answer = %s
                WHERE id = %s
            """
            self.cursor.execute(sql, (question, options[0], options[1], options[2], options[3], correct_answer, question_id))
            self.connection.commit()
            print(f"Question ID {question_id} updated in {table_name}.")
            return self.cursor.rowcount
        except Error as err:
            print(f"Error updating question: {err}")
            return 0

    def delete_question(self, question_id, language):
        """Delete a question from the database."""
        if not self.check_connection():
            print("Error: No database connection.")
            return 0

        try:
            table_name = f"{language.lower()}_questions"
            sql = f"DELETE FROM {table_name} WHERE id = %s"
            self.cursor.execute(sql, (question_id,))
            self.connection.commit()
            print(f"Question ID {question_id} deleted from {table_name}.")
            return self.cursor.rowcount
        except Error as err:
            print(f"Error deleting question: {err}")
            return 0
