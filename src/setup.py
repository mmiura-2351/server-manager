import discord
from commands.ping import ping_command
from commands.create_vanilla_server import create_vanilla_server_command
from commands.start_minecraft_server import start_minecraft_server_command
from commands.close_minecraft_server import close_minecraft_server_command
from commands.show_all_servers import show_all_servers_command
from commands.update_server_properties import update_server_properties_command

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

    @tree.command(name="create", description="Create Vanilla Server")
    @discord.app_commands.describe(version="Server Version")
    @discord.app_commands.describe(server_name="Server name")
    async def _create_vanilla_server(interaction: discord.Interaction, version: str, server_name: str) -> None:
        await create_vanilla_server_command(interaction, version, server_name)

    @tree.command(name="start", description="Start Minecraft Server")
    @discord.app_commands.describe(server_name="Server name")
    async def _start_minecraft_server(interaction: discord.Interaction, server_name: str) -> None:
        await start_minecraft_server_command(interaction, server_name)

    @tree.command(name="close", description="Stop Minecraft Server")
    @discord.app_commands.describe(server_name="Server name")
    async def _close_minecraft_server(interaction: discord.Interaction, server_name: str) -> None:
        await close_minecraft_server_command(interaction, server_name)

    @tree.command(name="list", description="Show All Servers")
    async def _show_all_servers(interaction: discord.Interaction) -> None:
        await show_all_servers_command(interaction)

    @tree.command(name="update-property", description="Update server.properties")
    @discord.app_commands.describe(server_name="Server name")
    @discord.app_commands.describe(property_name="Property name")
    @discord.app_commands.describe(value="Property value")
    async def _update_server_properties(interaction: discord.Integration, server_name: str, property_name: str, value: str) -> None:
        await update_server_properties_command(interaction, server_name, property_name, value)
