import mariadb
import sys
import config

# Connect to MariaDB Platform
def connect_db():
    try:
        conn = mariadb.connect(
            user=config.DB_Info["user"],
            password=config.DB_Info["password"],
            host=config.DB_Info["host"],
            port=config.DB_Info["port"],
            database=config.DB_Info["database"]

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return conn

def get_data(cur):
    #retrieving information
    cur.execute("SELECT * FROM " + config.DB_Info["table"]) 
    resultset = cur.fetchall()
    return resultset

def disconnect_db(conn):
    conn.close()