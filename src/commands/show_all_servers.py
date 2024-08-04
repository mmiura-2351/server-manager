import os
import discord
import subprocess
from commands.utils.get_ip import get_ip
from commands.utils.get_server_path import get_server_path

async def show_all_servers_command(interaction: discord.Interaction) -> None:
    await interaction.response.defer(thinking=True)

    server_path = get_server_path()

    if not server_path:
        await interaction.followup.send("Server path is not set.", ephemeral=True)
        return

    command = f"bash -c 'source ~/.bashrc && cd {server_path} && ls'"

    try:
        _result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        output = _result.stdout.strip()
        servers = output.split('\n')

        server_list = []
        for server in servers:
            status_command = f"screen -list | grep {server}"
            status_result = subprocess.run(status_command, shell=True, text=True, capture_output=True)
            if status_result.returncode == 0:
                # Assuming server_ip and server_port are stored in server.properties
                properties_file = os.path.join(server_path, server, "server.properties")
                server_ip = get_ip()
                server_port = "25565"  # Default port
                if os.path.exists(properties_file):
                    with open(properties_file, "r") as file:
                        for line in file:
                            if line.startswith("server-port="):
                                server_port = line.split("=")[1].strip()
                server_list.append(f"{server} (Running: {server_ip}:{server_port})")
            else:
                server_list.append(f"{server} (Not Running)")

        if server_list:
            await interaction.followup.send(f"Servers:\n```\n" + "\n".join(server_list) + "\n```", ephemeral=True)
        else:
            await interaction.followup.send("No servers found.", ephemeral=True)
    except subprocess.CalledProcessError as e:
        await interaction.followup.send(f"An error occurred while getting the servers: {e.stderr}", ephemeral=True)
