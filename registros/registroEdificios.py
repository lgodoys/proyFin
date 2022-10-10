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

"""PARA REGISTRAR NUEVOS EDIFICIOS, USAR LA SIGUIENTE QUERY:

INSERT INTO edificios (idedificio,direccion,contacto,telefono) VALUES (idedificio,direccion,contacto,telefono);"""

def registroEdificio(direccion,contacto,telefono):
    """Función que permite insertar en la tabla EDIFICIOS de la BD
    cuando un vehiculo sale del estacionamiento, para generar el cobro
    Requiere 3 parámetros, direccion, contacto y telefono.
    Retorna tres parámetros de la base de datos:
    - respuestaMySQL: la respuesta que genera la clase cuando cierra la escritura
    - estado: False o True. Si es False es porque finalizó con exito la escritura
    - errorMySQL: el mensaje de error que retorna MySQL Server en caso de problemas.
    Genera el ID Edificio con los 3 primeros y 3 ultimos caracteres de la direccion"""
    idedificio=direccion[0:3].upper()+direccion[-3]+direccion[-2]+direccion[-1]
    errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL()
    if errorSQL is not None:
        LOGGER.warning("Error: Se produjo un error al conectar a la base de datos: %s"%(str(errorSQL)))
    else:
        consultaSQL = f"INSERT INTO edificios (idedificios,direccion,contacto,telefono) VALUES ('{idedificio}','{direccion}','{contacto}','{telefono}');"
        respuestaMySQL, estado, errorMySQL = insertarDatosSQL(consultaSQL,dbSQL)
        if errorMySQL is None or not estado:
            LOGGER.info(respuestaMySQL)
        else:
            LOGGER.warning(errorMySQL)
    return respuestaMySQL, estado, errorMySQL