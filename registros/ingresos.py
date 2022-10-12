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


"""PARA REGISTRAR INGRESOS USAR LA SIGUIENTE QUERY

INSERT INTO cobros (idcobros,hora_entrada,vehiculos_idvehiculos,espacios_idespacios) VALUES (1,1665191196,(SELECT idvehiculos FROM vehiculos WHERE placa={placa}}),(SELECT idespacios FROM espacios WHERE vehiculos_idvehiculos=(SELECT idvehiculos from vehiculos where placa={placa}})));"""

def ingresoVehiculos(placa):
    """Función que permite insertar en la tabla COBROS de la BD
    cuando un vehiculo ingresa al estacionamiento.
    Requiere 1 parámetro, la placa patente.
    Retorna tres parámetros de la base de datos:
    - respuestaMySQL: la respuesta que genera la clase cuando cierra la escritura
    - estado: False o True. Si es False es porque finalizó con exito la escritura
    - errorMySQL: el mensaje de error que retorna MySQL Server en caso de problemas"""
    horaEntrada = int(datetime.strftime(datetime.now(),"%s"))
    errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL()
    if errorSQL is not None:
        LOGGER.warning("Error: Se produjo un error al conectar a la base de datos: %s"%(str(errorSQL)))
    else:
        consultaSQL = f"UPDATE espacios SET vehiculos_idvehiculos=(SELECT idvehiculos FROM vehiculos WHERE placa='{placa}') WHERE isnull(vehiculos_idvehiculos ORDER BY idespacios DESC LIMIT 1;"
        mensaje, estado, error = actualizarDatosSQL(consultaSQL,dbSQL)
        if error is None or not estado:
            errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL()
            if errorSQL is None:
                consultaSQL = f"INSERT INTO cobros (hora_entrada,vehiculos_idvehiculos,espacios_idespacios) VALUES ({horaEntrada},(SELECT idvehiculos FROM vehiculos WHERE placa='{placa}'),(SELECT idespacios FROM espacios WHERE vehiculos_idvehiculos=(SELECT idvehiculos FROM vehiculos WHERE placa='{placa}')));"
                respuestaMySQL, estado, errorMySQL = insertarDatosSQL(consultaSQL,dbSQL)
                if errorMySQL is None or not estado:
                    errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL()
                    if errorSQL is None:
                        consultaSQL = f"SELECT idcobros,hora_entrada,vehiculos_idvehiculos,espacios_idespacios FROM cobros WHERE vehiculos_idvehiculos=(SELECT idvehiculos FROM vehiculos WHERE placa='{placa}') ORDER BY hora_entrada DESC LIMIT 1;"
                        errorMySQL, datosEntregadosMySQL = consultaDBSQL(consultaSQL, dbSQL)
                        LOGGER.info(respuestaMySQL)
                else:
                    LOGGER.warning(errorMySQL)
            else:
                LOGGER.warning(errorMySQL)
        else:
            LOGGER.warning(errorMySQL)
    return datosEntregadosMySQL,errorMySQL
