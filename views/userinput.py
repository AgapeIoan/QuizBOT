import disnake

from disnake import TextInputStyle

class AnswerUserInput(disnake.ui.Modal):
    def __init__(self, answer: str = None, current_question_number: int = 0, question: str = None):
        self.answer = answer

        components = [
            disnake.ui.TextInput(
                label="Raspuns",
                placeholder=question[:100],
                custom_id="response",
                style=TextInputStyle.long,
            ),
        ]
        super().__init__(
            title=f"Intrebarea #{str(current_question_number)}",
            custom_id="modal_quiz_answer",
            components=components,
        )

    async def callback(self, inter: disnake.ModalInteraction):
        embed = inter.message.embeds[0]
        response = inter.text_values["response"]
        self.answer = str(self.answer) # In caz ca a scapat un integer in raspuns
        if self.answer.lower().strip() == response.lower().strip():
            embed.color = disnake.Color.green()
        else:
            embed.color = disnake.Color.red()
            embed.add_field(name="Raspuns corect", value=self.answer, inline=False)
        
        await inter.response.edit_message(embed=embed)
