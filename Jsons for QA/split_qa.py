import os
import random

# Function to read QA pairs from the text file
def read_qa_file(file_path):
    questions = []
    answers = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i in range(0, len(lines), 2):
        question = lines[i].strip()
        answer = lines[i + 1].strip()
        
        # Remove "Q: " prefix if present
        if question.startswith("Q: "):
            question = question[3:]
        
        # Remove "A: " prefix if present
        if answer.startswith("A: "):
            answer = answer[3:]
        
        questions.append(question)
        answers.append(answer)
    
    return questions, answers


# Function to perform the train/test split
def train_test_split(questions, answers, test_size=0.99):
    combined = list(zip(questions, answers))
    random.shuffle(combined)
    split_index = int(len(combined) * (1 - test_size))
    train_data = combined[:split_index]
    test_data = combined[split_index:]
    return train_data, test_data

# Function to write questions and answers to files in the correct format
def write_split_data(train_data, test_data, output_folder):
    os.makedirs(os.path.join(output_folder, 'train'), exist_ok=True)
    os.makedirs(os.path.join(output_folder, 'test'), exist_ok=True)
    
    # Write training data
    with open(os.path.join(output_folder, 'train', 'questions.txt'), 'w', encoding='utf-8') as q_train_file, \
         open(os.path.join(output_folder, 'train', 'reference_answers.txt'), 'w', encoding='utf-8') as a_train_file:
        for question, answer in train_data:
            q_train_file.write(question + "\n")
            a_train_file.write(answer + "\n")
    
    # Write test data
    with open(os.path.join(output_folder, 'test', 'questions.txt'), 'w', encoding='utf-8') as q_test_file, \
         open(os.path.join(output_folder, 'test', 'reference_answers.txt'), 'w', encoding='utf-8') as a_test_file:
        for question, answer in test_data:
            q_test_file.write(question + "\n")
            a_test_file.write(answer + "\n")

# Main script
def process_qa_split(input_file, output_folder, test_size=0.2):
    # Step 1: Read the QA data from qa.txt
    questions, answers = read_qa_file(input_file)
    
    # Step 2: Perform a train/test split
    train_data, test_data = train_test_split(questions, answers, test_size)
    
    # Step 3: Write the split data into the corresponding directories
    write_split_data(train_data, test_data, output_folder)

# Usage
input_file = 'Jsons for QA/qa.txt'  # Path to your qa.txt file
output_folder = 'data'  # Path to the output data directory
process_qa_split(input_file, output_folder, test_size=0.2)

print("Train/Test split completed!")
