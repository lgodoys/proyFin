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

SELECT ROUND(SUM((hora_salida-hora_entrada)/60/60)) as tiempoEstadia, vehiculos_idvehiculos from cobros GROUP BY vehiculos_idvehiculos;"""

def reporteEstadia():
    """Función que permite generar un reporte de estadía para todos los vehiculos
    No requiere parámetros
    Retorna dos parámetros de la base de datos:
    - datosEntregadosMySQL: la respuesta que genera la clase cuando cierra la consulta
    - errorMySQL: el mensaje de error que retorna MySQL Server en caso de problemas."""
    errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL()
    if errorSQL is not None:
        LOGGER.warning("Error: Se produjo un error al conectar a la base de datos: %s"%(str(errorSQL)))
    else:
        consultaSQL = f"SELECT ROUND(SUM((hora_salida-hora_entrada)/60/60)) as tiempoEstadiaEnHoras, vehiculos_idvehiculos from cobros GROUP BY vehiculos_idvehiculos;;'"
        errorMySQL, datosEntregadosMySQL = consultaDBSQL(consultaSQL, dbSQL)
    return datosEntregadosMySQL, errorMySQL