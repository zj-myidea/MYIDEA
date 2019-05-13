import logging
def getlogger(name,path):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    fhandle = logging.FileHandler(path)
    fmt = '%(asctime)s  %(moudle)s  %(funcName)s  %(message)s'
    fhandle.setFormatter(fmt)
    fhandle.setLevel(logging.INFO)
    logger.addHandler(fhandle)
    return logger
