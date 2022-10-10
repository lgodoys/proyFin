import logging
import logging.handlers

class PreProduction:
    #LOG_LEVEL=logging.DEBUG
    LOG_LEVEL=logging.INFO
    path_lib_dir='lib'

    ###############         DB          ###############
    SQL_HOST= "127.0.0.1"
    SQL_USER = "leonardo"
    SQL_PASS = "wuhy0%e!eog^@2wIiBD0wPk&2bOp4Lf&z4"
    SQL_DB = "estacionamientos"

    ##############      CONSTANTES      ###############
    VALOR_MINUTO = 15
