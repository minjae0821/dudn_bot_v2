import disnake
from disnake.ext import commands

INSTALL_DATA = [
    {
        "category": "🤖 | 봇 기능",
        "channels": [
            ("text", "🎧ㅣ채널생성")
            ("text", "📨ㅣ문의하기")
        ]
    },
    {
        "category": "⌨️ | 채팅 채널",
        "channels": [
            ("text", "🗨️ㅣ자유채팅"),
            ("text", "📸ㅣ스크린샷")
        ]
    },
    {
        "category": "🎙️ | 음성 채널",
        "channels": [
            ("voice", "🛏️ | Sleep"),
            ("voice", "☕ | Cafe")
            ("voice", "➕ | 채널 생성")
        ]
    }
]


class Setup(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="설치",
        description="봇을 설치합니다."
    )
    async def setup(self, inter):

        if not inter.author.guild_permissions.administrator:
            await inter.response.send_message(
                "❌ 관리자만 사용할 수 있습니다.",
                ephemeral=True
            )
            return

        await inter.response.defer(ephemeral=True)

        for data in INSTALL_DATA:

            # 카테고리 생성
            category = disnake.utils.get(
                inter.guild.categories,
                name=data["category"]
            )

            if category is None:
                category = await inter.guild.create_category(
                    data["category"]
                )

            # 채널 생성
            for channel_type, name in data["channels"]:

                if channel_type == "voice":

                    if disnake.utils.get(
                        category.voice_channels,
                        name=name
                    ) is None:

                        await category.create_voice_channel(name)

                else:

                    if disnake.utils.get(
                        category.text_channels,
                        name=name
                    ) is None:

                        await category.create_text_channel(name)

        await inter.edit_original_response(
            content="✅ 봇 설치가 완료되었습니다."
        )


def setup(bot):
    bot.add_cog(Setup(bot))