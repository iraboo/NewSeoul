import logging
from logging.handlers import RotatingFileHandler
import config

LOG_HOME = config.PROJECT_DIR

def get_logger(name):
    """
    :param name: Log file name
    :return: logger Object
    """
    logger = logging.getLogger(name)

    # Check handler exists
    if len(logger.handlers) > 0:
        return logger       # Logger already exists
        
    # DEBUG < INFO < WARNING < ERROR < CRITICAL
    logger.setLevel(logging.INFO)
    
    rotate_handler = RotatingFileHandler(LOG_HOME+"/"+name+".log", 'a', 1024*1024*5, 5)
    fomatter = logging.Formatter('[%(levelname)s-%(asctime)s-%(filename)s:%(lineno)s:%(funcName)s:%(message)s',
                                 datefmt="%Y-%m-%d %H:%M:%S")
    rotate_handler.setFormatter(fomatter)
    logger.addHandler(rotate_handler)
    return logger


