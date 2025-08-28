import mysql.connector

def get_connection(database=None):
    if database:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=database
        )
    else:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )