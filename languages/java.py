from db_connection import get_questions_by_language
def get_java_questions():
    return get_questions_by_language("Java")
