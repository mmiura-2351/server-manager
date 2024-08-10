import os
import discord
import subprocess
import time
from commands.utils.get_server_path import get_server_path
from commands.utils.get_server_name import get_server_name
from commands.utils.get_password import get_passwords

async def ark_server_manager_command(interaction: discord.Integration, command: str) -> None:
    await interaction.response.defer(thinking=True)

    server_path_pre = get_server_path()
    server_name = get_server_name()
    server_path = server_path_pre.replace("server_name", server_name)
    ADMIN_PASSWD = get_passwords("ADMIN_PASSWORD")
    SERVER_PASSWD = get_passwords("SERVER_PASSWORD")

    if command == "start":

        if not server_path:
            await interaction.followup.send("Server path is not set.", ephemeral=True)
            return

        # Check Server directory
        server_directory = os.path.join(server_path)
        if not os.path.exists(server_directory):
            await interaction.followup.send(f"Server '{server_name}' is not exist.", ephemeral=True)
            return

        command = f"bash -c 'source ~/.bashrc && cd {server_path} && screen -dmS {server_name} ./ShooterGameServer LostIsland?listen?SessionName=regles-lostisland?ServerAdminPassword={ADMIN_PASSWD}?ServerPassword={SERVER_PASSWD} -server -log'"

        try:
            # サーバーを起動するコマンドを実行
            subprocess.run(command, shell=True, check=True)
            await interaction.followup.send("サーバーが正常に起動しました。", ephemeral=True)
        except subprocess.CalledProcessError:
            await interaction.followup.send("サーバーの起動に失敗しました。", ephemeral=True)

    elif command == "stop":
        SESSION_ID = get_screen_session_id(server_name)

        if SESSION_ID:
            try:
                subprocess.run(f"screen -S {SESSION_ID} -p 0 -X stuff 'SaveWorld\n'", shell=True, check=True)
                time.sleep(10)
                subprocess.run(f"screen -S {SESSION_ID} -X quit", shell=True, check=True)
                await interaction.followup.send(f"サーバー '{server_name}' が停止しました。", ephemeral=True)
            except subprocess.CalledProcessError as e:
                await interaction.followup.send(f"サーバーを停止中にエラーが発生しました: {e.stderr}", ephemeral=True)
        else:
            await interaction.followup.send(f"名前 '{server_name}' の実行中のサーバーが見つかりませんでした。", ephemeral=True)

    else:
        await interaction.followup.send("Invalid command is entered")

def get_screen_session_id(server_name: str) -> str:
    command = f"screen -ls | grep '{server_name}' | awk '{{print $1}}'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    else:
        return None
