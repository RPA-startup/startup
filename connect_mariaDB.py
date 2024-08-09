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
        # Cursor 생성
        cur = conn.cursor()
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return conn, cur

def get_data(cur):
    # Retrieving all rows from the table
    try:
        cur.execute(f"SELECT * FROM {config.DB_Info['table']}") 
        resultset = cur.fetchall()
    except mariadb.Error as e:
        print(f"Error executing query: {e}")
        return None
    return resultset

def disconnect_db(conn, cur):
    cur.close()
    conn.close()

# Main execution
if __name__ == "__main__":
    conn, cur = connect_db()
    rows = get_data(cur)
    
    if rows:
        for row in rows:
            print(row)
    
    disconnect_db(conn, cur)
