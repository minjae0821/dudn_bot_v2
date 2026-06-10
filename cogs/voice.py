import disnake
from disnake.ext import commands
import json
import os

DATA_FILE = "data/temp_channels.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


class VoiceManager(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member,
        before,
        after
    ):

        # =====================
        # 생성 채널 입장
        # =====================

        if after.channel:

            if after.channel.name == "➕ 채널 생성":

                category = after.channel.category

                new_channel = await category.create_voice_channel(
                    name=f"{member.display_name}의 음성채널"
                )

                await member.move_to(new_channel)

                data = load_data()

                data[str(new_channel.id)] = {
                    "owner": member.id
                }

                save_data(data)

        # =====================
        # 빈 채널 자동 삭제
        # =====================

        if before.channel:

            data = load_data()

            if str(before.channel.id) in data:

                if len(before.channel.members) == 0:

                    del data[str(before.channel.id)]

                    save_data(data)

                    await before.channel.delete(
                        reason="임시 음성채널 자동 삭제"
                    )


def setup(bot):
    bot.add_cog(VoiceManager(bot))