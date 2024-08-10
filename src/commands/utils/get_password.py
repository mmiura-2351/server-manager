import os
from dotenv import load_dotenv

def get_passwords(name):
    load_dotenv()
    return os.getenv(name)