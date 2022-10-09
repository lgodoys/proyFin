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

SELECT SUM(valor) as Total, month(from_unixtime(floor(hora_salida))) AS MES FROM cobros GROUP BY MES;"""

def reporteDiario(dia):
    """Función que permite generar un reporte diario.
    Requiere 1 parámetro, el día
    Retorna dos parámetros de la base de datos:
    - datosEntregadosMySQL: la respuesta que genera la clase cuando cierra la consulta
    - errorMySQL: el mensaje de error que retorna MySQL Server en caso de problemas."""
    errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL()
    if errorSQL is not None:
        LOGGER.warning("Error: Se produjo un error al conectar a la base de datos: %s"%(str(errorSQL)))
    else:
        consultaSQL = f"SELECT SUM(valor) as Total, day(from_unixtime(floor(hora_salida))) AS DIA FROM cobros WHERE DIA='{dia}' GROUP BY DIA;'"
        errorMySQL, datosEntregadosMySQL = consultaDBSQL(consultaSQL, dbSQL)
    return datosEntregadosMySQL, errorMySQL