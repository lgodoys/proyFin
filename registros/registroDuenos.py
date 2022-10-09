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

"""PARA REGISTRAR NUEVOS DUEÑOS, USAR LA SIGUIENTE QUERY:

INSERT INTO dueños (rut,nombre,apellido,vehiculos_idvehiculos) 
VALUES (rut,nombre,apellido,SELECT idvehiculos FROM vehiculos WHERE placa='{placa}');"""

def registroDueno(rut,nombre,apellido,placa):
    """Función que permite insertar en la tabla DUEÑOS de la BD
    cuando se registra un nuevo dueño de vehiculo.
    Requiere 4 parámetros, RUT, Nombre, Apellido y Placa
    Retorna tres parámetros de la base de datos:
    - respuestaMySQL: la respuesta que genera la clase cuando cierra la escritura
    - estado: False o True. Si es False es porque finalizó con exito la escritura
    - errorMySQL: el mensaje de error que retorna MySQL Server en caso de problemas"""
    errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL()
    if errorSQL is not None:
        LOGGER.warning("Error: Se produjo un error al conectar a la base de datos: %s"%(str(errorSQL)))
    else:
        consultaSQL = f"INSERT INTO dueños (rut,nombre,apellido,vehiculos_idvehiculos) VALUES ('{rut}','{nombre}','{apellido}',(SELECT idvehiculos FROM vehiculos WHERE placa='{placa}'));"
        respuestaMySQL, estado, errorMySQL = insertarDatosSQL(consultaSQL,dbSQL)
        if errorMySQL is None or not estado:
            LOGGER.info(respuestaMySQL)
        else:
            LOGGER.warning(errorMySQL)
    return respuestaMySQL, estado, errorMySQL
