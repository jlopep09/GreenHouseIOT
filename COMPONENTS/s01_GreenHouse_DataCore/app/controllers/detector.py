
from app.controllers.db.db_queries import create_greenhouse, update_greenhouse_ip, get_greenhouse_by_name

class Detector():

    def checkIP(gh_name: str, gh_ip: str) -> bool:
        #llamar a db para obtener gh_ip de gh_name
        db_result = get_greenhouse_by_name(gh_name)
        print(db_result)
        if(db_result["result"]==[]):
            print("No se ha encontrado gh con el nombre {gh_name}, creando nueva entrada en la base de datos...")
            query_result = create_greenhouse(name = gh_name, ip = gh_ip)
            print("Invernadero creado correctamente.")
            return False
        
        #comprobar si la ip almacenada es la misma
        if(not db_result["result"][0]["ip"]==gh_ip):
            ip_anterior =  db_result["result"][0]["ip"]
            #print("Se ha detectado un cambio de ip, ip actual: {gh_ip}, ip anterior: {ip_anterior}")
            print("Se ha detectado un cambio de ip, actualizando base de datos...")
            update_greenhouse_ip(gh_name, gh_ip)
            #si no es la misma modificarla
        return False #no necesita cambio

