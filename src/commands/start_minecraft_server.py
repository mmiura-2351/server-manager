import os
import discord
import subprocess
from dotenv import load_dotenv

async def start_minecraft_server_command(interaction: discord.Integration, server_name: str) -> None:
    await interaction.response.defer(thinking=True)
    load_dotenv()

    server_path = os.getenv("SERVER_PATH_ABS")
    server_ip = get_ip()

    if not server_path:
        await interaction.followup.send("Server path is not set.", ephemeral=True)
        return

    command = f"bash -c 'source ~/.bashrc && cd {server_path}/{server_name} && screen -dmS {server_name} java -Xmx8192M -Xms8192M -jar server.jar nogui'"

    try:
        # Start Server
        _result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        await interaction.followup.send(f"Server '{server_name}' has been started.\n**IP**\n```{server_ip}```", ephemeral=True)
    except subprocess.CalledProcessError as e:
        await interaction.followup.send(f"An error occurred while starting the server: {e.stderr}", ephemeral=True)

def get_ip():
    """
    Get Global IPv4 IP Address
    return:
        ip_address: string
    """
    ip_address = subprocess.check_output(["curl", "-s", "https://api.ipify.org"]).decode("utf-8").strip()
    return ip_address
