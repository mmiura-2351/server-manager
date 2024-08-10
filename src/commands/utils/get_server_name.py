import os
from dotenv import load_dotenv

def get_server_name():
    load_dotenv()
    SERVER_PATH = os.getenv("SERVER_NAME")
    return SERVER_PATH
