__all__ = (
    'LOG_LEVEL_SYSLOG_LEVEL_MAP',
    'SIGNAL_NAME_NUM_MAP',
    'SIGNAL_NUM_NAME_MAP',
)
import logging
import signal
import syslog
import typing


LOG_LEVEL_SYSLOG_LEVEL_MAP: typing.Dict[int, int] = {
    logging.DEBUG: syslog.LOG_DEBUG,  # 10 -> 7
    logging.INFO: syslog.LOG_INFO,  # 20 -> 6
    logging.WARNING: syslog.LOG_WARNING,  # 30 -> 4
    logging.ERROR: syslog.LOG_ERR,  # 40 -> 3
    logging.CRITICAL: syslog.LOG_CRIT  # 50 -> 2
}

SIGNAL_NAME_NUM_MAP: typing.Dict[str, int] = {
    k: v
    for k, v in signal.__dict__.items()
    if k.startswith('SIG') and '_' not in k
}

SIGNAL_NUM_NAME_MAP: typing.Dict[int, str] = dict(zip(
    SIGNAL_NAME_NUM_MAP.values(),
    SIGNAL_NAME_NUM_MAP.keys(),
))

