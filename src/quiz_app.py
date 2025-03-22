# src/quiz_app.py
import streamlit as st
from src.utils.file_utils import load_questions_from_csv
from src.utils.quiz_logic import shuffle_questions, check_answer
from src.utils.leaderboard_utils import load_leaderboard, update_leaderboard

# Custom CSS for three-column layout
st.markdown(
    """
    <style>
    .main {
        display: flex;
        justify-content: space-between;
    }
    .quiz {
        flex: 2;
        padding: 0 20px;
    }
    .leaderboard {
        flex: 1;
        padding: 0 20px;
        border-left: 1px solid #ccc;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def main():
    st.set_page_config(page_title="Awesome Quiz App", page_icon=":question:", layout="wide")

    # Initialize session state variables if they do not exist
    if 'index' not in st.session_state:
        st.session_state.index = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = []
    if 'question_order' not in st.session_state:
        st.session_state.question_order = []
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = "All"  # Default category
    if 'selected_difficulty' not in st.session_state:
        st.session_state.selected_difficulty = "All"  # Default difficulty

    # Load questions
    questions = load_questions_from_csv("app/data/questions.csv")

    # Extract unique categories and difficulty levels
    categories = sorted({q["category"] for q in questions})
    difficulty_levels = sorted({q["difficulty"] for q in questions})

    # Add a category and difficulty selector to the left sidebar
    st.sidebar.title("Quiz Settings")
    new_selected_category = st.sidebar.selectbox("Choose a category", ["All"] + categories)
    new_selected_difficulty = st.sidebar.selectbox("Choose a difficulty level", ["All"] + difficulty_levels)

    # Reset quiz state if category or difficulty changes
    if (new_selected_category != st.session_state.selected_category or
        new_selected_difficulty != st.session_state.selected_difficulty):
        st.session_state.selected_category = new_selected_category
        st.session_state.selected_difficulty = new_selected_difficulty
        st.session_state.score = 0
        st.session_state.index = 0
        st.session_state.answers = []
        st.session_state.question_order = []  # Reset question_order

    # Filter questions based on the selected category and difficulty
    filtered_questions = questions
    if st.session_state.selected_category != "All":
        filtered_questions = [q for q in filtered_questions if q["category"] == st.session_state.selected_category]
    if st.session_state.selected_difficulty != "All":
        filtered_questions = [q for q in filtered_questions if q["difficulty"] == st.session_state.selected_difficulty]

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

        # Update the leaderboard
        if st.session_state.score > 0:
            name = st.text_input("Enter your name to save your score:")
            if st.button("Save Score"):
                if name:
                    update_leaderboard(name, st.session_state.score)
                    st.success("Score saved! 🎉")
                else:
                    st.error("Please enter your name.")

        if st.button("Restart"):
            st.session_state.score = 0
            st.session_state.index = 0
            st.session_state.answers = []
            st.session_state.question_order = shuffle_questions(list(range(len(filtered_questions))))
            st.rerun()

    # Main layout
    st.title("The Ultimate Quiz App")

    # Create columns for the center (quiz) and right (leaderboard)
    col1, col2 = st.columns([2, 1])  # Center column is twice as wide as the right column

    # Display the quiz in the center column
    with col1:
        display_question()

    # Display the leaderboard in the right column
    with col2:
        st.write("### Leaderboard")
        leaderboard = load_leaderboard()
        if leaderboard:
            for i, entry in enumerate(leaderboard):
                st.write(f"{i + 1}. {entry['name']} - {entry['score']} points")
        else:
            st.write("No scores yet. Be the first to play!")