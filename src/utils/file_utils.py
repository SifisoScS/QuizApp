# src/utils/file_utils.py
import csv

def load_questions_from_csv(file_path):
    """Load questions from a CSV file."""
    questions = []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Split the options string into a list
            options = row["options"].split(",")
            # Strip any extra whitespace from options
            options = [option.strip() for option in options]
            # Append the question data
            questions.append({
                "question": row["question"],
                "options": options,
                "answer": row["answer"],
                "category": row["category"],
                "difficulty": row["difficulty"]
            })
    return questions