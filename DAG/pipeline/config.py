import logging

USERNAME = 'zhoujing'
PASSWORD = '123'
DBIP = '192.168.91.128'
DBPORT = 3306
DBNAME = 'pipeline'

URL = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{DBIP}:{DBPORT}/{DBNAME}'

DATABASE_DEBUG = True


def getlogger(name, filepath):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handle = logging.FileHandler(filename=name)
    handle.setLevel(logging.INFO)
    fmt = logging.Formatter('%(asctime)s %(module)s %(funcName)s  %(message)s')
    handle.setFormatter(fmt)
    logger.addHandler(handle)
    return logger









