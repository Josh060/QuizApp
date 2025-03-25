from db_connection import get_questions_by_language
def get_cpp_questions():
    return get_questions_by_language("C++")
