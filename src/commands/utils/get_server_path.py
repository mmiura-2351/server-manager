import os
from dotenv import load_dotenv

def get_server_path():
    """
    Function to retrieve the server path.

    This function reads the absolute server path from the environment variable.
    If the environment variable is not set, it returns None.

    Returns:
        str: The absolute server path. Returns None if not set.
    """
    load_dotenv()
    SERVER_PATH = os.getenv("SERVER_PATH_ABS")
    return SERVER_PATH