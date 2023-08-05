# Logging
import logging

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):

        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

__author__ = 'Daniel Soler'
__copyright__ = '2019, NostrumBioDiscovery'
__url__ = 'https://github.com/nostrumbiodiscovery'
__title__ = 'AnalogFinder'
__description__ = ('AnalogFinder: Given a query molecule and some database find analogs')

name = "analog_finder"

