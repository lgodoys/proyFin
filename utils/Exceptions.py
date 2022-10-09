import logging
import sys
import os

dirpath = os.path.dirname(os.path.abspath(__file__))
parentPath = os.path.join(dirpath, os.pardir)

def logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler(parentPath+'/logs/'+name+'.log', mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    #logger.addHandler(screen_handler)
    return logger