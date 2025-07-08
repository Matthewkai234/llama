from csv_qa_system import CSVQASystem

if __name__ == "__main__":
    csv_path = "data.csv"  # replace with your actual CSV path
    question = "question "

    qa_system = CSVQASystem()
    answer, score = qa_system.answer_question_from_csv(csv_path, question)

    print("Answer:", answer)
    print(score)
