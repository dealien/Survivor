import logging

import coloredlogs


def setup_custom_logger(name, level=0):
    """


    :param name: 

    """
    logformat = '%(asctime)s %(name)s[%(process)d] %(module)s %(levelname)s %(message)s'
    formatter = logging.Formatter(
        fmt=logformat)
    handler = logging.FileHandler('main.log')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    if level is 3:
        logger.setLevel(logging.DEBUG)
    elif level is 2:
        logger.setLevel(logging.INFO)
    elif level is 1:
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.CRITICAL)
    # Avoid adding duplicate handlers
    if len(logger.handlers) > 0:
        for h in logger.handlers:
            if not isinstance(h, logging.FileHandler):
                logger.addHandler(handler)
    else:
        logger.addHandler(handler)
    coloredlogs.install(level='DEBUG',
                        fmt=logformat)
    return logger
