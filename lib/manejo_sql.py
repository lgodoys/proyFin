import mysql.connector as mysql
from mysql.connector import Error

#Definimos clase base para manejo de Base de Datos MySQL. Se definen todas las funciones básicas necesarias
class BaseDatosMySQL:
    # Método __init__ para inicializar parámetros y generar la conexión a la BD
    def __init__(self, direccion=None, baseDeDatos=None, usuario=None, password=None):
        self.error=None
        self.conexion = None
        self.cursor = None
        self.errorConexion = None
        try: 
            self.conexion = mysql.connect(host=direccion, database=baseDeDatos, user=usuario, password=password)
            self.cursor = self.conexion.cursor()
        except:
            self.errorConexion = "No se pudo conectar a la base de datos"
    
    # Método para validar la conexión: Comprueba si está conectada la base de datos
    def isConnected(self):
        isConnected = False
        if(self.conexion is not None):
            isConnected = self.conexion.is_connected()
        return isConnected

    # Metodo para cerrar la conexión: Cierra la conexión con la base de datos
    def cerrarConexion(self):
        error = None
        try:
            self.cursor.close()
            self.conexion.close()
        except:
            error = "Error, falló el cierre de la conexión a la base de datos"
        return error
    
    # Método para crear/borrar base de datos: Ejecuta una consulta para crear/borrar una base de datos, retorna el resultado de la creación de la base de datos
    def crearBaseDatos(self,creacion):
        errorSQL = None
        registrosSQL = ""
        try:
            self.cursor.execute(creacion)
            self.cursor.execute("SHOW DATABASES;")
            try:
                registrosSQL = self.cursor.fetchall()
            except Exception as err:
                errorSQL = "Error al extraer datos por %s"%(str(err))
        except Exception as err:
            errorSQL = "Error, problema de ejecución en la consulta MySQL por: %s"%(str(err))

        return registrosSQL, errorSQL

    # Método para consultar una base de datos: Ejecuta una consulta que es entregada en la entrada, retorna el resultado de la consulta
    def seleccionarRegistros(self,consulta):
        errorSQL = None
        registrosSQL = ""
        try:
            self.cursor.execute(consulta)
            try:
                registrosSQL = self.cursor.fetchall()
            except Exception as err:
                errorSQL = "Error al extraer datos por %s"%(str(err))
        except Exception as err:
            errorSQL = "Error, problema de ejecución en la consulta MySQL por %s"%(str(err))

        return registrosSQL, errorSQL

    # Método para insertar datos: Ejecuta script para guardar datos y retorna estado y mensaje de la consulta
    def guardarDatos(self, consulta):
        error = None
        mensaje = ""
        estado = True
        try:
            self.cursor.execute(consulta)
            self.conexion.commit()
            if(self.cursor.rowcount >= 1):
                mensaje = "Se guardó exitosamente"
            else:
                error = "Error al guardar datos"
                estado = False
        except Exception as err:
            estado = False
            error = 'Error, problema de ejecución en la consulta de guardar en base de datos: %s'%(str(err))
        return mensaje, estado, error

    # Método para borrar datos: Ejecuta script para borrar datos y retorna el número de registros afectados
    def borraDatos(self,consulta):
        error = None
        mensaje = ""
        estado = True
        try:
            self.cursor.execute(consulta)
            self.conexion.commit()
            mensaje = f"Numero de registros afectados: {self.cursor.rowcount}"
        except Exception as err:
            estado = False
            error = 'Error, problema de ejecución en la consulta de borrar en base de datos: %s'%(str(err))
        return mensaje, estado, error

    # Método para actualizar datos: Ejecuta script para actualizar datos, retorna estado y mensaje de la consulta
    def updateDatos(self,consulta):
        error = None
        mensaje = ""
        estado = True
        try:
            self.cursor.execute(consulta)
            self.cursor.execute("SELECT ROW_COUNT() as rowcount")
            rows = self.cursor.fetchall()
            rowcount = rows[0][0]
            if rowcount > 0:
                self.conexion.commit()
                mensaje = "Se actualizó exitosamente"
            else:
                estado = False
                mensaje = "No se pudo actualizar"
                error = "Error, problema de ejecución en la consulta"
        except Exception as err:
            estado = False
            error = "Error, problema de ejecución en la actualización de la base de datos por %s"%(str(err))
        return mensaje, estado, error