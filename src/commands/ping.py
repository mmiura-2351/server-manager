def ping_command(interaction: discord.Interaction) -> None:
    """
    Responds with Pong
    """
    await interaction.response.send_message("Pong!")
