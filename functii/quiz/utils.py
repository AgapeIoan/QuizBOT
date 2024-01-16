import random
import json
import datetime
import disnake
import itertools
import random

from functii.debug import print_debug, print_log

with open("storage/quiz/questions.json", "r", encoding='utf-8') as f:
    QUESTIONS_DB = json.load(f)

def ranges(i):
    for a, b in itertools.groupby(enumerate(i), lambda pair: pair[1] - pair[0]):
        b = list(b)
        yield b[0][1], b[-1][1]

def shuffle_answers(answers: list, correct_answers: list):
    if not answers: # modal
        return answers, correct_answers
    elif correct_answers == [0]: # no answer
        return random.shuffle(answers), correct_answers

    answers_dict = {}
    for ans, index in zip(answers, range(1, 100)):
        if index in correct_answers:
            answers_dict[ans] = index
        else:
            answers_dict[ans] = 0

    random.shuffle(answers)

    new_correct_answers = []
    for ans, index in zip(answers, range(1, 100)):
        if answers_dict[ans] != 0:
            new_correct_answers.append(index)

    return answers, new_correct_answers

def set_buttons_red_and_green(self, buttons_number: int, greens = []):
    answer_buttons = get_answer_buttons(self, buttons_number)
    for green in greens:
        answer_buttons[green-1].style = disnake.ButtonStyle.green
    for i in answer_buttons: # Primele 2 butoane sunt pentru Send si Next
        i.disabled = True
        if i.style != disnake.ButtonStyle.green:
            i.style = disnake.ButtonStyle.red
    
    return self

def disable_answer_buttons(self):
    for i in get_answer_buttons(self, self.buttons_number):
        i.disabled = True
        i.style = disnake.ButtonStyle.gray
    return self

def reset_buttons(self):
    if self.buttons_number > 0:
        for i in get_answer_buttons(self, self.buttons_number):
            i.disabled = False
            i.style = disnake.ButtonStyle.gray

    send_button = find_button_by_custom_id(self, "send")
    next_button = find_button_by_custom_id(self, "next")
    send_button.disabled = False
    send_button.style = disnake.ButtonStyle.green
    
    next_button.disabled = True
    next_button.style = disnake.ButtonStyle.gray

    return self

def remove_answer_buttons(self):
    answer_buttons = get_answer_buttons(self, self.buttons_number)
    if answer_buttons:    
        for i in answer_buttons:
            self.remove_item(i)
    return self

def create_embed(inter, image_url = ""):
    if inter.correct_answers == [0]:
        title = f"❗ Intrebarea #{inter.current_question_number} [FARA RASPUNS GASIT] ❗"
        inter.question = "❗ " + inter.question + "\n"
    else:
        title = f"Intrebarea #{inter.current_question_number}"
        inter.question = inter.question + "\n"

    if inter.question.startswith("https://"):
        image_url = inter.question.split("\n")[0]
        inter.question = "\n".join(inter.question.split("\n")[1:])

    embed = disnake.Embed(
        title=title,
        description=inter.question + '\n',
        color=0xffd700,
        timestamp=datetime.datetime.utcnow()
    )
    try:
        icon_url = inter.author.avatar.url
    except AttributeError:
        icon_url = ""
    embed.set_footer(text="Requested by " + str(inter.author), icon_url=icon_url)
    # embed.add_field(name="Raspuns 1", value=inter.answers[0], inline=False)
    for ans_index in range(len(inter.answers)):
        embed.add_field(name=f"Raspuns {ans_index + 1}", value=inter.answers[ans_index], inline=False)
    
    embed.set_image(image_url)
    return embed

def create_message(inter, numar_intrebare = None):
    if not numar_intrebare or numar_intrebare > len(QUESTIONS_DB["questions"]) or numar_intrebare < 1:
        # Invalid input. Get a random question.
        print_debug("Invalid input. Getting a random question.")
        numar_intrebare = random.randint(0, len(QUESTIONS_DB["questions"]) - 1) + 1
    
    inter.current_question_number = numar_intrebare
    inter.question = QUESTIONS_DB["questions"][numar_intrebare - 1]
    inter.answers = QUESTIONS_DB["answers"][numar_intrebare - 1].copy()
    inter.correct_answers = QUESTIONS_DB["correct_answers"][numar_intrebare - 1].copy()

    inter.answers, inter.correct_answers = shuffle_answers(inter.answers, inter.correct_answers)

    print_debug("Current question number: " + str(inter.current_question_number))

    inter.embed = create_embed(inter)

    return inter

def find_button_by_custom_id(self, custom_id):
    for i in self.children:
        if i.custom_id == custom_id:
            return i
    return None

def get_answer_buttons(self, buttons_number: int):
    answer_buttons = []
    first_answer_button = find_button_by_custom_id(self, "1")
    if not first_answer_button:
        return answer_buttons
        
    first_answer_button_index = self.children.index(first_answer_button)

    for i in range(first_answer_button_index, first_answer_button_index + buttons_number):
        answer_buttons.append(self.children[i])
    
    return answer_buttons

if __name__ == "__main__":
    pass
