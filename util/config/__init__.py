import os
import sys
from configobj import ConfigObj

from util import Strings


class ConfigParser:
    @staticmethod
    def load(p=None):
        """
        Load configuration by given path or `CONFIG` environment. The environment variable is primary lookup

        :param str or None p: the configuration path
        :return: the configuration object
        :rtype: Config
        """
        if p is None:
            if 'CONFIG' in os.environ:
                p = os.environ['CONFIG']
            elif len(sys.argv) > 1:
                p = sys.argv[1]
            else:
                raise Exception('Configuration parameter must be set')

        if Strings.is_empty(p):
            raise Exception('Configuration path is missing')

        if not os.path.exists(p):
            raise Exception('Configuration file does not exists "{0}"'.format(p))

        conf = ConfigObj(p)

        # size of sections must be greater than one
        if len(conf.sections) == 0:
            raise Exception('There are no any sections')

        return conf


path = os.environ['TEST_CONFIG'] if 'TEST_CONFIG' in os.environ else sys.argv[-1:][0]

config = ConfigParser.load(path)
