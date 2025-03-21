import streamlit as st
import random
import json
import csv
import os

# --- Theme Customization ---
st.set_page_config(page_title="Awesome Quiz App", page_icon=":question:")

# --- Load CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# --- Get script directory ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Load quiz data from CSV file ---
def load_quiz_data(filename="questions.csv"):
    """Loads quiz questions from a CSV file."""
    quiz_data = []
    try:
        filepath = os.path.join(SCRIPT_DIR, filename)  # Construct full path
        with open(filepath, 'r', encoding='utf-8') as csvfile:  # Encoding for special characters
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                # Split the options string into a list
                options = [option.strip() for option in row['options'].split(',')]
                quiz_data.append({
                    "question": row['question'],
                    "options": options,
                    "answer": row['answer'],
                    "category": row['category'],
                    "difficulty": row['difficulty']
                })
    except FileNotFoundError:
        st.error(f"Error: {filename} not found.  Make sure the file exists in the correct directory.")
    except Exception as e:
        st.error(f"An error occurred while loading quiz data: {e}")
    return quiz_data

quiz_data = load_quiz_data()  # Load the quiz data

# --- Get unique categories from quiz data ---
all_categories = sorted({q['category'] for q in quiz_data})  # Use set comprehension

def update_question_order():
    """Updates the question order based on selected categories."""
    filtered_questions = [q for q in quiz_data if q['category'] == st.session_state.selected_category]
    st.session_state.question_order = list(range(len(filtered_questions)))
    random.shuffle(st.session_state.question_order)

# --- Session State Initialization ---
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.index = 0
    st.session_state.answers = []
    st.session_state.question_order = []
    st.session_state.selected_category = all_categories[0]  # Initialize with the first category

    update_question_order()

    if not st.session_state.question_order:  # Handle case where no questions match selected categories
        st.warning("No questions match the selected categories. Please select at least one category.")

# --- Quiz Logic Functions ---
def reset_quiz_state():
    """Resets the quiz state to start over."""
    st.session_state.score = 0
    st.session_state.index = 0
    st.session_state.answers = []
    update_question_order()

def get_current_question():
    """Gets the current question data based on the shuffled order and selected categories."""
    filtered_questions = [q for q in quiz_data if q['category'] == st.session_state.selected_category]

    if not filtered_questions:
        return None  # No questions match selected categories

    if st.session_state.index >= len(filtered_questions):
        return None

    if not st.session_state.question_order:
        return None

    question_index = st.session_state.question_order[st.session_state.index]
    try:
        return filtered_questions[question_index]
    except IndexError as e:
        st.error(f"IndexError: {e}. Check question_order and filtered_questions.")
        return None
    except TypeError as e:
        st.error(f"TypeError: {e}. Check the structure of questions")
        return None

def display_results():
    """Displays the final score and detailed results."""
    filtered_questions = [q for q in quiz_data if q['category'] == st.session_state.selected_category]  # filters the selected quiz to find what quiz matches
    st.write(f"Quiz Completed! Your score: {st.session_state.score}/{len(filtered_questions)}")  # dynamically adjusts the final score
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

    if (current_question_data := get_current_question()) is not None:  # checks whether the object is none
        try:
            st.write(f"**Question {st.session_state.index + 1}:** {current_question_data['question']}")

            with st.form(key=f"question_form_{st.session_state.index}"):
                user_answer = st.radio("Choose your answer:", current_question_data['options'], key=f"radio_{st.session_state.index}")
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
                st.rerun()
        except KeyError as e:
            st.error(f"KeyError: {e} in current_question_data. Check your quiz_data structure.")
            st.stop()
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            st.stop()

    else:
        display_results()

# --- Main App Flow ---
st.title("The Ultimate Quiz App")

# --- Category Selection ---
st.sidebar.header("Category Selection")
selected_category = st.sidebar.selectbox("Choose a category:", all_categories, key="selected_category_selectbox")

# Check if selected_category has changed
if selected_category != st.session_state.selected_category:
    st.session_state.selected_category = selected_category
    st.session_state.index = 0  # Reset the index to start from the beginning
    st.session_state.score = 0  # reset score
    st.session_state.answers = []  # clearing answers
    update_question_order()
    st.rerun()

progress_bar = st.progress(st.session_state.index / len(quiz_data) if len(quiz_data) > 0 else 0)

display_question()