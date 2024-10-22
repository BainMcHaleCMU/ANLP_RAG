import re
from collections import Counter
from sklearn.metrics import f1_score

# Function to normalize text by removing articles and punctuation and lowercasing
def normalize_answer(s):
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)
    
    def remove_punctuation(text):
        return re.sub(r'[^\w\s]', '', text)
    
    def lowercase(text):
        return text.lower()
    
    return remove_articles(remove_punctuation(lowercase(s))).strip()

# Function to compute Exact Match (EM)
def exact_match_score(prediction, ground_truth):
    return int(normalize_answer(prediction) == normalize_answer(ground_truth))

# Function to compute F1 Score
def f1_score_single(prediction, ground_truth):
    prediction_tokens = normalize_answer(prediction).split()
    ground_truth_tokens = normalize_answer(ground_truth).split()
    
    common_tokens = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common_tokens.values())
    
    if num_same == 0:
        return 0
    
    precision = num_same / len(prediction_tokens)
    recall = num_same / len(ground_truth_tokens)
    f1 = 2 * (precision * recall) / (precision + recall)
    
    return f1

# Function to compute recall
def recall_score_single(prediction, ground_truth):
    prediction_tokens = normalize_answer(prediction).split()
    ground_truth_tokens = normalize_answer(ground_truth).split()
    
    common_tokens = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common_tokens.values())
    
    if len(ground_truth_tokens) == 0:
        return 0
    recall = num_same / len(ground_truth_tokens)
    return recall

# Reading the reference and generated answers
with open('reference_answers.txt', 'r') as f:
    reference_answers = f.readlines()

with open('generated_answers.txt', 'r') as f:
    generated_answers = f.readlines()

# Ensure the files have the same number of answers
assert len(reference_answers) == len(generated_answers), "Mismatch in number of answers."

# Evaluation metrics
total_em = 0
total_f1 = 0
total_recall = 0

# Iterate over all answers and compute metrics
for ref_answer, gen_answer in zip(reference_answers, generated_answers):
    em = exact_match_score(gen_answer.strip(), ref_answer.strip())
    f1 = f1_score_single(gen_answer.strip(), ref_answer.strip())
    recall = recall_score_single(gen_answer.strip(), ref_answer.strip())
    
    total_em += em
    total_f1 += f1
    total_recall += recall

# Average the metrics over all the questions
num_questions = len(reference_answers)
average_em = total_em / num_questions
average_f1 = total_f1 / num_questions
average_recall = total_recall / num_questions

# Display the results
print(f"Exact Match: {average_em * 100:.2f}%")
print(f"F1 Score: {average_f1 * 100:.2f}%")
print(f"Recall: {average_recall * 100:.2f}%")
