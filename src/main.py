import os
import discord
from discord import app_commands
from dotenv import load_dotenv
from setup import SetupCommands

def main():
    # Create Bot instance
    bot = discord.Client(intents=intents())
    # Create CommandTree instance
    tree = app_commands.CommandTree(bot)

    discord_events(bot, tree)

    # Setup slash commands
    SetupCommands(tree)

    # Start discord bot
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

def discord_events(bot, tree):
    """
    The discord_events function sets up event handlers for the Discord bot.
    It includes the on_ready event which synchronizes the command tree when the bot is ready.

    Args:
        bot (discord.Client): The Discord bot instance
        tree (app_commands.CommandTree): The CommandTree instance to synchronize

    Example:
        @bot.event
        async def on_ready():
            await tree.sync()
    """
    # Sync command tree when bot is ready
    @bot.event
    async def on_ready():
        await tree.sync(guild=discord.Object(id=os.getenv("GUILD_ID")))

if __name__ == "__main__":
    load_dotenv()
    main()
