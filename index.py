import os
import disnake
import time
from disnake.ext import commands


from functii.debug import DEBUG_STATE, print_log
from functii.bools import BOT_TOKEN

# intent pentru events vezi #8
bot = commands.Bot(command_prefix=commands.when_mentioned, intents=disnake.Intents.all())

@bot.slash_command(
    name="ping",
    description="Pings the bot.",
)
async def ping(inter):
    za_ping = round(bot.latency * 1000)
    await inter.response.send_message(f'**Pong!**\n🏓 {za_ping} ms')

@bot.listen()
async def on_ready():
    game = disnake.Activity(name="Mentenanta temporara", type=disnake.ActivityType.watching)
    await bot.change_presence(activity=game, status=disnake.Status.dnd)

    print_log("Connected succesfully!")
    print_log("Invite link: " + disnake.utils.oauth_url(bot.user.id))
    print_log(f"Name: {bot.user}")
    print_log(f"Servers: {len(bot.guilds)}")
    print_log(f"Latency: {bot.latency}")
    print_log(f"Status: {bot.status}")
    print_log(f"")


print_log("Logging in...\n")
if not DEBUG_STATE:
    print_log("DEBUG_STATE is False, production token is going to be used!")
    for i in range(3):
        print_log("Bot is starting in " + str(3*5 - i*5) + " seconds.")
        # time.sleep(5)

# load cog
for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")
        print_log(f"Loaded cogs.{name}!")

bot.run(BOT_TOKEN)
