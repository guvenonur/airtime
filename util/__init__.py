import logging


def create_logger(msg):
    """
    :param str msg: logger name
    :return: logger
    :rtype: logger object
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger(msg)
