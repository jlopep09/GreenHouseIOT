import app.controllers.db.connector as connector
import mariadb
from fastapi import HTTPException, status
from numpy import interp
import app.const as const

def create_img(image: bytes):
    try:
        conn = connector.get_con()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO images (image) VALUES (%s)",
            (image,)  # ✅ Asegurar que es una tupla (con la coma final)
        )

        conn.commit()
        img_id = cur.lastrowid
        conn.close()
        return {"message": "Image saved successfully", "id": img_id}

    except mariadb.Error as e:
        print(f"Error de MariaDB: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving image: {str(e)}")

def get_greenhouse_by_name(name: str):
    ghs = []
    try:
        conn = connector.get_con()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM greenhouses WHERE name=?", (name,)) 
        columns = [col[0] for col in cur.description]  # Obtener nombres de las columnas
        for row in cur.fetchall():
            gh = dict(zip(columns, row))  # Combina nombres de columnas con valores
            ghs.append(gh)

        conn.close()
        return {"result": ghs}
        
    except mariadb.Error as e:
        print(f"Error retrieving table information: {e}")

def get_greenhouses(user_auth0_id: str):
    greenhouses = []
    try:
        conn = connector.get_con()
        cur = conn.cursor()

        cur.execute("SELECT * FROM greenhouses WHERE owner_id = ?", (user_auth0_id,))
        columns = [col[0] for col in cur.description]  # Obtener nombres de las columnas

        for row in cur.fetchall():
            greenhouse = dict(zip(columns, row))  # Combina nombres de columnas con valores
            greenhouses.append(greenhouse)

        conn.close()
        return {"greenhouses": greenhouses}  # Devuelve como JSON
        
    except mariadb.Error as e:
        print(f"Error retrieving greenhouses for user {user_auth0_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve greenhouses")

def get_reads(user_auth0_id:str):
    print("Obteniendo lecturas del userautid ")
    print(user_auth0_id)
    reads = []
    try:
        print("Lecturas: check 1 ")
        conn = connector.get_con()
        cur = conn.cursor()
        print("Lecturas: check 2 ")
        # 1) Recuperar los IDs de los invernaderos de este usuario
        cur.execute("SELECT id FROM greenhouses WHERE owner_id = ?", (user_auth0_id,))
        print("Lecturas: check 3 ")
        gh_ids = [row[0] for row in cur.fetchall()]
        print("Lecturas: check 4 ")

        # Si no tiene invernaderos, devolvemos lista vacía
        if not gh_ids:
            conn.close()
            return {"reads": []}
        print("Lecturas: check 5 ")
        # 2) Construir la consulta dinámica con placeholders para IN (...)
        placeholders = ",".join(["?"] * len(gh_ids))
        sql = f"SELECT * FROM sensor_reads WHERE gh_id IN ({placeholders})"
        cur.execute(sql, gh_ids)
        print("Lecturas: check 6 ")

        # 3) Mapear columnas a diccionarios
        columns = [col[0] for col in cur.description]
        for row in cur.fetchall():
            reads.append(dict(zip(columns, row)))
        print("Lecturas: check 7 ")
        conn.close()
        return {"reads": reads}

    except mariadb.Error as e:
        print(f"Error retrieving reads for user {user_auth0_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve reads")
    
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

def create_greenhouse( name: str, ip: str,sync_code: str, description: str= None, image: bytes = None):
    try:
        conn = connector.get_con()
        cur = conn.cursor()
        
        # Inserta un nuevo registro en la tabla `greenhouses`
        cur.execute(
            "INSERT INTO greenhouses (name, description, image, ip, sync_code) VALUES (?, ?, ?, ?, ?)",
            (name, description, image, ip, sync_code)
        )
        
        # Confirma los cambios
        conn.commit()
        
        # Obtén el ID del nuevo registro insertado
        greenhouse_id = cur.lastrowid
        
        conn.close()
        
        return {"message": "Greenhouse created successfully", "id": greenhouse_id}
        
    except mariadb.Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating greenhouse: {e}")
def sync_greenhouse(name: str, sync_code: str, owner_id: str):
    try:
        conn = connector.get_con()
        cur = conn.cursor()

        # Verifica si el invernadero existe y obtiene el sync_code actual
        cur.execute("SELECT id, sync_code FROM greenhouses WHERE name = ?", (name,))
        result = cur.fetchone()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Greenhouse with name '{name}' not found"
            )

        _, current_sync_code = result

        # Si ya tiene un sync_code asignado, lanza excepción
        if current_sync_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Greenhouse already synced"
            )
        if current_sync_code!=sync_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Greenhouse sync code is not valid"
            )

        # Si no tiene sync_code, actualiza el owner_id
        cur.execute(
            """
            UPDATE greenhouses
            SET owner_id = ?
            WHERE name = ?
            """,
            (owner_id, name)
        )

        conn.commit()
        conn.close()

        return {"message": "Greenhouse updated successfully", "name": name}
    
    except Exception as e:
        # Cierra conexión si algo sale mal
        if conn:
            conn.close()
        raise e
    
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