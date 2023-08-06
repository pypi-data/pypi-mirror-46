import logging
import datetime

INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR
DEBUG = logging.DEBUG


def load_file_as_iter(path):
    with open(path, "r+") as f:
        for i in f:
            yield i


def zprint(message):
    new_m = "|{}| {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message)
    print(new_m)


def get_logger(log_file):
    logger = logging.Logger("logger to {}".format(log_file))
    hdlr = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(levelname)s %(lineno)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    return logger


def log2file(message, logger, level=logging.INFO, verbose=False):
    new_m = "|{}| {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message)
    logger.log(level, new_m)
    if verbose: print(new_m)
