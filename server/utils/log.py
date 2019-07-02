import logging
import os
import syslog

FORMAT = '%(asctime)s [%(name)s] [%(levelname)s] [%(pathname)s:%(lineno)s %(funcName)s] %(message)s'
logging.basicConfig(filename='Hawkeye.log', level=logging.INFO, format=FORMAT)
logger = logging.getLogger()
