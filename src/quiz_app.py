import streamlit as st
import random
import json

# --- Theme Customization ---
st.set_page_config(page_title="Awesome Quiz App", page_icon=":question:")

# --- Load CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# --- Load quiz data from a JSON file ---
try:
    with open("quiz_data.json", "r") as f:
        quiz_data = json.load(f)
except FileNotFoundError:
    quiz_data = [  # Default quiz data if JSON is missing
        {"question": "What is the capital of France?", "options": ["Paris", "London", "Rome", "Berlin"], "answer": "Paris"},
        {"question": "What is 5 + 7?", "options": ["10", "11", "12", "13"], "answer": "12"},
        {"question": "What is the chemical symbol for gold?", "options": ["Au", "Ag", "Fe", "Pb"], "answer": "Au"},
        {"question": "What is the largest ocean on Earth?", "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"], "answer": "Pacific Ocean"},
        {"question": "Who wrote 'Pride and Prejudice'?", "options": ["Jane Austen", "Charlotte Brontë", "Mark Twain", "Charles Dickens"], "answer": "Jane Austen"},
        {"question": "What is the powerhouse of the cell?", "options": ["Nucleus", "Mitochondria", "Ribosome", "Endoplasmic Reticulum"], "answer": "Mitochondria"},
        {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Venus", "Jupiter"], "answer": "Mars"},
        {"question": "What is the largest mammal in the world?", "options": ["Elephant", "Blue Whale", "Giraffe", "Great White Shark"], "answer": "Blue Whale"},
        {"question": "In which year did the Titanic sink?", "options": ["1912", "1905", "1898", "1920"], "answer": "1912"},
        {"question": "What is the smallest country in the world?", "options": ["Vatican City", "Monaco", "Nauru", "Malta"], "answer": "Vatican City"},
    ] # load default values
except json.JSONDecodeError:
    st.error("Error decoding quiz_data.json.  Please check the file format.")
    quiz_data = []

# --- Session State Initialization ---
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.index = 0
    st.session_state.answers = []
    st.session_state.question_order = list(range(len(quiz_data)))
    random.shuffle(st.session_state.question_order)


# --- Quiz Logic Functions ---

def reset_quiz_state():
    """Resets the quiz state to start over."""
    st.session_state.score = 0
    st.session_state.index = 0
    st.session_state.answers = []
    st.session_state.question_order = list(range(len(quiz_data)))
    random.shuffle(st.session_state.question_order)


def get_current_question():
    """Gets the current question data based on the shuffled order."""
    print(f"Debug: st.session_state.index = {st.session_state.index}")  # Debug print
    print(f"Debug: len(quiz_data) = {len(quiz_data)}")  # Debug print
    if st.session_state.index >= len(quiz_data):
        return None

    question_index = st.session_state.question_order[st.session_state.index]
    print(f"Debug: question_index = {question_index}")  # Debug print
    try:
        question = quiz_data[question_index]
        print(f"Debug: question = {question}")
        return question
    except IndexError as e:
        st.error(f"IndexError: {e}.  question_index is out of range.  Check question_order and quiz_data.")
        return None  # Return None to avoid further errors
    except TypeError as e:
        st.error(f"TypeError: {e}. quiz_data or question_order might not be in the correct format.")
        return None


def display_results():
    """Displays the final score and detailed results."""
    st.write(f"Quiz Completed! Your score: {st.session_state.score}/{len(quiz_data)}")
    st.write("### Detailed Results:")
    for i in range(len(st.session_state.answers)):  # Iterate through answers
        answer = st.session_state.answers[i]
        st.write(f"**Question {i + 1}:** {answer['question']}")
        st.write(f"Your Answer: {answer['user_answer']} - {'Correct' if answer['is_correct'] else 'Wrong'}")
        st.write(f"Correct Answer: {answer['correct_answer']}")
        st.write("---")

    if st.button("Restart"):
        reset_quiz_state()
        st.rerun()

def display_question():
    """Displays the current question and handles user input."""
    current_question_data = get_current_question()

    if current_question_data is not None:  # Explicit check for None
        try: # error handling for the different questions
            st.write(f"**Question {st.session_state.index + 1}:** {current_question_data['question']}")

            with st.form(key=f"question_form_{st.session_state.index}"):
                user_answer = st.radio("Choose your answer:", current_question_data['options'], key=f"radio_{st.session_state.index}")  # Unique key
                submit_button = st.form_submit_button("Submit")

            if submit_button:
                is_correct = user_answer == current_question_data['answer']

                st.session_state.answers.append({
                    "question": current_question_data['question'],
                    "user_answer": user_answer,
                    "correct_answer": current_question_data['answer'],
                    "is_correct": is_correct
                })

                if is_correct:
                    st.session_state.score += 1
                    st.success("Correct! 🎉")
                else:
                    st.error(f"Wrong! The correct answer is {current_question_data['answer']} 😞")

                st.session_state.index += 1
                st.rerun()  # Force re-execution
        except KeyError as e:
            st.error(f"KeyError: {e} in current_question_data. Check your quiz_data structure.")
            st.stop()  # Stop execution to prevent further errors
        except Exception as e: # Generic error for any other potential issues
            st.error(f"An unexpected error occurred: {e}")
            st.stop()

    else:
        display_results()

# --- Main App Flow ---
st.title("The Ultimate Quiz App")
progress_bar = st.progress(st.session_state.index / len(quiz_data) if len(quiz_data) > 0 else 0)

display_question()