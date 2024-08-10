import discord
from commands.ping import ping_command
from commands.ark_server_manager import ark_server_manager_command
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

    @tree.command(name="ark", description="Manage ARK Server")
    @discord.app_commands.choices(
        command=[
            discord.app_commands.Choice(name="start", value="start"),
            discord.app_commands.Choice(name="stop", value="stop")
        ])
    async def _ark_server_manager(interaction: discord.Interaction, command: str):
        await ark_server_manager_command(interaction, command)
