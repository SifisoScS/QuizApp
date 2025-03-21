# src/quiz_app.py
import streamlit as st
from src.utils.file_utils import load_questions_from_csv
from src.utils.quiz_logic import shuffle_questions, check_answer

def main():
    st.set_page_config(page_title="Awesome Quiz App", page_icon=":question:")

    # Initialize session state variables if they do not exist
    if 'index' not in st.session_state:
        st.session_state.index = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = []
    if 'question_order' not in st.session_state:
        st.session_state.question_order = []
        
    # Load questions

    questions = load_questions_from_csv("app/data/questions.csv")

    # Extract unique categories
    categories = list(set([q["category"] for q in questions]))
    categories.sort()  # Sort categories alphabetically

    # Add a category selector to the sidebar
    st.sidebar.title("Quiz Settings")
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = "All"  # Default category

    # Update selected category if user changes it
    new_selected_category = st.sidebar.selectbox("Choose a category", ["All"] + categories)
    if new_selected_category != st.session_state.selected_category:
        st.session_state.selected_category = new_selected_category
        # Reset quiz state when category changes
        st.session_state.score = 0
        st.session_state.index = 0
        st.session_state.answers = []
        st.session_state.question_order = []  # Reset question_order

    # Filter questions based on the selected category
    if st.session_state.selected_category == "All":
        filtered_questions = questions
    else:
        filtered_questions = [q for q in questions if q["category"] == st.session_state.selected_category]

    # Initialize question_order if not already set
    if 'question_order' not in st.session_state or not st.session_state.question_order:
        st.session_state.question_order = shuffle_questions(list(range(len(filtered_questions))))

    # Quiz logic
    def display_question():
        if st.session_state.index < len(filtered_questions):
            question_data = filtered_questions[st.session_state.question_order[st.session_state.index]]
            st.write(f"**Question {st.session_state.index + 1}:** {question_data['question']}")
            st.write(f"**Category:** {question_data['category']} | **Difficulty:** {question_data['difficulty']}")
            user_answer = st.radio("Choose your answer:", question_data['options'])

            if st.button("Submit"):
                is_correct = check_answer(user_answer, question_data['answer'])
                st.session_state.answers.append({
                    "question": question_data['question'],
                    "user_answer": user_answer,
                    "correct_answer": question_data['answer'],
                    "is_correct": is_correct,
                    "category": question_data['category'],
                    "difficulty": question_data['difficulty']
                })
                if is_correct:
                    st.session_state.score += 1
                    st.success("Correct! 🎉")
                else:
                    st.error(f"Wrong! The correct answer is {question_data['answer']} 😞")
                st.session_state.index += 1
                st.rerun()
        else:
            display_results()

    def display_results():
        st.write(f"Quiz Completed! Your score: {st.session_state.score}/{len(filtered_questions)}")
        st.write("### Detailed Results:")
        for i, answer in enumerate(st.session_state.answers):
            st.write(f"**Question {i + 1}:** {answer['question']}")
            st.write(f"**Category:** {answer['category']} | **Difficulty:** {answer['difficulty']}")
            st.write(f"Your Answer: {answer['user_answer']} - {'Correct' if answer['is_correct'] else 'Wrong'}")
            st.write(f"Correct Answer: {answer['correct_answer']}")
            st.write("---")
        if st.button("Restart"):
            st.session_state.score = 0
            st.session_state.index = 0
            st.session_state.answers = []
            st.session_state.question_order = shuffle_questions(list(range(len(filtered_questions))))
            st.rerun()

    st.title("The Ultimate Quiz App")
    display_question()
