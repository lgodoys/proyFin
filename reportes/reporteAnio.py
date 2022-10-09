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

"""PARA OBTENER REPORTES ANUALES, USAR LA SIGUIENTE QUERY:

SELECT SUM(valor) as Total, year(from_unixtime(floor(hora_salida))) AS AÑO FROM cobros GROUP BY AÑO;"""


def reporteAnual(year):
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
        consultaSQL = f"SELECT SUM(valor) as Total, year(from_unixtime(floor(hora_salida))) AS AÑO FROM cobros WHERE AÑO='{year}' GROUP BY AÑO;'"
        errorMySQL, datosEntregadosMySQL = consultaDBSQL(consultaSQL, dbSQL)
    return datosEntregadosMySQL, errorMySQL