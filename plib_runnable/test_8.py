import os
import logging
from logging.handlers import RotatingFileHandler
# from loguru import logger as loguru_logger
# from converge import settings



def build_app_logger(name='app', logfile='app.log', debug=True):
    """
    General purpose application logger. Useful mainly for debugging
    """
    # level = logging.DEBUG if settings.DEBUG else logging.INFO
    level = logging.INFO
    
    logdir = './logs'  # TODO: move this to settings
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    logpath = os.path.join(logdir, logfile)
    maxBytes = 1024 * 1024 * 10
    handler = RotatingFileHandler(logpath, maxBytes=maxBytes, backupCount=100)
    handler.setLevel(level)
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s: %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger



def test_build_app_logger():
    """Check the correctness of build_app_logger
    """
    
    app_logger = build_app_logger()
    assert app_logger.level == logging.INFO
    assert app_logger.handlers[0].level == logging.INFO
    assert app_logger.handlers[0].formatter.datefmt == None