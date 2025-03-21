# app/tests/test_quiz_logic.py
from src.utils.quiz_logic import shuffle_questions, check_answer

def test_shuffle_questions():
    questions = [{"question": "Q1"}, {"question": "Q2"}]
    shuffled = shuffle_questions(questions)
    assert len(shuffled) == len(questions)
    assert set(shuffled) == set(questions)

def test_check_answer():
    assert check_answer("Paris", "Paris") == True
    assert check_answer("Paris", "London") == False