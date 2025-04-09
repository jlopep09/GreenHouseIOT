import app.controllers.db.connector as connector
import app.controllers.db.db_queries as db_queries


def get_db_info():
    return connector.db_info()


def get_all_greenhouses_info():
    return db_queries.get_greenhouses()



def get_all_reads():
    return db_queries.get_reads()
   


def get_greenhouse_info_by_id(id: int):
    return db_queries.get_greenhouse(id)
def get_greenhouse_info_by_name(name: str):
    return db_queries.get_greenhouse_by_name(name)



def get_reads_from_greenhouse_id(id: int):
    return db_queries.get_reads_byid(id)