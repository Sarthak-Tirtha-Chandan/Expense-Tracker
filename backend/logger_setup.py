import logging

def setup_logger(name, filename = 'server.log' ,level = logging.DEBUG):

    logger = logging.getLogger(name)

    logger.setLevel(level)
    FileHandler = logging.FileHandler(filename)
    Formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    FileHandler.setFormatter(Formatter)
    logger.addHandler(FileHandler)

    return logger
