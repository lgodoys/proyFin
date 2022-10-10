from datetime import *
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from environment import app_config
from utils.Exceptions import *
from utils.util import *

LOGGER = logger('estacionamiento')

env = os.getenv('INT_ENV', default='dev')
logging.info("env: %s"%(env))
config = app_config[env]

"""PARA REGISTRAR NUEVOS ESPACIOS, USAR LA SIGUIENTE QUERY:

INSERT INTO espacios (idespacios,vehiculos_idvehiculos,edificios_idedificios) VALUES (idespacio,(SELECT idvehiculo FROM vehiculos WHERE placa = '{placa}'),(SELECT idedificio FROM edificios WHERE direccion='{direccion}');"""

def registroEspacio(idespacio,direccion):
    """Función que permite insertar en la tabla ESPACIOS de la BD
    un nuevo espacio administrado
    Requiere 3 parámetros, idespacio, placa y direccion.
    Retorna tres parámetros de la base de datos:
    - respuestaMySQL: la respuesta que genera la clase cuando cierra la escritura
    - estado: False o True. Si es False es porque finalizó con exito la escritura
    - errorMySQL: el mensaje de error que retorna MySQL Server en caso de problemas.
    Obtiene el ID del edificio y el ID del vehiculo desde la direccion y la placa"""
    errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL()
    if errorSQL is not None:
        LOGGER.warning("Error: Se produjo un error al conectar a la base de datos: %s"%(str(errorSQL)))
    else:
        consultaSQL = f"INSERT INTO espacios (idespacios,edificios_idedificios) VALUES ({idespacio},(SELECT idedificios FROM edificios WHERE direccion='{direccion}'));"
        respuestaMySQL, estado, errorMySQL = insertarDatosSQL(consultaSQL,dbSQL)
        if errorMySQL is None or not estado:
            LOGGER.info(respuestaMySQL)
        else:
            LOGGER.warning(errorMySQL)
    return respuestaMySQL, estado, errorMySQL
