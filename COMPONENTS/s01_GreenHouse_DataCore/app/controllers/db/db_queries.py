from sqlite3 import Binary
import app.controllers.db.connector as connector
import mariadb
from fastapi import HTTPException, status
from numpy import interp
import app.const as const

def create_img(image: bytes):
    try:
        conn = connector.get_con()
        cur = conn.cursor()

        # Inserta solo la imagen en la base de datos
        cur.execute(
            "INSERT INTO images (image) VALUES (%s)",
            (image,)  # ✅ Asegurar que es una tupla (con la coma final)
        )

        conn.commit()
        img_id = cur.lastrowid

        conn.close()

        return {"message": "Image saved successfully", "id": img_id}

    except mariadb.Error as e:
        print(f"Error de MariaDB: {e}")  # Para depuración
        raise HTTPException(status_code=500, detail=f"Error saving image: {str(e)}")


def get_greenhouse_by_name(name: str):
    ghs = []
    try:
        conn = connector.get_con()
        cur = conn.cursor()
        
        # Retrieving information
        cur.execute("SELECT * FROM greenhouses WHERE name=?", (name,)) 
        columns = [col[0] for col in cur.description]  # Obtener nombres de las columnas
        for row in cur.fetchall():
            gh = dict(zip(columns, row))  # Combina nombres de columnas con valores
            ghs.append(gh)

        conn.close()
        return {"result": ghs}
        
    except mariadb.Error as e:
        print(f"Error retrieving table information: {e}")
def get_greenhouses():
    greenhouses = []
    try:
        conn = connector.get_con()
        cur = conn.cursor()

        # retrieving information 
        cur.execute("SELECT * FROM greenhouses") 
        columns = [col[0] for col in cur.description]  # Obtener nombres de las columnas

        for row in cur.fetchall():
            greenhouse = dict(zip(columns, row))  # Combina nombres de columnas con valores
            greenhouses.append(greenhouse)

        conn.close()
        return {"greenhouses": greenhouses}  # Devuelve como JSON
        
    except mariadb.Error as e:
        print(f"Error retrieving table information: {e}")
        return {"error": "Failed to retrieve greenhouses"}

def get_reads():
    reads = []
    try:
        conn = connector.get_con()
        cur = conn.cursor()

        # retrieving information 
        cur.execute("SELECT * FROM sensor_reads") 
        columns = [col[0] for col in cur.description]  # Obtener nombres de las columnas
        for row in cur.fetchall():
            read = dict(zip(columns, row))  # Combina nombres de columnas con valores
            reads.append(read)

        conn.close()
        return {"reads": reads}  # Devuelve como JSON
        
    except mariadb.Error as e:
        print(f"Error retrieving table information: {e}")
        return {"error": "Failed to retrieve reads"}

def get_reads_byid(id: int):
    reads = []
    try:
        conn = connector.get_con()
        cur = conn.cursor()
        
        # Retrieving information
        cur.execute("SELECT * FROM sensor_reads WHERE gh_id=?", (id,))  # Asegúrate de que sea una tupla con (id,)
        columns = [col[0] for col in cur.description]  # Obtener nombres de las columnas
        for row in cur.fetchall():
            read = dict(zip(columns, row))  # Combina nombres de columnas con valores
            reads.append(read)

        conn.close()
        return {"reads": reads}
        
    except mariadb.Error as e:
        print(f"Error retrieving table information: {e}")

def get_greenhouse(id: int):

    # Query to get tables and columns
    result="" #= "id | date | name | description | img\n"
    try:
        conn = connector.get_con()
        cur = conn.cursor()
        #retrieving information 

        cur.execute("SELECT * FROM greenhouses WHERE id=?", (id,)) 
        gh_list = cur.fetchall()
        # Iterate over each table to get columns
        for entry in gh_list:  # Elimina la coma para desempaquetar toda la tupla
            result += " | ".join(str(value) for value in entry) + "\n"  # Une los valores con separadores
        conn.close()
        return result
        
    except mariadb.Error as e:
        print(f"Error retrieving table information: {e}")

def create_greenhouse( name: str, ip: str, description: str= None, image: bytes = None):
    try:
        conn = connector.get_con()
        cur = conn.cursor()
        
        # Inserta un nuevo registro en la tabla `greenhouses`
        cur.execute(
            "INSERT INTO greenhouses (name, description, image, ip) VALUES (?, ?, ?, ?)",
            (name, description, image, ip)
        )
        
        # Confirma los cambios
        conn.commit()
        
        # Obtén el ID del nuevo registro insertado
        greenhouse_id = cur.lastrowid
        
        conn.close()
        
        return {"message": "Greenhouse created successfully", "id": greenhouse_id}
        
    except mariadb.Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating greenhouse: {e}")
    
def update_greenhouse_ip(name: str, ip: str):
    try:
        conn = connector.get_con()
        cur = conn.cursor()

        # Verifica si el invernadero existe
        cur.execute("SELECT id FROM greenhouses WHERE name = ?", (name,))
        result = cur.fetchone()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Greenhouse with name '{name}' not found"
            )

        # Si existe, actualiza los valores
        cur.execute(
            """
            UPDATE greenhouses
            SET ip = ?
            WHERE name = ?
            """,
            (ip, name)
        )

        # Confirma los cambios
        conn.commit()
        conn.close()

        return {"message": "Greenhouse updated successfully", "name": name}

    except mariadb.Error as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating greenhouse: {e}"
        )

def create_read(tds: int, humidity: int, water_level: int, temperature: int, light_level: bool, water_temperature:float, gh_id:int):
    try:
        conn = connector.get_con()
        cur = conn.cursor()
        
        # Inserta un nuevo registro en la tabla `greenhouses`
        cur.execute(
            "INSERT INTO sensor_reads (tds, humidity, water_level, temperature, light_level, water_temperature, gh_id) VALUES (?, ?, ?, ?, ?, ?,?)",
            (tds, humidity, get_percentage(water_level, const.WATER_MIN_RANGE, const.WATER_MAX_RANGE), temperature, light_level,water_temperature, gh_id)
        )
        
        # Confirma los cambios
        conn.commit()
        
        # Obtén el ID del nuevo registro insertado
        read_id = cur.lastrowid
        
        conn.close()
        
        return {"message": "Read created successfully", "id": read_id}
        
    except mariadb.Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating read: {e}")
    
def get_percentage(value: int,min_range: int, top_range: int) -> int:
    return int(interp(value, [min_range, top_range], [0,100] ))