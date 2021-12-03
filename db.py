import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

data = os.environ.get("DB")
user = os.environ.get("DB_USER")
host = os.environ.get("DB_HOST")
password = os.environ.get("DB_PASS")

conn_string = f"dbname='{data}' user='{user}' host='{host}' password='{password}'"

db = psycopg2.connect(conn_string)

# print("Connecting to database ... ")

# cursor = conn.cursor()
print("Connected!\n")
