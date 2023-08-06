import logging

FORMAT = "%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s"

_log = logging.getLogger("bets-cli")

debug = _log.debug
info = _log.info
warning = _log.warning
exception = _log.exception
error = _log.error


def init(level=logging.DEBUG):
    logging.basicConfig(format=FORMAT, level=level)
    debug("log initialized!")
