import random
import json
import datetime
import disnake
import itertools

from functii.debug import print_debug, print_log

with open("storage/quiz/questions.json", "r", encoding='utf-8') as f:
    QUESTIONS_DB = json.load(f)

def ranges(i):
    for a, b in itertools.groupby(enumerate(i), lambda pair: pair[1] - pair[0]):
        b = list(b)
        yield b[0][1], b[-1][1]

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

def create_embed(inter):
    if inter.correct_answers == [0]:
        title = f"❗ Intrebarea #{inter.current_question_number} [FARA RASPUNS GASIT] ❗"
        inter.question = "❗ " + inter.question + "\n"
    else:
        title = f"Intrebarea #{inter.current_question_number}"
        inter.question = inter.question + "\n"

    embed = disnake.Embed(
        title=title,
        description=inter.question + '\n',
        color=0xffd700,
        timestamp=datetime.datetime.utcnow()
    )
    try:
        icon_url = inter.author.avatar.url
    except AttributeError:
        icon_url = "https://cdn.discordapp.com/avatars/1054834099489079379/756ff7fe4f84636087e0816c67893878.webp"
    embed.set_footer(text="Requested by " + str(inter.author), icon_url=icon_url)
    # embed.add_field(name="Raspuns 1", value=inter.answers[0], inline=False)
    for ans_index in range(len(inter.answers)):
        embed.add_field(name=f"Raspuns {ans_index + 1}", value=inter.answers[ans_index], inline=False)
    return embed

def create_message(inter, numar_intrebare = None):
    if not numar_intrebare or numar_intrebare > len(QUESTIONS_DB["questions"]) or numar_intrebare < 1:
        # Invalid input. Get a random question.
        print_debug("Invalid input. Getting a random question.")
        numar_intrebare = random.randint(0, len(QUESTIONS_DB["questions"]) - 1) + 1
    
    inter.current_question_number = numar_intrebare
    inter.question = QUESTIONS_DB["questions"][numar_intrebare - 1]
    inter.answers = QUESTIONS_DB["answers"][numar_intrebare - 1]
    inter.correct_answers = QUESTIONS_DB["correct_answers"][numar_intrebare - 1]

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