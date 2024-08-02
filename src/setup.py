import discord
from commands.ping import ping_command

def SetupCommands(tree):
    """
    The SetupCommands function sets up the necessary slash commands
    for the provided CommandTree instance.

    Args:
        tree (app_commands.CommandTree): The CommandTree instance to register commands to
    """
    @tree.command(name="ping", description="Responds with ping")
    async def _ping(interaction: discord.Interaction) -> None:
        await ping_command(interaction)
