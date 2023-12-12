# *************************************************************************************************************************
#   ISCLogWrapper.py
#       This module defines a wrapper for the Python logging module, providing a convenient setup for console and
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
#   -.  LogRecordFormatter is a custom formatter class that extends logging.Formatter to add color support.
#   -.  ISCLogWrapper sets up logging according to the configuration provided and applies the LogFormatter.
# ---------------------------------------------------------------------------------------------------------------------
#   last updated: November 2023
#   authors: Ruben Maharjan, Bigya Bajarcharya, Mofeoluwa Jide-Jegede, Phil Pfeiffer
# *************************************************************************************************************************

# ***********************************************
# imports
# ***********************************************

# config.DEFAULTS - module containing default configuration values for the logging setup
#    DEFAULT_LOGGING_CONFIG - a dictionary containing the default logging configuration settings
# logging - provides a flexible framework for emitting log messages from Python programs
#    logging.getLogger - return a logger with the specified name
#    logging.Formatter - class which formats logging records
#    logging.StreamHandler - sends logging output to streams like stdout or stderr
#    logging.FileHandler - sends logging output to a disk file
# os - provides a portable way of using operating system dependent functionality
#    os.path.join - join one or more path components intelligently
# sys - provides access to some variables used or maintained by the interpreter
#    sys.stdout, sys.stderr - file objects used by the print and exception calls to write their output

import logging
import os
import sys

from config.DEFAULTS import (DEFAULT_LOG_RECORD_FORMAT_CONFIG,
                             DEFAULT_LOGGING_CONFIG)
from .helperFunctions import err_to_str

# Logging formatter supporting colorized output
# ***************************************************************************************************************************
# LogRecordFormatter:  Set up object for controlling the appearance of log records
#
#    Methods:
#     __init__():  set up parameters for formatting the log
#         Parameters:
#            useColor – determine whether to colorize log records
#       line_format():  return config module default for record format
#       date_format():  return config module default for date format
#       format(): format a log record
#         Parameters:
#           record – record to format
#         Outputs:
#           The formatted record
# ***************************************************************************************************************************


class LogRecordFormatter(logging.Formatter):

    @staticmethod
    def line_format(): return DEFAULT_LOG_RECORD_FORMAT_CONFIG['line_format']

    @staticmethod
    def date_format(): return DEFAULT_LOG_RECORD_FORMAT_CONFIG['date_format']

    def __init__(self, color, *args, **kwargs):
        super(LogRecordFormatter, self).__init__(*args, **kwargs)
        self.useColor = color
        self.colorCodes = DEFAULT_LOG_RECORD_FORMAT_CONFIG['color_codes']
        self.resetCode = DEFAULT_LOG_RECORD_FORMAT_CONFIG['reset']

    def format(self, record, *args, **kwargs):
        record.color_on, record.color_off = "", ""
        if (self.useColor and record.levelno in self.colorCodes):
            record.color_on = self.colorCodes[record.levelno]
            record.color_off = self.resetCode
        return super(LogRecordFormatter, self).format(record, *args, **kwargs)

# ***************************************************************************************************************************
# ISCLogWrapper:  wrap the logging module, providing methods to set up logging
#
#    Methods:
#     __init__():  set up parameters for formatting the log
#         Parameters:
#            log_dict: define the following parameters for logging operation –
#                console_log_output– where to direct console messages
#                console_log_level – minimum level at which to log console messages
#                console_colorize – whether to colorize log console messages
#                logfile_path– path to file (ignored if name set to stdout or stderr)
#                logfile_file – name of file
#                logfile_log_level – minimum level at which to log logfile messages
#                logfile_colorize – whether to colorize logfile  messages

#
#       format(): format a log recrod
#         Parameters:
#           record – record to format
#         Outputs:
#           The formatted record
# ***************************************************************************************************************************


class ISCLogWrapper(object):

    def __init__(self, config):
        # Configurable logging parameters
        self.console_log_output = config.get('console_log_output') if 'console_log_output' in config.get_all(
        ) else DEFAULT_LOGGING_CONFIG['console']['output']
        self.console_log_level = config.get('console_log_level') if 'console_log_level' in config.get_all(
        ) else DEFAULT_LOGGING_CONFIG['console']['log_level']
        self.console_colorize = config.get('console_colorize') if 'console_colorize' in config.get_all(
        ) else DEFAULT_LOGGING_CONFIG['console']['colorize']
        self.logfile_path = config.get('logfile_path') if 'logfile_path' in config.get_all(
        ) else DEFAULT_LOGGING_CONFIG['logfile']['path']
        self.logfile_file = config.get('logfile_file') if 'logfile_file' in config.get_all(
        ) else DEFAULT_LOGGING_CONFIG['logfile']['name']
        self.logfile_log_level = config.get('logfile_log_level') if 'logfile_log_level' in config.get_all(
        ) else DEFAULT_LOGGING_CONFIG['logfile']['log_level']
        self.logfile_colorize = config.get('logfile_colorize') if 'logfile_colorize' in config.get_all(
        ) else DEFAULT_LOGGING_CONFIG['logfile']['colorize']

        # Log record formatting parameters
        self.line_format = config.get('line_format') if 'line_format' in config.get_all(
        ) else LogRecordFormatter.line_format()
        self.date_format = config.get('date_format') if 'date_format' in config.get_all(
        ) else LogRecordFormatter.date_format()

    # Set up logging using the configuration values passed to the constructor
    def set_up_logging(self):

        # Create logger
        # For simplicity, we use the root logger, i.e. call 'logging.getLogger()' without a name argument.
        # This way we can simply use module methods for logging throughout the script.
        # An alternative would be exporting the logger, i.e.
        #     'global logger; logger = logging.getLogger("<name>")'
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
            print(
                f"Invalid console output: {console_log_output}",  file=sys.stderr)

        console_handler = logging.StreamHandler(console_log_output)

        # Set console log level
        try:
            # only accepts uppercase level names
            console_handler.setLevel(self.console_log_level.upper())
        except Exception as exception:
            print(
                f"Failed to set console log level. Invalid level: {self.console_log_level}  \n Error: {err_to_str(exception)}",  file=sys.stderr)
            return False

        # Create and set formatter, add console handler to logger
        console_formatter = LogRecordFormatter(
            fmt=self.line_format, color=self.console_colorize, datefmt=self.date_format)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # Create log file handler
        try:
            if (console_log_output == "stdout"):
                logfile_handler = logging.FileHandler(sys.stdout)
            elif (console_log_output == "stderr"):
                logfile_handler = logging.FileHandler(sys.stderr)
            else:
                logfile_handler = logging.FileHandler(
                    os.path.join(self.logfile_path, self.logfile_file))
        except Exception as exception:
            print(
                f"Failed to set up log file: {err_to_str(exception)}",  file=sys.stderr)
            return False

        # Set log file log level
        try:
            # only accepts uppercase level names
            logfile_handler.setLevel(self.logfile_log_level.upper())
        except Exception as exception:
            print(
                f"Failed to set up log file log level: {err_to_str(exception)}",  file=sys.stderr)
            return False

        # Create and set formatter, add log file handler to logger
        logfile_formatter = LogRecordFormatter(
            fmt=self.line_format, color=self.logfile_colorize, datefmt=self.date_format)
        logfile_handler.setFormatter(logfile_formatter)
        logger.addHandler(logfile_handler)

        # Success
        return True
