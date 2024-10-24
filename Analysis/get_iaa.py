from sklearn.metrics import f1_score
import numpy as np
import re

# Function to normalize text by removing articles and punctuation and lowercasing
def normalize_answer(s):
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)
    
    def remove_punctuation(text):
        return re.sub(r'[^\w\s]', '', text)
    
    def lowercase(text):
        return text.lower()
    
    return remove_articles(remove_punctuation(lowercase(s))).strip()


# Function to calculate F1 score for tokenized answers
def compute_f1_score_for_answers(answer1, answer2):
    # Tokenize the answers
    answer1 = normalize_answer(answer1)
    answer2 = normalize_answer(answer2)
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
with open('sampled_reference_answers.txt', 'r', encoding='utf-8') as f:
    answers1 = f.readlines()

with open('sampled_other_reference_answers.txt', 'r', encoding='utf-8') as f:
    answers2 = f.readlines()

with open('sampled_questions.txt', 'r', encoding='utf-8') as f:
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