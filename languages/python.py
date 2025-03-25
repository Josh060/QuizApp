from db_connection import get_questions_by_language
def get_python_questions():
    return get_questions_by_language("Python")
