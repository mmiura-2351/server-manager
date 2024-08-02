import time
import discord

async def ping_command(interaction: discord.Interaction) -> None:
    """
    Responds ping
    """
    send_time = interaction.created_at.timestamp()  # interaction.created_atをタイムスタンプに変換
    delay = (time.time() - send_time) * 1000  # 遅延を計算
    await interaction.response.send_message(f"Bot ping: {round(delay)}ms")
