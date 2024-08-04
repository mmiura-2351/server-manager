import os
import discord
import subprocess
from dotenv import load_dotenv

async def show_all_servers_command(interaction: discord.Interaction) -> None:
    await interaction.response.defer(thinking=True)
    load_dotenv()

    server_path = os.getenv("SERVER_PATH_ABS")

    if not server_path:
        await interaction.followup.send("Server path is not set.", ephemeral=True)
        return

    command = f"bash -c 'source ~/.bashrc && cd {server_path} && ls'"

    try:
        _result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        output = _result.stdout.strip()
        await interaction.followup.send(f"Servers:\n```\n{output}\n```", ephemeral=True)
    except subprocess.CalledProcessError as e:
        await interaction.followup.send(f"An error occurred while getting the servers: {e.stderr}", ephemeral=True)