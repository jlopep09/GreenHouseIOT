import mariadb
from fastapi import HTTPException, status
import os
from dotenv import load_dotenv

def get_con():
    try:
        # Cargar variables de entorno
        load_dotenv()

        # Comprobar si todas las variables necesarias existen
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")

        # Si alguna variable falta, lanzar un error HTTP con el mismo mensaje
        if not all([db_user, db_password, db_host, db_port, db_name]):
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail="Missing one or more required environment variables"
            )

        # Establecer la conexión a la base de datos
        conn = mariadb.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            port=int(db_port or 3306),
            database=db_name
        )
        return conn

    except mariadb.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error connecting to MariaDB Platform: {e}"
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


