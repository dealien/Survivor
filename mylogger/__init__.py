import logging

import coloredlogs


def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d %(module)s %(name)s[%(process)d] %(levelname)s %(message)s')
    handler = logging.FileHandler('main.log')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # Avoid adding duplicate handlers
    if len(logger.handlers) > 0:
        for h in logger.handlers:
            if not isinstance(h, logging.FileHandler):
                logger.addHandler(handler)
    else:
        logger.addHandler(handler)
    coloredlogs.install(level='DEBUG',
                        fmt='%(asctime)s.%(msecs)03d %(module)s %(name)s[%(process)d] %(levelname)s %(message)s')
    return logger
