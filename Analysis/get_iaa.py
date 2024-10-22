from sklearn.metrics import f1_score
import numpy as np

# Function to calculate F1 score for tokenized answers
def compute_f1_score_for_answers(answer1, answer2):
    # Tokenize the answers
    answer1_tokens = answer1.split()
    answer2_tokens = answer2.split()
    
    # Get the set of unique tokens
    all_tokens = set(answer1_tokens).union(set(answer2_tokens))
    
    # Create binary vectors for presence/absence of tokens in each answer
    vector1 = [1 if token in answer1_tokens else 0 for token in all_tokens]
    vector2 = [1 if token in answer2_tokens else 0 for token in all_tokens]
    
    # Compute F1 score (average='binary' ensures that it treats them as binary labels)
    return f1_score(vector1, vector2)

# Reading answers from files
with open('answer1.txt', 'r') as f:
    answers1 = f.readlines()

with open('answer2.txt', 'r') as f:
    answers2 = f.readlines()

with open('sampled_questions.txt', 'r') as f:
    questions = f.readlines()

# Compute F1 score for each pair of answers
f1_scores = []
for ans1, ans2 in zip(answers1, answers2):
    f1 = compute_f1_score_for_answers(ans1.strip(), ans2.strip())
    f1_scores.append(f1)

# Compute the average F1 score across all questions
average_f1 = np.mean(f1_scores)

# Display the average F1 score
print(f'Average F1 Score: {average_f1:.4f}')