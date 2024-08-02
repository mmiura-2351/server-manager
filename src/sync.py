import os
import argparse
import requests
from dotenv import load_dotenv

def get_commands():
    commands = []
    file_lines = []
    with open("setup.py", "r") as file:
        file_lines = file.readlines()

    parsing_block = ""
    parsing_lines = False
    for line in file_lines:
        # Extract command when @tree.command is found in the line.
        if "@tree.command" in line:
            parsing_lines = True
            parsing_block += line.strip()
        elif parsing_lines:
            parsing_block += line.strip()
            if parsing_block.endswith(")"):
                parsing_lines = False
                command_name = parsing_block.split('name="')[1].split('"')[0]
                command_description = parsing_block.split('description="')[1].split('"')[0]
                commands.append({"name": command_name, "description": command_description})
                parsing_block = ""

    return commands

def sync_commands(mode: str):
    """
    Syncs the Discord commands based on the specified mode.

    Args:
        mode (str): The mode for syncing commands ('global' or 'guild').
    """
    load_dotenv()
    application_id = os.getenv("APPLICATION_ID")
    guild_id = os.getenv("GUILD_ID")
    url = f"https://discord.com/api/v10/applications/{application_id}/guilds/{guild_id}/commands"
    headers = {
        "Authorization": f"Bot {os.getenv('DISCORD_TOKEN')}",
        "Content-Type": "application/json"
    }

    if mode == "global":
        url = f"https://discord.com/api/v10/applications/{application_id}/commands"

    commands = get_commands()

    # Get existing commands
    existing_commands = requests.get(url, headers=headers).json()
    existing_command_names = {cmd['name']: cmd['id'] for cmd in existing_commands}

    for command_data in commands:  # Loop to register each command
        if command_data['name'] in existing_command_names:
            # Update if command already exists
            command_id = existing_command_names[command_data['name']]
            update_url = f"{url}/{command_id}"
            response = requests.patch(update_url, headers=headers, json=command_data)
            if response.status_code == 200:
                print(f"{command_data['name'].capitalize()} command updated.")
            else:
                print("Failed to update command:", response.json())
        else:
            # Register new command
            response = requests.post(url, headers=headers, json=command_data)
            if response.status_code == 201:
                print(f"{command_data['name'].capitalize()} command synced.")
            else:
                print("Failed to sync command:", response.json())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync Discord commands.")
    parser.add_argument("-m", "--mode", type=str, required=True, help="Mode to sync commands: 'global' or 'guild'")
    args = parser.parse_args()
    sync_commands(args.mode)
