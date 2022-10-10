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


"""PARA REGISTRAR UN COBRO, USAR LAS SIGUIENTES QUERYS:
SELECT hora_entrada from cobros WHERE vehiculos_idvehiculos=(SELECT idvehiculos FROM vehiculos WHERE placa='{placa}');

UPDATE cobros SET hora_salida={hora_salida},valor={valor} WHERE vehiculos_idvehiculos=(SELECT idvehiculos FROM vehiculos WHERE placa='{placa}}');
"""

def salida(placa):
    """Función que permite insertar en la tabla COBROS de la BD
    cuando un vehiculo sale del estacionamiento, para generar el cobro
    Requiere 1 parámetro, la placa patente.
    Retorna tres parámetros de la base de datos:
    - respuestaMySQL: la respuesta que genera la clase cuando cierra la escritura
    - estado: False o True. Si es False es porque finalizó con exito la escritura
    - errorMySQL: el mensaje de error que retorna MySQL Server en caso de problemas
    
    Primero realiza una consulta a la BD para obtener la hora de entrada, luego,
    calcula el tiempo de estadía y el valor en función de la hora de entrada y de salida
    y luego registra el dato en la tabla."""
    errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL()
    if errorSQL is not None:
        LOGGER.warning("Error: se produjo un error al conectar al motor de base de datos: %s"%(str(errorSQL)))
    else:
        consultaSQL = f"SELECT idcobros, hora_entrada from cobros WHERE vehiculos_idvehiculos=(SELECT idvehiculos FROM vehiculos WHERE placa='{placa}') ORDER BY hora_entrada DESC LIMIT 1;"
        errorMySQL, datosEntregadosMySQL = consultaDBSQL(consultaSQL, dbSQL)
        if errorMySQL is None:
            if(len(datosEntregadosMySQL)>0):
                idcobros = datosEntregadosMySQL[0][0]
                horaSalida = int(datetime.strftime(datetime.now(),"%s"))
                horaEntrada = datosEntregadosMySQL[0][1]
                tiempoUso = (horaSalida-horaEntrada)/60
                valor = config.VALOR_MINUTO*tiempoUso
                errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL()
                if errorSQL is not None:
                    LOGGER.warning("Error: Se produjo un error al conectar a la base de datos: %s"%(str(errorSQL)))
                else:
                    consultaSQL = f"UPDATE cobros SET hora_salida={horaSalida},valor={valor} WHERE idcobros={idcobros} AND vehiculos_idvehiculos=(SELECT idvehiculos FROM vehiculos WHERE placa='{placa}');"
                    respuestaMySQL, estado, errorMySQL = insertarDatosSQL(consultaSQL,dbSQL)
                    if errorMySQL is None or not estado:
                        errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL()
                        if errorSQL is None:
                            consultaSQL = f"SELECT idcobros,hora_entrada,hora_salida,valor,vehiculos_idvehiculos,espacios_idespacios FROM cobros WHERE vehiculos_idvehiculos=(SELECT idvehiculos FROM vehiculos WHERE placa='{placa}') ORDER BY hora_entrada DESC LIMIT 1;"
                            errorMySQL, datosEntregadosMySQL = consultaDBSQL(consultaSQL, dbSQL)
                    else:
                        LOGGER.warning(errorMySQL)
        else:
            LOGGER.warning(errorMySQL)
    return datosEntregadosMySQL, errorMySQL

