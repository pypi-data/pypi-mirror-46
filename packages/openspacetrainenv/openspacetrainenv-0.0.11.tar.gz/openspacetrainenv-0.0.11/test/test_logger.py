import os
import time
import unittest

from src import Logger


class TestLogger(unittest.TestCase):
    def test_logging_methods(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        Logger(f'{dir_path}/test.log')
        Logger().info('info', location='TEST')
        Logger().debug('debug', location='TEST')
        Logger().warning('warning', location='TEST')
        Logger().error('error', location='TEST')

        log_types = ['INFO', 'DEBUG', 'WARNING', 'ERROR']

        time.sleep(2)

        with open(f'{dir_path}/test.log', mode='w+') as fp:
            lines = fp.readlines()

        for i, line in enumerate(lines):
            self.assertListEqual(line.strip().split(' - ')[2:], [log_types[i], f'[TEST]: {log_types[i].lower()}'])

        os.remove(f'{dir_path}/test.log')
