import logging


def create_logger(msg):
    """
    :param str msg: logger name
    :return: logger
    :rtype: logger object
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger(msg)


class Strings:
    @staticmethod
    def is_empty(text):
        """
        Check string is empty or not

        :param str text: the input string object
        :return: true if string is empty, false otherwise
        :rtype: bool
        """
        return True if text is None or len(str(text).strip()) == 0 else False
