import asyncio
import disnake

from functii.quiz.utils import set_buttons_red_and_green, create_message, reset_buttons, disable_answer_buttons, remove_answer_buttons, find_button_by_custom_id
from functii.debug import print_debug, print_log
from functii.sql import send_answer_to_db
from views.userinput import AnswerUserInput

class MainMenu(disnake.ui.View):
    message: disnake.Message
    original_author: disnake.User

    def __init__(self, correct_answers: list, current_question_number: int, answers: list, question: str, *args, **kwargs):
        super().__init__(timeout=0)
        self.correct_answers = correct_answers
        self.current_question_number = current_question_number
        self.answers = answers
        self.question = question
        self.buttons_number = len(answers)
        self.free_row = 0
        self.needs_user_input = len(answers) <= 1
        for i in range(self.buttons_number):
            self.free_row = int(i / 5)
            self.add_item(AnswerButton(label=f"Raspuns {i+1}", custom_id=f"{i+1}", row=self.free_row))

    # Timeout and error handling.
    async def on_timeout(self):
        for i in self.children:
            i.disabled = True

        await self.message.edit(content="**🔒 Butoanele au fost dezactivate datorita inactivitatii!**", view=self)

    async def interaction_check(self, interaction):
        if interaction.author.id == self.original_author.id:
            return True

        await interaction.response.send_message("**❗ Nu poti folosi comanda deoarece nu esti autorul acesteia!**", ephemeral=True)

        return False
    
    @disnake.ui.button(style=disnake.ButtonStyle.green, label="Trimite", custom_id="send", row=4)
    async def send_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        button.disabled = True
        button.style = disnake.ButtonStyle.gray
        
        next_button = find_button_by_custom_id(self, "next")
        next_button.disabled = False
        next_button.style = disnake.ButtonStyle.green
        
        possible_answers = [] # mereu crescator
        self.correct_answers.sort()

        for i in self.children:
            if i.style == disnake.ButtonStyle.blurple:
                possible_answers.append(int(i.custom_id))
        
        if self.needs_user_input:
            modal = AnswerUserInput(self.correct_answers[0], self.current_question_number, self.question)
            await interaction.response.send_modal(modal)

            await interaction.edit_original_message(view=self)
            send_answer_to_db(self.original_author.id, self.current_question_number, 0)
            
        elif possible_answers == self.correct_answers:
            self = set_buttons_red_and_green(self, self.buttons_number, self.correct_answers)
            embed = interaction.message.embeds[0]
            embed.color = disnake.Color.green()
            await interaction.response.edit_message(view=self, embed=embed)

        elif self.correct_answers == [0]:
            self = set_buttons_red_and_green(self, self.buttons_number)
            await interaction.response.edit_message(view=self)

        else:
            self = set_buttons_red_and_green(self, self.buttons_number, self.correct_answers)
            embed = interaction.message.embeds[0]
            embed.color = disnake.Color.red()
            await interaction.response.edit_message(view=self, embed=embed)

        print_debug("possible_answers: " + str(possible_answers))
        print_debug("correct_answers: " + str(self.correct_answers))

        for ans in possible_answers:
            try:
                send_answer_to_db(self.original_author.id, self.current_question_number, ans, self.answers, True)
            except Exception as e:
                print_log(f"Error sending data to db: {e}")
                pass
        
    @disnake.ui.button(style=disnake.ButtonStyle.gray, label="Urmatoarea intrebare", custom_id="next", row=4, disabled=True)
    async def next_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.defer()
        self.current_question_number += 1
        self = reset_buttons(self)
        interaction = create_message(interaction, self.current_question_number)
        self.correct_answers = interaction.correct_answers
        self.question = interaction.question
        self.answers = interaction.answers

        self = remove_answer_buttons(self)

        self.buttons_number = len(interaction.answers)
        self.free_row = 0
        self.needs_user_input = len(interaction.answers) <= 1

        for i in range(self.buttons_number):
            self.free_row = int(i / 5)
            self.add_item(AnswerButton(label=f"Raspuns {i+1}", custom_id=f"{i+1}", row=self.free_row))

        await interaction.edit_original_message(embed=interaction.embed, view=self)
    

class AnswerButton(disnake.ui.Button):
    def __init__(self, label: str, *args, **kwargs):
        super().__init__(style=disnake.ButtonStyle.gray, label=label, *args, **kwargs)
        
    async def callback(self, interaction: disnake.MessageInteraction):
        await interaction.response.defer()
        if self.style == disnake.ButtonStyle.gray:
           self.style = disnake.ButtonStyle.blurple
        else:
            self.style = disnake.ButtonStyle.gray
        await interaction.edit_original_message(view=self.view)
        