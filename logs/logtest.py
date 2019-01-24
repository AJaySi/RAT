#!/usr/bin/python3

# Common test framework logging library.
from colorlog import ColoredFormatter
# Return a logger object for the common framework.
import logging

# Common logging function for the framework. There needs to be different types of logging:
# 1). One for console(stdout) : The logs seen during the execution.
# 2). Logging into a file : The logs to record the TC execution and reporting.
# 3). Framework level logging : Maybe merged into TC log file. This might be useful for 
# verbose logging and debug information/dumps, plus important test environment details. 
def setup_logger():
    """Return a logger with a default ColoredFormatter."""
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-s%(reset)s- %(asctime)s -[%(filename)s:]- %(reset)s%(blue)s%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red',
        }
    )
    
    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger

logger = setup_logger()