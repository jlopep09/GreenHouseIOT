from fastapi import APIRouter, HTTPException, Header
import app.controllers.db.connector as connector
import app.controllers.db.db_queries as db_queries
import mariadb

router = APIRouter(tags=["MariaDB"],prefix="/db")

def get_ghconfigs(user_auth0_id:str):
    print("Obteniendo configuraciones de gh del userautid ")
    print(user_auth0_id)
    configs = []
    try:
        conn = connector.get_con()
        cur = conn.cursor()
        # 1) Recuperar los IDs de los invernaderos de este usuario
        cur.execute("SELECT id FROM greenhouses WHERE owner_id = ?", (user_auth0_id,))
        gh_ids = [row[0] for row in cur.fetchall()]
        # Si no tiene invernaderos, devolvemos lista vacía
        if not gh_ids:
            conn.close()
            return {"configs": []}
        # 2) Construir la consulta dinámica con placeholders para IN (...)
        placeholders = ",".join(["?"] * len(gh_ids))
        sql = f"SELECT * FROM actuators WHERE gh_id IN ({placeholders})"
        cur.execute(sql, gh_ids)

        # 3) Mapear columnas a diccionarios
        columns = [col[0] for col in cur.description]
        for row in cur.fetchall():
            configs.append(dict(zip(columns, row)))
        conn.close()
        return {"configs": configs}

    except mariadb.Error as e:
        print(f"Error retrieving configs for user {user_auth0_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve reads")
def create_ghconfig(user_auth0_id: str, actuator_data: dict):
    print(f"Creando nueva configuración de actuador para usuario {user_auth0_id}")
    try:
        conn = connector.get_con()
        cur = conn.cursor()
        
        # 1) Verificar que el invernadero pertenece al usuario
        cur.execute("SELECT id FROM greenhouses WHERE id = ? AND owner_id = ?", 
                   (actuator_data['gh_id'], user_auth0_id))
        gh = cur.fetchone()
        
        if not gh:
            conn.close()
            raise HTTPException(status_code=403, detail="No tienes permiso para modificar este invernadero")
        
        # 2) Insertar el nuevo actuador
        sql = """
            INSERT INTO actuators 
            (name, auto, timer_on, timer_off, manual_status, gh_id) 
            VALUES (?, ?, ?, ?, ?, ?)
        """
        
        # Valores por defecto si no se proporcionan
        auto = actuator_data.get('auto', False)
        timer_on = actuator_data.get('timer_on', '09:00:00')
        timer_off = actuator_data.get('timer_off', '14:00:00')
        manual_status = actuator_data.get('manual_status', False)
        
        # Convertir booleanos a bits
        auto_bit = 1 if auto else 0
        manual_status_bit = 1 if manual_status else 0
        
        cur.execute(sql, (
            actuator_data['name'],
            auto_bit,
            timer_on,
            timer_off,
            manual_status_bit,
            actuator_data['gh_id']
        ))
        
        # Obtener el ID del actuador insertado
        actuator_id = cur.lastrowid
        
        # Confirmar cambios
        conn.commit()
        conn.close()
        
        return {
            "id": actuator_id,
            "message": "Actuador creado exitosamente",
            "actuator": {
                "id": actuator_id,
                "name": actuator_data['name'],
                "auto": auto,
                "timer_on": timer_on,
                "timer_off": timer_off,
                "manual_status": manual_status,
                "gh_id": actuator_data['gh_id']
            }
        }
        
    except mariadb.Error as e:
        print(f"Error al crear configuración: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear configuración: {str(e)}")

"""
    ROUTER ENDPOINTS
"""
@router.get("/reads/")
async def get_all_reads(user_auth0_id: str = Header(..., alias="UserAuth")):
    return (db_queries.get_reads(user_auth0_id))
   
@router.get("/ghconfig/")
async def get_all_reads(user_auth0_id: str = Header(..., alias="UserAuth")):
    return get_ghconfigs(user_auth0_id)
  
@router.get("/reads/{id}")
async def get_reads_from_greenhouse_id(id: int):
    return (db_queries.get_reads_byid(id))

@router.post("/ghconfig/")
async def create_actuator_config(
    actuator_data: dict, 
    user_auth0_id: str = Header(..., alias="UserAuth")
):
    # Validación básica de datos
    required_fields = ['name', 'gh_id']
    for field in required_fields:
        if field not in actuator_data:
            raise HTTPException(status_code=400, detail=f"Campo requerido faltante: {field}")
    
    # Validar que el nombre del actuador sea uno de los valores permitidos
    allowed_names = ['pump', 'fan', 'light', 'oxigen']
    if actuator_data['name'] not in allowed_names:
        raise HTTPException(
            status_code=400, 
            detail=f"Nombre de actuador inválido. Valores permitidos: {', '.join(allowed_names)}"
        )
    
    return create_ghconfig(user_auth0_id, actuator_data)