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
    parse_mode = ""
    for line in file_lines:
        # Extract command when @tree.command is found in the line.
        if "@tree.command" in line:
            parse_mode = "command"
            parsing_block += line.strip()
        if parse_mode == "command":
            parsing_block += line.strip()
            if parsing_block.endswith(")"):
                parse_mode = ""
                command_name = parsing_block.split("name=\"")[1].split("\"")[0]
                command_description = parsing_block.split("description=\"")[1].split("\"")[0]
                command_data = {
                    "name": command_name,
                    "description": command_description,
                    "options": []
                }
                commands.append(command_data)
                parsing_block = ""

        # Extract choices when @discord.app_command.choices is found in the line.
        if "@discord.app_commands.choices" in line:
            parse_mode = "choices"
            parsing_block = 1
        if parse_mode == "choices":
            if parsing_block == 1 and "=" in line:
                option_name = line.split("=")[0].strip()
                commands[-1]["options"].append({
                    "name": option_name,
                    "description": option_name,
                    "type": 3,
                    "required": True,
                    "choices": []
                })
                parsing_block = 2
            if parsing_block == 2 and "discord.app_commands.Choice" in line:
                choices_name = line.split("name=\"")[1].split("\"")[0]
                choices_value = line.split("value=\"")[1].split("\"")[0]
                # Add choices to the last command's options
                commands[-1]["options"][-1]["choices"].append({
                    "name": choices_name,
                    "value": choices_value,
                })
            if "]" in line:
                parse_mode = ""
                parsing_block = ""

        # Extract describe when @discord.app_commands.describe is found in the line.
        if "@discord.app_commands.describe" in line:
            option_name = line.split("=")[0].strip().split("(")[1]
            description = line.split("=")[1].strip().strip('"').replace(")", "")
            commands[-1]["options"].append({
                "name": option_name,
                "description": description,
                "type": 3,
                "required": True,
            })

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
        "Authorization": f"Bot {os.getenv("DISCORD_TOKEN")}",
        "Content-Type": "application/json"
    }

    if mode == "global":
        url = f"https://discord.com/api/v10/applications/{application_id}/commands"

    commands = get_commands()

    # Get existing commands
    existing_commands = requests.get(url, headers=headers).json()
    existing_command_names = {cmd["name"]: cmd["id"] for cmd in existing_commands}

    for command_data in commands:  # Loop to register each command
        if command_data["name"] in existing_command_names:
            # Update if command already exists
            command_id = existing_command_names[command_data["name"]]
            update_url = f"{url}/{command_id}"
            response = requests.patch(update_url, headers=headers, json=command_data)
            if response.status_code == 200:
                print(f"{command_data["name"].capitalize()} command updated.")
            else:
                print("Failed to update command:", response.json())
        else:
            # Register new command
            response = requests.post(url, headers=headers, json=command_data)
            if response.status_code == 201:
                print(f"{command_data["name"].capitalize()} command synced.")
            else:
                print("Failed to sync command:", response.json())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync Discord commands.")
    parser.add_argument("-m", "--mode", type=str, required=True, help="Mode to sync commands: 'global' or 'guild'")
    args = parser.parse_args()
    sync_commands(args.mode)
