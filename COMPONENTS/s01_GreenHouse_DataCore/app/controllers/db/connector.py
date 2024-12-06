import mariadb
import sys
from fastapi import HTTPException, status

def get_con():
    try:
        conn = mariadb.connect(
            user="root",
            password="123456",
            host="mariadb",
            port=3306,
            database="db_greenhouse"
        )
        return conn
    except mariadb.Error as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error connecting to MariaDB Platform: {e}")


def db_info():
    # Query to get tables and columns
    result = ""
    try:
        conn = get_con()
        cur = conn.cursor()
        # Get all tables in the database
        cur.execute("SHOW TABLES")
        tables = cur.fetchall()

        # Iterate over each table to get columns
        for (table_name,) in tables:
            result = result + f"Table: {table_name}\n"
            
            # Get columns for the current table
            cur.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = cur.fetchall()
            
            # Print column details
            for column in columns:
                column_name = column[0]
                column_type = column[1]
                result = result + f"  Column: {column_name} - Type: {column_type}\n"
        conn.close()
        return result
        
    except mariadb.Error as e:
        print(f"Error retrieving table information: {e}")


