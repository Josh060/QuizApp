from db_connection import get_questions_by_language

def get_javascript_questions():
    return get_questions_by_language("JavaScript")
