import disnake
from disnake.ext import commands
import json
import os
import asyncio

# 데이터 저장 파일 경로
DATA_FILE = "data/temp_channels.json"


def load_data():
    # 데이터 파일이 없으면 빈 딕셔너리 반환
    if not os.path.exists(DATA_FILE):
        return {}

    # JSON 파일 읽어서 딕셔너리로 반환
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    # 딕셔너리를 JSON 파일로 저장
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


class VoiceManager(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member,  # 상태가 변경된 멤버
        before,  # 변경 전 상태
        after    # 변경 후 상태
    ):

        # =====================
        # 생성 채널 입장 처리
        # =====================

        if after.channel:  # 사용자가 음성 채널에 들어갔을 때

            if after.channel.name == "➕ | 채널 생성":  # 특정 채널에 들어갔을 경우

                category = after.channel.category  # 해당 채널의 카테고리 가져오기

                # 새 음성 채널 생성 (멤버 이름 기반)
                new_channel = await category.create_voice_channel(
                    name=f"{member.display_name}의 음성채널"
                )

                # 멤버를 새로 만든 채널로 이동
                await member.move_to(new_channel)

                # 데이터 로드 후 새 채널 정보 저장
                data = load_data()

                data[str(new_channel.id)] = {
                    "owner": member.id  # 채널 소유자 ID 기록
                }

                save_data(data)

        # =====================
        # 빈 채널 자동 삭제 처리
        # =====================

        if before.channel:  # 사용자가 음성 채널에서 나갔을 때

            data = load_data()

            if str(before.channel.id) in data:  # 해당 채널이 임시 채널인지 확인

                await asyncio.sleep(1)  # 잠깐 대기 (멤버 이동 처리 안정화)

                if len(before.channel.members) == 0:  # 채널에 아무도 없으면

                    # 데이터에서 채널 정보 삭제
                    del data[str(before.channel.id)]

                    save_data(data)

                    # 실제 디스코드 서버에서 채널 삭제
                    await before.channel.delete(
                        reason="임시 음성채널 자동 삭제"
                    )


def setup(bot):
    # Cog 등록
    bot.add_cog(VoiceManager(bot))
