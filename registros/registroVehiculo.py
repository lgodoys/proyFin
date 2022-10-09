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

"""PARA REGISTRAR NUEVOS VEHICULOS, USAR LA SIGUIENTE QUERY:

INSERT INTO vehiculos (idvehiculos,placa) VALUES (idvehiculo,placa);"""

def registroAuto(direccion,placa):
    """Función que permite insertar en la tabla VEHICULOS de la BD
    un nuevo vehiculo.
    Requiere 2 parámetros, direccion y placa.
    Retorna tres parámetros de la base de datos:
    - respuestaMySQL: la respuesta que genera la clase cuando cierra la escritura
    - estado: False o True. Si es False es porque finalizó con exito la escritura
    - errorMySQL: el mensaje de error que retorna MySQL Server en caso de problemas.
    Obtiene el ID del edificio y el ID del vehiculo desde la direccion y la placa"""
    errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL()
    if errorSQL is not None:
        LOGGER.warning("Error: Se produjo un error al conectar a la base de datos: %s"%(str(errorSQL)))
    else:
        consultaSQL = f"SELECT idedificios FROM edificios WHERE direccion='{direccion}'"
        errorMySQL, datosEntregadosMySQL = consultaDBSQL(consultaSQL, dbSQL)
        if errorMySQL is None:
            if(len(datosEntregadosMySQL)>0):
                idEdificio = datosEntregadosMySQL[0][0]
                idVehiculo = idEdificio[0:3]+placa[3:6]
                errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL()
                if errorSQL is not None:
                    LOGGER.warning("Error: Se produjo un error al conectar a la base de datos: %s"%(str(errorSQL)))
                else:
                    consultaSQL = f"INSERT INTO vehiculos (idvehiculos,placa) VALUES ('{idVehiculo}','{placa}');"
                    respuestaMySQL, estado, errorMySQL = insertarDatosSQL(consultaSQL,dbSQL)
                    if errorMySQL is None:
                        LOGGER.info(respuestaMySQL)
                    else:
                        LOGGER.warning(errorMySQL)
    return respuestaMySQL, estado, errorMySQL
