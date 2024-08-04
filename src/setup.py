import discord
from commands.ping import ping_command
from commands.create_vanilla_server import create_vanilla_server_command
from commands.start_minecraft_server import start_minecraft_server_command
from commands.close_minecraft_server import close_minecraft_server_command

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

    @tree.command(name="server-create", description="Create Vanilla Server")
    @discord.app_commands.describe(version="Server Version")
    @discord.app_commands.describe(server_name="Server name")
    async def _create_vanilla_server(interaction: discord.Interaction, version: str, server_name: str) -> None:
        await create_vanilla_server_command(interaction, version, server_name)

    @tree.command(name="server-start", description="Start Minecraft Server")
    @discord.app_commands.describe(server_name="Server name")
    async def _start_minecraft_server(interaction: discord.Interaction, server_name: str) -> None:
        await start_minecraft_server_command(interaction, server_name)

    @tree.command(name="server-close", description="Stop Minecraft Server")
    @discord.app_commands.describe(server_name="Server name")
    async def _close_minecraft_server(interaction: discord.Interaction, server_name: str) -> None:
        await close_minecraft_server_command(interaction, server_name)
