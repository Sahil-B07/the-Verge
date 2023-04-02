import logging

def config_logger():
    # create logger
    logger = logging.getLogger('root')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('/home/sahilr/the-Verge/logs/verge.log')
    fh.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s - %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')

    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger