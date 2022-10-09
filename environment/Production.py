import logging
import logging.handlers

class Production:
    #LOG_LEVEL=logging.DEBUG
    LOG_LEVEL=logging.INFO
    path_lib_dir='lib'


    ###############    Email Info   ##############
    EMAIL_TO_SLEEPING_CELL="leonardo.godoy@estudiantes.iacc.cl"

    ###############       DB       ###############
    #DB LAB
    SQL_HOST_NOC = "127.0.0.1"
    SQL_USER_NOC = "leonardo"
    SQL_PASS_NOC = "W4rw1ck.2022365"
    SQL_DB_NOC = "estacionamientos"
