from functii.quiz.utils import create_message
from views.mainmenu import MainMenu

async def setup_message_view(self, inter):
    view = MainMenu(inter.correct_answers, inter.current_question_number, inter.answers, inter.question)
    view.original_author = inter.author
    view.bot = self.bot
    
    view.message = await inter.edit_original_message(embed=inter.embed, view=view)

    # return view

if __name__ == "__main__":
    pass