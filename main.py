import os
from dotenv import load_dotenv

import disnake
from disnake.ext import commands

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

bot = commands.InteractionBot(
    intents=intents
)

@bot.event
async def on_ready():
    print(f"{bot.user} 온라인")

    print("등록된 슬래시 명령어:")
    for cmd in bot.slash_commands:
        print(cmd.name)

bot.load_extension("cogs.answer")
bot.load_extension("cogs.voice")
#bot.load_extension("cogs.inquiry")

bot.run(TOKEN)