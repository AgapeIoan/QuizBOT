import json

def write_to_json(question, answers, correct_answer):
    with open('questions.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
    
    db["questions"].append(question)
    db["answers"].append(answers)
    db["correct_answers"].append(correct_answer)

    with open('questions.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=4)

def input_from_keyboard():
    question = ""
    answers = []
    correct_answers = []

    print("Enter question:")
    while True:
        line = input()
        if line == "":
            break
        question += line + "\n"

    answers_number = int(input("Enter number of answers: "))

    print("Enter answers:")
    for i in range(answers_number):
        print("Answer {}:".format(i + 1))
        answer = ""
        while True:
            line = input()
            if line == "":
                break
            answer += line + "\n"
        answers.append(answer)

    print(f"Enter the correct answers:")
    while True:
        line = input()
        if line == "":
            break
        try:
            correct_answers.append(int(line))
        except ValueError:
            correct_answers.append(line)

    return question, answers, correct_answers

if __name__ == '__main__':
    while True:
        print("Want to input a question? (y/n)")
        if input() == "y":
            question, answers, correct_answer = input_from_keyboard()
            print("Saving to JSON...")
            write_to_json(question, answers, correct_answer)
            print("Done.")
        elif input() == "n":
            # end the program
            print("Exiting...")
            break
        else:
            print("Invalid input.")
            continue
