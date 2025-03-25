import mysql.connector

def get_questions_by_language(language):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='quiz_db'
        )
        cursor = conn.cursor()
        query = """SELECT question, option1, option2, option3, option4, answer 
                   FROM it_questions WHERE language = %s ORDER BY RAND() LIMIT 5"""
        cursor.execute(query, (language,))
        questions = cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        questions = []
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()
    return questions
