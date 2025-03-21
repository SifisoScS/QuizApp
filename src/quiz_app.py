import streamlit as st

# Quiz data (questions and answers)
quiz_data = [
    {"question": "What is the capital of France?", "options": ["Paris", "London", "Rome", "Berlin"], "answer": "Paris"},
    {"question": "What is 5 + 7?", "options": ["10", "11", "12", "13"], "answer": "12"},
    {"question": "What is the chemical symbol for gold?", "options": ["Au", "Ag", "Fe", "Pb"], "answer": "Au"},
    {"question": "Which element has the atomic number 1?", "options": ["Oxygen", "Hydrogen", "Carbon", "Nitrogen"], "answer": "Hydrogen"},
    {"question": "What is the main ingredient in guacamole?", "options": ["Tomato", "Avocado", "Pepper", "Onion"], "answer": "Avocado"},
    {"question": "Who painted the Mona Lisa?", "options": ["Van Gogh", "Picasso", "Da Vinci", "Monet"], "answer": "Da Vinci"},
    {"question": "What is the smallest country in the world?", "options": ["Vatican City", "Monaco", "Nauru", "Malta"], "answer": "Vatican City"},
    {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Venus", "Jupiter"], "answer": "Mars"},
    {"question": "What is the hardest natural substance on Earth?", "options": ["Gold", "Iron", "Diamond", "Quartz"], "answer": "Diamond"},
    {"question": "In which year did the Titanic sink?", "options": ["1912", "1905", "1898", "1920"], "answer": "1912"},
    {"question": "What is the largest mammal in the world?", "options": ["Elephant", "Blue Whale", "Giraffe", "Great White Shark"], "answer": "Blue Whale"},
    {"question": "Who wrote 'Romeo and Juliet'?", "options": ["Shakespeare", "Hemingway", "Dickens", "Austen"], "answer": "Shakespeare"},
    {"question": "What is the largest planet in our solar system?", "options": ["Earth", "Jupiter", "Mars", "Saturn"], "answer": "Jupiter"},
]

# Session State for score, index tracking, and answers
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.index = 0
    st.session_state.answers = []  # To store user answers

# Display Question
def display_question():
    if st.session_state.index < len(quiz_data):
        question_data = quiz_data[st.session_state.index]
        st.write(f"**Question {st.session_state.index + 1}:** {question_data['question']}")
        user_answer = st.radio("Choose your answer:", question_data['options'])

        if st.button("Submit"):
            # Store the user's answer
            st.session_state.answers.append({
                "question": question_data['question'],
                "user_answer": user_answer,
                "correct_answer": question_data['answer'],
                "is_correct": user_answer == question_data['answer']
            })
            
            if user_answer == question_data['answer']:
                st.session_state.score += 1
                st.success("Correct!")
            else:
                st.error(f"Wrong! The correct answer is {question_data['answer']}")
            
            st.session_state.index += 1
            st.rerun()
    else:
        # Display detailed results
        st.write(f"Quiz Completed! Your score: {st.session_state.score}/{len(quiz_data)}")
        st.write("### Detailed Results:")
        for i, answer in enumerate(st.session_state.answers):
            st.write(f"**Question {i + 1}:** {answer['question']}")
            st.write(f"Your Answer: {answer['user_answer']} - {'Correct' if answer['is_correct'] else 'Wrong'}")
            st.write(f"Correct Answer: {answer['correct_answer']}")
            st.write("---")
        
        if st.button("Restart"):
            st.session_state.score = 0
            st.session_state.index = 0
            st.session_state.answers = []  # Reset answers
            st.rerun()

display_question()