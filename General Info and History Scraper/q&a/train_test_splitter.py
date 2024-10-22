import random

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def write_file(file_path, data):
    with open(file_path, 'w') as file:
        file.writelines(data)

def split_data(questions_file, answers_file, train_questions_file, train_answers_file, test_questions_file, test_answers_file, split_ratio=0.8):
    # Read questions and answers
    questions = read_file(questions_file)
    answers = read_file(answers_file)

    # Ensure both files have the same number of lines
    assert len(questions) == len(answers), "Questions and answers files must have the same number of lines."

    # Pair questions with their corresponding answers
    paired_data = list(zip(questions, answers))

    # Shuffle the data
    random.shuffle(paired_data)

    # Calculate the split index
    split_index = int(len(paired_data) * split_ratio)

    # Split into training and testing sets
    train_data = paired_data[:split_index]
    test_data = paired_data[split_index:]

    # Separate questions and answers for train and test sets
    train_questions, train_answers = zip(*train_data)
    test_questions, test_answers = zip(*test_data)

    # Write to respective files
    write_file(train_questions_file, train_questions)
    write_file(train_answers_file, train_answers)
    write_file(test_questions_file, test_questions)
    write_file(test_answers_file, test_answers)

# Example usage:
split_data(
    'questions.txt',
    'reference_answers.txt',
    'train_questions.txt',
    'train_answers.txt',
    'test_questions.txt',
    'test_answers.txt'
)