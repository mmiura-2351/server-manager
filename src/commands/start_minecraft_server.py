import os
import discord
import subprocess
import time
from commands.utils.get_ip import get_ip
from commands.utils.get_server_path import get_server_path

async def start_minecraft_server_command(interaction: discord.Integration, server_name: str) -> None:
    await interaction.response.defer(thinking=True)

    server_path = get_server_path()
    server_ip = get_ip()
    server_port = 25565

    if not server_path:
        await interaction.followup.send("Server path is not set.", ephemeral=True)
        return

    # Check Server directory
    server_directory = os.path.join(server_path, server_name)
    if not os.path.exists(server_directory):
        await interaction.followup.send(f"Server '{server_name}' is not exist.", ephemeral=True)
        return

    # Ensure the server port is set to 25565
    set_server_port(server_path, server_name, server_port)

    for attempt in range(3):
        command = f"bash -c 'source ~/.bashrc && cd {server_path}/{server_name} && screen -dmS {server_name} java -Xmx8192M -Xms8192M -jar server.jar nogui'"

        try:
            # Start Server
            _result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            time.sleep(10)  # Wait for the server to start

            # Check if the screen session exists
            screen_check = subprocess.run(f"screen -list | grep -q {server_name}", shell=True)
            if screen_check.returncode == 0:
                await interaction.followup.send(f"Server '{server_name}' has been started.\n**IP**\n```{server_ip}:{server_port}```", ephemeral=True)
                return
            else:
                # Increment port in server.properties
                increment_server_port(server_path, server_name)
                server_port += 1
        except subprocess.CalledProcessError as e:
            await interaction.followup.send(f"An error occurred while starting the server: {e.stderr}", ephemeral=True)
            return

    await interaction.followup.send("Failed to start the server after 3 attempts.", ephemeral=True)

def set_server_port(server_path, server_name, port):
    """
    Set the port number in server.properties file to a specific value
    """
    properties_file = os.path.join(server_path, server_name, "server.properties")

    # Create the file if it does not exist
    if not os.path.exists(properties_file):
        with open(properties_file, "w") as file:
            file.write(f"server-port={port}\n")
    else:
        with open(properties_file, "r") as file:
            lines = file.readlines()

        with open(properties_file, "w") as file:
            for line in lines:
                if line.startswith("server-port="):
                    file.write(f"server-port={port}\n")
                else:
                    file.write(line)

def increment_server_port(server_path, server_name):
    """
    Increment the port number in server.properties file
    """
    properties_file = os.path.join(server_path, server_name, "server.properties")
    with open(properties_file, "r") as file:
        lines = file.readlines()

    with open(properties_file, "w") as file:
        for line in lines:
            if line.startswith("server-port="):
                port = int(line.split("=")[1].strip()) + 1
                file.write(f"server-port={port}\n")
            else:
                file.write(line)
