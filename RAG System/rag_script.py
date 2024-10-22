def get_answer(question):
    # Simulating a RAG system query
    top_chunks = retrieve_top_k(question, k=3)
    prompt = create_prompt(template, question, top_chunks)
    return READER_LLM(prompt)


def generate_answers(input_file, output_file):

    with open(input_file, 'r') as file:
        questions = file.readlines()

    answers = []
    for index, question in enumerate(questions):
        question = question.strip()
        if question:
            answer = get_answer(question)
            answers.append(f'Question {index + 1}: {answer}')

    with open(output_file, 'w') as file:
        for answer in answers:
            file.write(answer + '\n')
            print(answer)  # Print each answer as it's generated

# Usage example:
generate_answers("data/test/questions.txt", "model_answers.txt")