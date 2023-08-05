import logging
from logging.handlers import RotatingFileHandler
import sys
import os


def load(logger_name):

    """ Shorthand for loading a logger """

    return logging.getLogger(logger_name)


def create(logger_name, file: str=None, rewrite: bool=False, level: str="INFO"):

    """ Configures a new logger object. """

    log = logging.getLogger(logger_name)

    # Some colors to make the next part more readable
    blue = "\033[0;34m"
    green = "\033[0;32m"
    purple = "\033[0;35m"
    red = "\033[0;31m"
    bold_red = "\033[1;31m"
    reset = "\033[0m"

    # Configure new configuration for "levelname" (add colors)
    logging.addLevelName(logging.DEBUG, f"{blue}DEBUG{reset}")
    logging.addLevelName(logging.INFO, f"{green}INFO{reset}")
    logging.addLevelName(logging.WARN, f"{purple}WARN{reset}")
    logging.addLevelName(logging.ERROR, f"{red}ERROR{reset}")
    logging.addLevelName(logging.CRITICAL, f"{bold_red}CRITICAL{reset}")

    # Configure the logger to screen / STDOUT
    formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    if rewrite:
        stream_handler.terminator = ""
    log.addHandler(stream_handler)

    try:
        if file:
            # If file is "True", check environment var for log location, or fall back to logger_name in current directory."
            if type(file) == bool:
                file = os.environ.get("LOG_FILE_OUTPUT", logger_name)

            file_handler = RotatingFileHandler(file, mode='a', maxBytes=1000000, backupCount=2, encoding='utf-8')
            file_handler.setFormatter(formatter)
            log.addHandler(file_handler)
    except PermissionError as e:
        dlog.error(f"Cannot write log to file in '{file}' due to permission issues.")

    # Set the final level
    log.setLevel(level)

    return log

dlog = create('logquicky', level="ERROR")
