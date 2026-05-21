

import mysql.connector
from mysql.connector import Error
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import DB_CONFIG


def get_connection():
    """
    Creates and returns a MySQL database connection.
    Returns the connection if successful, None if failed.
    """
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )

        if connection.is_connected():
            print(" Connected to MySQL:", DB_CONFIG["database"])
            return connection

    except Error as e:
        print(f" Connection failed: {e}")
        print(" Check: Is MySQL running? Is password correct in config.py?")
        return None


def close_connection(connection, cursor=None):
    
    try:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print(" Connection closed.")
    except Error as e:
        print(f"Error while closing: {e}")



if __name__ == "__main__":
    print("Testing database connection...")
    conn = get_connection()

    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db = cursor.fetchone()
        print(f" Active database: {db[0]}")
        close_connection(conn, cursor)