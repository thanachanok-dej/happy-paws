import os


import mariadb
from dotenv import load_dotenv
# 1. Load variables from the .env file
load_dotenv()
def get_connection():
    # 2. Create and return a MariaDB connection
    return mariadb.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )
