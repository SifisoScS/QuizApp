# src/utils/quiz_logic.py
import random

def shuffle_questions(questions):
    """Shuffle the order of questions."""
    return random.sample(questions, len(questions))

def check_answer(user_answer, correct_answer):
    """Check if the user's answer is correct."""
    return user_answer == correct_answer