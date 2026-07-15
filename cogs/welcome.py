import disnake
from disnake.ext import commands


# ==========================
# 설정
# ==========================

WELCOME_CHANNEL_NAME = "👋ㅣ환영해요"

NOTICE_CHANNEL_NAME = "📢ㅣ공지사항"
RULE_CHANNEL_NAME = "📜ㅣ서버규칙"



class Welcome(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.invites = {}

    # 봇 준비
    @commands.Cog.listener()
    async def on_ready(self):

        self.invites.clear()

        for guild in self.bot.guilds:
            try:
                self.invites[guild.id] = await guild.invites()
            except:
                self.invites[guild.id] = []

        print("Welcome Cog Ready")

    # 새 멤버 입장
    @commands.Cog.listener()
    async def on_member_join(self, member):

        guild = member.guild

        # 환영 채널 찾기
        channel = disnake.utils.get(
            guild.text_channels,
            name=WELCOME_CHANNEL_NAME
        )

        if channel is None:
            return

        inviter = "알 수 없음"

        try:
            old_invites = self.invites.get(guild.id, [])
            new_invites = await guild.invites()

            for new in new_invites:
                for old in old_invites:

                    if (
                        new.code == old.code
                        and new.uses > old.uses
                    ):
                        inviter = new.inviter.mention
                        break

            self.invites[guild.id] = new_invites

        except:
            pass

        rule_channel = disnake.utils.get(
            guild.text_channels,
            name=RULE_CHANNEL_NAME
        )

        notice_channel = disnake.utils.get(
            guild.text_channels,
            name=NOTICE_CHANNEL_NAME
        )

        rule = (
            rule_channel.mention
            if rule_channel
            else "#서버규칙"
        )

        notice = (
            notice_channel.mention
            if notice_channel
            else "#공지사항"
        )

        embed = disnake.Embed(
            title="🎉 새로운 멤버가 입장했습니다!",
            color=0x57F287
        )

        # 오른쪽 프로필 사진
        embed.set_thumbnail(
            url=member.display_avatar.url
        )

        # 새 멤버
        embed.add_field(
            name="👤 새 멤버",
            value=member.mention,
            inline=True
        )

        # 초대한 사람
        embed.add_field(
            name="📨 초대한 사람",
            value=inviter,
            inline=True
        )

        embed.add_field(
            name="📢 안내",
            value=(
                f"📣 {notice} 채널을 읽어주세요.\n"
                f"✅ {rule} 채널을 확인해주세요.\n\n"
                
            ),
            inline=False
        )

        await channel.send(embed=embed)

    # 초대 생성 시 업데이트
    @commands.Cog.listener()
    async def on_invite_create(self, invite):

        self.invites[invite.guild.id] = await invite.guild.invites()

    # 초대 삭제 시 업데이트
    @commands.Cog.listener()
    async def on_invite_delete(self, invite):

        self.invites[invite.guild.id] = await invite.guild.invites()


def setup(bot):
    bot.add_cog(Welcome(bot))