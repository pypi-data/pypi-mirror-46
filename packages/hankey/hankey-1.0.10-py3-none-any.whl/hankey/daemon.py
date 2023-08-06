import logging
import sys
from time import sleep

from hankey.main import run

logger = logging.getLogger("Hankey daemon")
logger.addHandler(logging.FileHandler("/var/log/hankey/logs.log"))
logger.addHandler(logging.StreamHandler(sys.stdout))
info_level = logging.getLevelName('INFO')
logger.setLevel(info_level)


def main():
    while True:
        logger.info("RUNNING HANKEY")
        try:
            user = None
            if len(sys.argv) > 1:
                user = sys.argv[1]
            run(user)
        except Exception as e:
            logger.exception(str(e))
        logger.info("FINISHED RUNNING HANKEY")
        sleep(60 * 60)
