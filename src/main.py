import os
import discord
from discord import app_commands
from dotenv import load_dotenv
from Setup import SetupCommands

def main():
    # Create Bot instance
    bot = discord.Client(intents=intents())
    # Create CommandTree instance
    tree = app_commands.CommandTree(bot)

    # Setup slash commands
    SetupCommands(tree)

    # Start discord bot
    load_dotenv()
    bot.run(os.getenv("DISCORD_TOKEN"))

def intents():
    """
    This function sets the intents for the Discord bot.
    It uses the default intents and enables message-related intents.

    Returns:
        discord.Intents: The configured intents object
    """
    intents = discord.Intents.default()
    intents.messages = True
    return intents    

if __name__ == "__main__":
    main()