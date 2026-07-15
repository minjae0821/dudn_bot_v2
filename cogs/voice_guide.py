import disnake
from disnake.ext import commands

class VoiceEmbed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("VoiceEmbed 준비 완료!")

        # 채널 이름으로 찾기
        channel = disnake.utils.get(
            self.bot.get_all_channels(),
            name="🎧ㅣ채널생성"
        )

        if channel is None:
            print("🎧ㅣ채널생성 채널을 찾을 수 없습니다.")
            return

        # 안내 임베드 생성
        embed = disnake.Embed(
            title="🎧 음성 채널 생성",
            description=(
                "아래 **`➕ | 채널 생성`** 음성채널에 입장하면\n"
                "**개인 음성채널이 자동으로 생성됩니다.**"
            ),
            color=0x5865F2
        )

        embed.add_field(
            name="📌 이용 방법",
            value=(
                "➊ **➕ | 채널 생성** 음성채널 입장\n"
                "➋ 개인 음성채널 자동 생성\n"
                "➌ 친구들과 자유롭게 이용"
            ),
            inline=False
        )

        embed.add_field(
            name="💡 안내",
            value=(
                "• 채널에 아무도 없으면 자동으로 삭제됩니다."
            ),
            inline=False
        )

        # ==========================
        # 이미 임베드가 있는지 확인
        # ==========================
        async for message in channel.history(limit=20):
            if (
                message.author == self.bot.user
                and message.embeds
                and message.embeds[0].title == "🎧 음성 채널 생성"
            ):
                print("안내 임베드가 이미 존재합니다.")
                return

        # 임베드가 없으면 전송
        await channel.send(embed=embed)
        print("안내 임베드 전송 완료!")

def setup(bot):
    bot.add_cog(VoiceEmbed(bot))