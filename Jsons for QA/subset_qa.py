# Python script to filter questions based on keywords and write corresponding answers with UTF-8 encoding

def filter_date_questions():
    # Open input files and output files with UTF-8 encoding
    with open(r"C:\Users\jbber\.vscode\ANLP_RAG\data\test\questions.txt", "r", encoding="utf-8") as q_file, open(r"C:\Users\jbber\.vscode\ANLP_RAG\data\test\reference_answers.txt", "r", encoding="utf-8") as a_file:
        questions = q_file.readlines()
        answers = a_file.readlines()

    # Ensure the files have the same number of lines
    if len(questions) != len(answers):
        print("Error: questions.txt and reference_answers.txt have different number of lines.")
        return

    # Prepare output files
    with open("date_questions.txt", "w", encoding="utf-8") as dq_file, open("date_answers.txt", "w", encoding="utf-8") as da_file:
        # Filter questions that start with "What date" or "When"
        for question, answer in zip(questions, answers):
            if question.strip().lower().startswith(("what date", "when")):
                dq_file.write(question)
                da_file.write(answer)

    print("Filtered questions and answers have been written to date_questions.txt and date_answers.txt")

# Run the function
filter_date_questions()
