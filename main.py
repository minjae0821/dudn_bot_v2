import os
import disnake
from disnake.ext import commands
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# 인텐트 설정
intents = disnake.Intents.default()
intents.message_content = True
intents.voice_states = True

# 봇 생성
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"봇 로그인 완료: {bot.user}")

# cogs/voice.py Cog 불러오기
bot.load_extension("cogs.channel")
bot.load_extension("cogs.voice")
bot.load_extension("cogs.voice_guide")
bot.load_extension("cogs.ticket")
bot.load_extension("cogs.welcome")

# 실행
bot.run(TOKEN)
