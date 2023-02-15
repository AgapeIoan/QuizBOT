import datetime
import os
import json
import disnake
import random
import functii.quiz.quiz
import functii.quiz.utils

from typing import List
from disnake.ext import commands
from disnake import Option, OptionType

from functii.debug import print_debug, print_log
from functii.sql import read_answered_questions
from views.mainmenu import MainMenu

class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="quiz",
        description="Get a quiz question",
        options=[
            Option("numar_intrebare", "Numarul intrebarii", OptionType.integer, required=False),
            Option("mesaj_ascuns", "Mesaj ascuns", OptionType.boolean, required=False)
        ]
    )
    async def quiz(self, inter: disnake.CommandInteraction, numar_intrebare: int = None, mesaj_ascuns: bool = True):
        await inter.response.defer(ephemeral=mesaj_ascuns)
        # mesaj_ascuns = ephemeral

        inter = functii.quiz.utils.create_message(inter, numar_intrebare)
        await functii.quiz.quiz.setup_message_view(self, inter)
        

    @commands.slash_command(
        name="progress",
        description="Get overall progress"
    )
    async def progress(self, inter: disnake.CommandInteraction):
        await inter.response.defer(ephemeral=True)

        intrebari = read_answered_questions(inter.author.id)
        # intrebari = [(1,), (2,), (3,), (5,), (6,), (9,), (10,), (11,)]
        intrebari = [i[0] for i in intrebari]
        intrebari.sort()
        intrebari = list(dict.fromkeys(intrebari))
        intrebari = list(functii.quiz.utils.ranges(intrebari))

        if intrebari:
            output = "".join(f"{intrebare[0]} - {intrebare[1]}\n" for intrebare in intrebari)

        await inter.edit_original_message(content=f"**Intrebari rezolvate:\n** {output}")
            

def setup(bot):
    bot.add_cog(Quiz(bot))
