# *************************************************************************************************************************
#   ISCLogWrapper.py
#       This module defines a wrapper for the Python logging module, providing a convenient setup for both console and 
#       file logging with optional colorized output. It is configurable via a dictionary of default values and supports 
#       custom log formats and date formats.
# -------------------------------------------------------------------------------------------------------------------
#   Usage:
#       The ISCLogWrapper class is used to configure and initialize logging with predefined settings. It supports
#       customization of console and file log levels, output destinations, and whether to use color in output.
#
#       Parameters:
#           default_dict - A dictionary of default logging configurations including log levels, file paths, and colorization preferences.
#
#       Outputs:
#           Logging output to console and/or to a specified log file, with an optional colorized format for better readability.
#
#   Design Notes:
#   -.  LogFormatter is a custom formatter class that extends logging.Formatter to add color support.
#   -.  ISCLogWrapper sets up logging according to the configuration provided and applies the LogFormatter.
# ---------------------------------------------------------------------------------------------------------------------
#   last updated: November 2023
#   authors: Ruben Maharjan, Bigya Bajarcharya, Mofeoluwa Jide-Jegede
# *************************************************************************************************************************
# ***********************************************
# imports
# ***********************************************

# os - provides a portable way of using operating system dependent functionality
#    os.path.join - join one or more path components intelligently

# sys - provides access to some variables used or maintained by the interpreter
#    sys.stdout, sys.stderr - file objects used by the print and exception calls to write their output

# logging - provides a flexible framework for emitting log messages from Python programs
#    logging.getLogger - return a logger with the specified name
#    logging.Formatter - class which formats logging records
#    logging.StreamHandler - sends logging output to streams like stdout or stderr
#    logging.FileHandler - sends logging output to a disk file

# glob - finds all the pathnames matching a specified pattern according to the rules used by the Unix shell
# No direct glob usage in the imports section

# config.DEFAULTS - module containing default configuration values for the logging setup
#    DEFAULT_LOGGING_CONFIG - a dictionary containing the default logging configuration settings

import os
import sys
import logging
import glob
from config.DEFAULTS import DEFAULT_LOGGING_CONFIG

# Define constants used for the log line format and date format
LOG_LINE_TEMPLATE="%(color_on)s[%(asctime)s.%(msecs)03d] [%(threadName)s] [%(levelname)-8s] [%(filename)s:%(lineno)d] %(message)s%(color_off)s"
LOG_LING_DATEFMT="%Y-%m-%d %H:%M:%S"

# Logging formatter supporting colorized output
class LogFormatter(logging.Formatter):

    COLOR_CODES = {
        logging.CRITICAL: "\033[1;35m", # bright/bold magenta
        logging.ERROR:    "\033[1;31m", # bright/bold red
        logging.WARNING:  "\033[1;33m", # bright/bold yellow
        logging.INFO:     "\033[0;37m", # white / light gray
        logging.DEBUG:    "\033[1;30m"  # bright/bold black / dark gray
    }

    RESET_CODE = "\033[0m"

    def __init__(self, color, *args, **kwargs):
        super(LogFormatter, self).__init__(*args, **kwargs)
        self.color = color

    def format(self, record, *args, **kwargs):
        if (self.color == True and record.levelno in self.COLOR_CODES):
            record.color_on  = self.COLOR_CODES[record.levelno]
            record.color_off = self.RESET_CODE
        else:
            record.color_on  = ""
            record.color_off = ""
        return super(LogFormatter, self).format(record, *args, **kwargs)

# This class wraps the logging module and provides methods to set up logging
class ISCLogWrapper:

    # The constructor takes several arguments that configure logging
    def __init__(self, default_dict=DEFAULT_LOGGING_CONFIG):
        self.console_log_output = default_dict['console_log_output'] # The output to write the console logs to (stdout or stderr)
        self.console_log_level = default_dict['console_log_level'] # The minimum logging level to log to the console (e.g., INFO, WARNING, etc.)
        self.console_log_color = default_dict['console_log_color'] # A boolean value indicating whether the console log should be colorized
        self.logfile_file = default_dict['logfile_file'] # The filename to write the logs to
        self.logfile_path = default_dict['logfile_path'] # The directory path to write the logs to
        self.logfile_log_level = default_dict['logfile_log_level'] # The minimum logging level to log to the file
        self.logfile_log_color = default_dict['logfile_log_color'] # A boolean value indicating whether the file log should be colorized

    # Set up logging using the configuration values passed to the constructor

    # Set up logging
    def set_up_logging(self):

        # Create logger
        # For simplicity, we use the root logger, i.e. call 'logging.getLogger()'
        # without name argument. This way we can simply use module methods for
        # for logging throughout the script. An alternative would be exporting
        # the logger, i.e. 'global logger; logger = logging.getLogger("<name>")'
        logger = logging.getLogger()

        # Set global log level to 'debug' (required for handler levels to work)
        logger.setLevel(logging.DEBUG)

        # Create console handler
        console_log_output = self.console_log_output.lower()
        if (console_log_output == "stdout"):
            console_log_output = sys.stdout
        elif (console_log_output == "stderr"):
            console_log_output = sys.stderr
        else:
            print("Failed to set console output: invalid output: '%s'" % console_log_output)
            return False
        console_handler = logging.StreamHandler(console_log_output)

        # Set console log level
        try:
            console_handler.setLevel(self.console_log_level.upper()) # only accepts uppercase level names
        except:
            print("Failed to set console log level: invalid level: '%s'" % self.console_log_level)
            return False

        # Create and set formatter, add console handler to logger
        console_formatter = LogFormatter(fmt=LOG_LINE_TEMPLATE, color=self.console_log_color, datefmt=LOG_LING_DATEFMT)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # Create log file handler
        try:
            logfile_handler = logging.FileHandler(os.path.join(self.logfile_path, self.logfile_file))
        except Exception as exception:
            print("Failed to set up log file: %s" % str(exception))
            return False

        # Set log file log level
        try:
            logfile_handler.setLevel(self.logfile_log_level.upper()) # only accepts uppercase level names
        except:
            print("Failed to set log file log level: invalid level: '%s'" % self.logfile_log_level)
            return False

        # Create and set formatter, add log file handler to logger
        logfile_formatter = LogFormatter(fmt=LOG_LINE_TEMPLATE, color=self.logfile_log_color, datefmt=LOG_LING_DATEFMT)
        logfile_handler.setFormatter(logfile_formatter)
        logger.addHandler(logfile_handler)

        # Success
        return True
