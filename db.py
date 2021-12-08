import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

data = os.environ.get("DB")
user = os.environ.get("DB_USER")
host = os.environ.get("DB_HOST")
password = os.environ.get("DB_PASS")
port = os.environ.get("DB_PORT")

db = None

try: 
    db = psycopg2.connect(
        host=host, 
        database=data,
        user=user,
        password=password,
        port=port
    )
    print("Connection Successfully!")

except Exception as error:
    print("Error Message: " + error)

# finally:
#     if db is not None:
#         db.close()

# conn_string = f"dbname='{data}' user='{user}' host='{host}' password='{password}'"

# db = psycopg2.connect(conn_string)

# # print("Connecting to database ... ")

# # cursor = conn.cursor()
# print("Connected!\n")
