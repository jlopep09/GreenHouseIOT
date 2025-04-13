import mariadb
from fastapi import HTTPException, status
import os

def get_con():
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("USER:", os.getenv("DB_USER"))
        print("PASSWORD:", os.getenv("DB_PASSWORD"))
        print("HOST:", os.getenv("DB_HOST"))
        print("PORT:", os.getenv("DB_PORT"))
        print("DATABASE:", os.getenv("DB_NAME"))
        conn = mariadb.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            database=os.getenv("DB_NAME")
        )
        return conn
    except mariadb.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = f"Error connecting to MariaDB Platform: {e}. Check db url host:{os.getenv('DB_HOST')}"
        )

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


