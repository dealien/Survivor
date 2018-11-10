import logging

import coloredlogs

log = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', fmt='%(asctime)s.%(msecs)03d %(programname)s %(name)s[%(process)d] %(levelname)s %(message)s')
