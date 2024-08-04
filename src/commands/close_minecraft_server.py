import discord
import subprocess

async def close_minecraft_server_command(interaction: discord.Integration, server_name: str) -> None:
    await interaction.response.defer(thinking=True)

    # Command to get the screen session ID
    SESSION_ID = get_screen_session_id(server_name)

    command = "stop"

    if SESSION_ID:
        command_to_send = f"screen -S {SESSION_ID} -p 0 -X stuff '{command}\n'"
        try:
            subprocess.run(command_to_send, shell=True, check=True)
            await interaction.followup.send(f"Server '{server_name}' has been stopped.", ephemeral=True)
        except subprocess.CalledProcessError as e:
            await interaction.followup.send(f"An error occurred while stopping the server: {e.stderr}", ephemeral=True)
    else:
        await interaction.followup.send(f"No running server found with the name '{server_name}'.", ephemeral=True)

def get_screen_session_id(server_name: str) -> str:
    # Command to get the screen session ID
    command = f"screen -ls | grep '{server_name}' | awk '{{print $1}}'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    else:
        return None
