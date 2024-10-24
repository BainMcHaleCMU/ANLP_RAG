import random

# Function to randomly select 20% of lines
def get_random_subset(file_path, percentage=0.2):
    with open(file_path, 'r', encoding='utf-8') as f:  # Specify encoding
        lines = f.readlines()

    # Total number of lines
    total_lines = len(lines)
    
    # Number of lines to select
    subset_size = int(total_lines * percentage)

    # Randomly sample line indices
    selected_indices = sorted(random.sample(range(total_lines), subset_size))
    
    # Get the subset of lines using selected indices
    subset = [lines[i].strip() for i in selected_indices]
    
    return subset, selected_indices

# Function to get corresponding answers for selected lines
def get_reference_answers(reference_file_path, selected_indices):
    with open(reference_file_path, 'r', encoding='utf-8') as f:  # Specify encoding
        answers = f.readlines()
    
    # Get the answers corresponding to the selected indices
    selected_answers = [answers[i].strip() for i in selected_indices]
    
    return selected_answers

# Paths to the input files
questions_file = 'questions.txt'
reference_answers_file = 'reference_answers.txt'
percent = .5

# Get a random subset of questions and corresponding indices
subset_questions, selected_indices = get_random_subset(questions_file, percentage=percent)

# Get the corresponding reference answers using the selected indices
subset_answers = get_reference_answers(reference_answers_file, selected_indices)

# Save the selected questions and corresponding answers
with open('sampled_questions.txt', 'w', encoding='utf-8') as q_out:  # Specify encoding
    q_out.write('\n'.join(subset_questions))

with open('sampled_reference_answers.txt', 'w', encoding='utf-8') as a_out:  # Specify encoding
    a_out.write('\n'.join(subset_answers))

# Display the selected indices and confirm the script ran successfully
print(f"Selected indices ({percent*100}%): {selected_indices}")
print(f"Subset of questions and answers saved to 'sampled_questions.txt' and 'sampled_reference_answers.txt'.")
