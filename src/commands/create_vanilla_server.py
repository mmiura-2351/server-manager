import os
import discord
import subprocess
from dotenv import load_dotenv
from commands.utils.get_server_path import get_server_path

async def create_vanilla_server_command(interaction: discord.Interaction, version: str, server_name: str) -> None:
    await interaction.response.defer(thinking=True)
    load_dotenv()

    # Get Server Path
    server_path = get_server_path()
    mss = os.getenv("SERVER_SETUP_PATH_ABS")

    if not server_path:
        await interaction.followup.send("Server path is not set.", ephemeral=True)
        return

    if not mss:
        await interaction.followup.send("Server setup script path is not set.", ephemeral=True)
        return

    # Full command
    command = f"bash -c 'source ~/.bashrc && cd {server_path} && {mss} -v {version} -s vanilla -d {server_name}'"

    try:
        # Create Server
        _result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        await interaction.followup.send(f"Server '{server_name}' has been created.", ephemeral=True)
    except subprocess.CalledProcessError as e:
        await interaction.followup.send(f"An error occurred while creating the server: {e.stderr}", ephemeral=True)
