import os
import discord
from commands.utils.get_server_path import get_server_path

async def update_server_properties_command(interaction: discord.Integration, server_name: str, property_name: str, property_value: str) -> None:
    await interaction.response.defer(thinking=True)

    server_path = get_server_path()
    properties_file = os.path.join(server_path, server_name, "server.properties")

    if not os.path.exists(properties_file):
        await interaction.followup.send(f"Server properties file for '{server_name}' does not exist.", ephemeral=True)
        return

    try:
        update_server_properties(server_path, server_name, property_name, property_value)
        await interaction.followup.send(f"Property '{property_name}' has been updated to '{property_value}' for server '{server_name}'.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"An error occurred while updating the property: {str(e)}", ephemeral=True)

def update_server_properties(server_path, server_name, property_name, property_value):
    """
    Update a specific property in the server.properties file.

    Args:
        server_path (str): The path to the server directory.
        server_name (str): The name of the server.
        property_name (str): The name of the property to update.
        property_value (str): The value to set for the property.
    """
    properties_file = os.path.join(server_path, server_name, "server.properties")

    # Create the file if it does not exist
    if not os.path.exists(properties_file):
        with open(properties_file, "w") as file:
            file.write(f"{property_name}={property_value}\n")
    else:
        with open(properties_file, "r") as file:
            lines = file.readlines()

        with open(properties_file, "w") as file:
            property_found = False
            for line in lines:
                if line.startswith(f"{property_name}="):
                    file.write(f"{property_name}={property_value}\n")
                    property_found = True
                else:
                    file.write(line)
            if not property_found:
                file.write(f"{property_name}={property_value}\n")
