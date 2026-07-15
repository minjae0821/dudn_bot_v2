import disnake
from disnake.ext import commands


# ===========================
# 문의 작성 Modal
# ===========================
class InquiryModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="문의 내용",
                placeholder="문의 내용을 입력해주세요.",
                custom_id="content",
                style=disnake.TextInputStyle.paragraph,
                max_length=1000,
            )
        ]

        super().__init__(
            title="문의 작성",
            custom_id="inquiry_modal",
            components=components,
        )

    async def callback(self, inter: disnake.ModalInteraction):

        content = inter.text_values["content"]

        manage_channel = disnake.utils.get(
            inter.guild.text_channels,
            name="📩-문의관리"
        )

        if manage_channel is None:
            await inter.response.send_message(
                "❌ `📩-문의관리` 채널을 찾을 수 없습니다.",
                ephemeral=True,
            )
            return

        embed = disnake.Embed(
            title="📩 새로운 문의",
            color=disnake.Color.blue()
        )

        embed.add_field(
            name="작성자",
            value=f"{inter.author.mention}\n({inter.author})",
            inline=False,
        )

        embed.add_field(
            name="유저 ID",
            value=str(inter.author.id),
            inline=False,
        )

        embed.add_field(
            name="문의 내용",
            value=content,
            inline=False,
        )

        embed.set_thumbnail(
            url=inter.author.display_avatar.url
        )

        await manage_channel.send(embed=embed)

        await inter.response.send_message(
            "✅ 문의가 정상적으로 접수되었습니다.",
            ephemeral=True,
        )


# ===========================
# 문의 버튼
# ===========================
class InquiryView(disnake.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(
        label="문의하기",
        style=disnake.ButtonStyle.primary,
        custom_id="inquiry_button",
        emoji="📨"
    )
    async def inquiry_button(
        self,
        button: disnake.ui.Button,
        inter: disnake.MessageInteraction,
    ):
        await inter.response.send_modal(
            InquiryModal()
        )


# ===========================
# Cog
# ===========================
class Inquiry(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.ready = False

    async def cog_load(self):
        # Persistent View 등록 (한 번만)
        self.bot.add_view(InquiryView())

    # ---------------------------
    # 봇 시작 시 문의 안내 임베드 생성
    # ---------------------------
    @commands.Cog.listener()
    async def on_ready(self):

        # 재접속 시 중복 실행 방지
        if self.ready:
            return

        self.ready = True

        channel = disnake.utils.get(
            self.bot.get_all_channels(),
            name="📨ㅣ문의하기"
        )

        if channel is None:
            print("[문의] '📨ㅣ문의하기' 채널을 찾을 수 없습니다.")
            return

        # 이미 안내 임베드가 있는지 확인
        async for message in channel.history(limit=None):

            if (
                message.author == self.bot.user
                and message.embeds
                and message.embeds[0].title == "📨 문의센터"
            ):
                print("[문의] 안내 임베드가 이미 존재합니다.")
                return
        
        embed = disnake.Embed(
            title="📨 문의센터",
            description=(
                "문의가 필요하시면 아래 버튼을 눌러 문의를 작성해주세요.\n\n"
                "또는 **`/문의`** 명령어를 사용하셔도 됩니다.\n\n"
                "문의 내용은 관리자에게만 전달됩니다."
            ),
            color=disnake.Color.green(),
        )

        embed.set_footer(
            text="문의는 신중하게 작성해주세요."
        )

        await channel.send(
            embed=embed,
            view=InquiryView()
        )

        print("[문의] 안내 임베드 생성 완료")

    # ---------------------------
    # /문의
    # ---------------------------
    @commands.slash_command(
        name="문의",
        description="관리자에게 문의를 보냅니다."
    )
    async def inquiry(
        self,
        inter: disnake.ApplicationCommandInteraction
    ):

        embed = disnake.Embed(
            title="📨 문의하기",
            description=(
                "아래 버튼을 눌러 문의를 작성해주세요.\n\n"
                "문의 내용은 관리자에게만 전달됩니다."
            ),
            color=disnake.Color.green(),
        )

        await inter.response.send_message(
            embed=embed,
            view=InquiryView(),
            ephemeral=True,
        )

def setup(bot):
    bot.add_cog(Inquiry(bot))
