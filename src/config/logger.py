import logging

# create logger
logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('./logs/verge.log')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s - %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')

fh.setFormatter(formatter)

logger.addHandler(fh)