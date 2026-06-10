import disnake
from disnake.ext import commands

class Answer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="대답",
        description="테스트 명령어"
    )
    async def answer(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message("넵")

def setup(bot):
    bot.add_cog(Answer(bot))