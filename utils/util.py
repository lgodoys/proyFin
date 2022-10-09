# encoding: utf-8
import logging
from datetime import *
import os

#librerías locales
from lib.manejo_sql import *
from environment import app_config
from utils.Exceptions import *

env = os.getenv('INT_ENV', default='dev')
logging.info("env: %s"%(env))
config = app_config[env]

# Fuera de la clase, se configuran los métodos para levantar la conexión a la BD.
def llamadaBDMySQL():
    errorSQL = None
    ipBD = config.SQL_HOST
    nombreBD = config.SQL_DB
    usuarioBD = config.SQL_USER
    passwordBD = config.SQL_PASS
    dbSQL = BaseDatosMySQL(ipBD, nombreBD, usuarioBD, passwordBD)
    isConnectedSQL = dbSQL.isConnected()
    if not isConnectedSQL:
        errorSQL = "No está conectado a MySQL..."
        print("Error: no se pudo conectar a la base de datos MySQL.")
    return errorSQL, isConnectedSQL, dbSQL

# Método para crear una base de datos. Hace uso de la función correspondiente en la clase BaseDatosMySQL
def crearDBSQL(consultaEjecutar,db):
    errorMySQL = None
    datosEntregadosMySQL = []
    datosEntregadosMySQL, errorMySQL = db.crearBaseDatos(consultaEjecutar)
    if errorMySQL is None:
        errorMySQL = db.cerrarConexion()
    else:
        print("Error: error en ejecución de creación de base de datos MySQL: %s"%(str(errorMySQL)))
    return errorMySQL, datosEntregadosMySQL

# Método para crear una Tabla en la base de datos. Hace uso de la función correspondiente en la clase BaseDatosMySQL
def crearTablaDBSQL(consultaEjecutar,db):
    errorMySQL = None
    datosEntregadosMySQL = []
    datosEntregadosMySQL, errorMySQL = db.seleccionarRegistros(consultaEjecutar)
    if errorMySQL is None:
        errorMySQL = db.cerrarConexion()
    else:
        print("Error: error en ejecución de creación de tabla en base de datos: %s"%(str(errorMySQL)))
    return errorMySQL, datosEntregadosMySQL

# Método para consultar en la base de datos. Hace uso de la función correspondiente en la clase BaseDatosMySQL
def consultaDBSQL(consultaEjecutar,db):
    errorMySQL = None
    datosEntregadosMySQL = []
    datosEntregadosMySQL, errorMySQL = db.seleccionarRegistros(consultaEjecutar)
    if errorMySQL is None:
        errorMySQL = db.cerrarConexion()
    else:
        print("Error: error en ejecución ed consulta a base de datos MySQL: %s"%(str(errorMySQL)))
    return errorMySQL, datosEntregadosMySQL

# Método para insertar datos en la base de datos. Hace uso de la función correspondiente en la clase BaseDatosMySQL
def insertarDatosSQL(consultaEjecutar, db):
    error = None
    mensaje = None
    mensaje, estado, error = db.guardarDatos(consultaEjecutar)
    if error is None:
        error = db.cerrarConexion()
    else:
        print("Error en guardar datos en base de datos MySQL: %s"%(str(error)))
    return mensaje,estado,error

# Método para borrar datos en la base de datos. Hace uso de la función correspondiente en la clase BaseDatosMySQL
def borrarDatosSQL(consultaEjecutar,db):
    error = None
    mensaje = None
    mensaje, estado, error = db.borraDatos(consultaEjecutar)
    if error is None:
        error = db.cerrarConexion()
    else:
        print("Error en borrar datos en base de datos MySQL: %s"%(str(error)))
    return mensaje, estado, error

# Método para actualizar datos en la base de datos. Hace uso de la función correspondiente en la clase BaseDatosMySQL
def actualizarDatosSQL(consultaEjecutar,db):
    error = None
    mensaje = None
    mensaje, estado, error = db.updateDatos(consultaEjecutar)
    if error is None:
        error = db.cerrarConexion()
    else:
        print("Error en actualizar datos en base de datos MySQL: %s"%(error))
    return mensaje, estado, error
