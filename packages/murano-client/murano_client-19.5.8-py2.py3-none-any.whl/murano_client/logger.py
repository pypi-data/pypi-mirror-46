# pylint: disable=C1801,W1202,C0103
import os
import sys
import logging
import traceback
from logging.handlers import RotatingFileHandler

LOG_FORMAT = "%(asctime)s-%(levelname)s | %(name)s | %(funcName)s:%(lineno)d ::> %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)

env_level = os.environ.get('MURANO_CLIENT_DEBUG')
if isinstance(env_level, str):
    env_level = env_level.upper()

LOG_KWARGS = {
    'format': LOG_FORMAT,
    'level': getattr(logging, env_level or 'CRITICAL')
}
DEFAULT_LOG_FILE        = os.environ.get('MURANO_CLIENT_LOGFILE', 'stderr')
DEFAULT_LOG_MAX_BYTES   = int(os.environ.get('MURANO_CLIENT_LOG_MAX_BYTES', 1024*1000))
DEFAULT_LOG_MAX_BACKUPS = int(os.environ.get('MURANO_CLIENT_MAX_BACKUPS', 3))

if DEFAULT_LOG_FILE in ['stdout', 'stderr']:
    DEFAULT_LOG_FILE = getattr(sys, DEFAULT_LOG_FILE)
    LOG_KWARGS['stream'] = DEFAULT_LOG_FILE
else:
    LOG_KWARGS['filename'] = DEFAULT_LOG_FILE
    LOG_KWARGS['filemode'] = 'a'

logging.basicConfig(**LOG_KWARGS)
logging.getLogger().propagate = False

def log_exceptions(ex_cls, ex, tb):
    _tb = ''
    for e in traceback.format_tb(tb):
        _tb += e
    logging.critical('murano_client logging unhandled exception: \n{}{}'
                     .format(_tb, ex))
sys.excepthook = log_exceptions

def getLogger(*args, **kwargs):
    name = args[0]
    if not name.startswith("murano_client"):
        name = 'murano_client.' + args[0]
    log = logging.getLogger(name=name)

    if not len(log.handlers) and DEFAULT_LOG_FILE not in [sys.stdout, sys.stderr]:
        rfh = RotatingFileHandler(
            kwargs.get('log-filename') or DEFAULT_LOG_FILE,
            maxBytes=DEFAULT_LOG_MAX_BYTES,
            backupCount=DEFAULT_LOG_MAX_BACKUPS,
        )
        rfh.setFormatter(FORMATTER)
        log.addHandler(rfh)

    elif not len(log.handlers) and DEFAULT_LOG_FILE in [sys.stdout, sys.stderr]:
        streamh = logging.StreamHandler(DEFAULT_LOG_FILE)
        streamh.setFormatter(FORMATTER)
        log.addHandler(streamh)

    log.propagate = False
    return log

