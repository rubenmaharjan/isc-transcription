# *************************************************************************************************************************
#   TranscriptionConfig.py
#       Manage the configuration for an audio transcription system, including access to XML configuration files.
# -------------------------------------------------------------------------------------------------------------------
#   Usage:
#       The module provides an interface for interacting with the transcription configuration through the
#       TranscriptionConfig class. Functions are also available for parsing command-line arguments and for
#       validating XML configuration files.
#
#       Parameters:
#           Various parameters can be defined in an XML configuration file, which are then parsed and applied to
#           the transcription system. Command-line arguments can override configuration file settings.
#
#       Outputs:
#           The TranscriptionConfig class provides methods to retrieve and set configuration values, and to
#           create or delete configuration keys.
#
#   Design Notes:
#   -.  The module makes use of lxml for XML parsing and validation.
#   -.  Custom utility functions are used for command-line parsing and XML validation.
#   -.  The logging module is used to provide feedback and error reporting.
# ---------------------------------------------------------------------------------------------------------------------
#   last updated: November 2023
#   authors: Ruben Maharjan, Bigya Bajarcharya, Mofeoluwa Jide-Jegede, Phil Pfeiffer
# *************************************************************************************************************************

# ***********************************************
# imports
# ***********************************************

# config.DEFAULTS - module to handle default configuration settings for the transcription system
#   DEFAULT_* - constants defining default values for configuration settings
# lxml.etree - provides XML parsing and validation functionality
#   parse - function to parse an XML document into an element tree
#   XMLSchema - class to validate an XML document against XML Schema
# os – operating system primitives
#   path.isfile – test if argument is a file:
# src.utils - custom package for utility functions related to the transcription model
#   helperFunctions - module with functions for command-line argument parsing and XML file validation

from config.DEFAULTS import DEFAULT_CONFIG_FILE, DEFAULT_CONFIG_FILE_SCHEMA, DEFAULT_WHISPER_CONFIGS
from lxml.etree import ElementTree as ET
import os
import src.utils.helperFunctions as helperFunctions
import logging

# ***********************************************
#  auxiliary functions
# ***********************************************

err_to_str = lambda e: '' if str(e) is None else str(e)
logger = logging.getLogger()

# ***********************************************
#  main module
# ***********************************************

def configure_whisperX_operation(config_file, fail_if_missing=True):
    """
    Extract parameters from the XML configuration file if path is specified;
    otherwise, populate with the default XML path over the default configuration values.

    Parameters:
    - config_file: Path to the XML file.
    Note: config_file assumed to have all top-level elements
    """

    # return config_data

# **************************************************************************
    #read XML configuration files for the transcription system.
# **************************************************************************

class TranscriptionConfig(object):

    def __init__(self):
        command_line_args = helperFunctions.parse_command_line_args()
        self.config_data = DEFAULT_WHISPER_CONFIGS
#
        try:
            config_file, fail_if_missing = self.command_line_args.configxml, True
        except:
            config_file, fail_if_missing = DEFAULT_CONFIG_FILE, False
        if not os.path.isfile(config_file):
            err_msg = f"Config file not found: {config_file}"
            if fail_if_missing:   logger.error(err_msg)
            else:                 logger.warning(err_msg)
        else:
            helperFunctions.validate_configxml(logger, config_file, DEFAULT_CONFIG_FILE_SCHEMA)
            try:
                for child in ET.parse(config_file).getroot():
                    self.config_data[child.tag] = child.text
            except Exception as e:
                logger.error(f"Error loading config file: {config_file} - {err_to_str(e)}")

        for (key, value) in command_line_args:
            self.config_data[key] = value


    def get(self, key):
        """
        Get the value for the specified key in the configuration file.
        """
        try:
            return self.config_data.get(key)
        except Exception as e:
            logger.error(f'Could not find element in configuration file: {e}')
            return None

    def set_param(self, key, value):
        """
        Set the value for the specified key in the configuration file.

        :param key: The name of the key in the format 'parent/child' or 'key' if it has no parent.
        :param value: The new value to assign to the key.
        :return: True if the key's value was successfully updated, False otherwise.
        """
        try:
            parts = key.split("/")
            if len(parts) == 1:
                parent = self.root
            elif len(parts) > 1:
                parent = self.root.find('/'.join(parts[:-1]))

            element = parent.find(parts[-1]) if parent is not None else None
            if element is None:
                element = ET.Element(parts[-1])
                parent.append(element)

            element.text = value
            logger.info(f'Set value of key "{key}" to: {value}')
            return True
        except Exception as e:
            logger.error(f'Error while setting element value: {e}')
            return False

    def get_all(self):
        """
        Get all key-value pairs in the configuration file.
        """
        result = {}
        try:
            for child in self.root:
                if child.tag == "settings":
                    for subchild in child:
                        result[f"{child.tag}/{subchild.tag}"] = subchild.text
                else:
                    result[child.tag] = child.text
            return result
        except Exception as e:
            logger.error(f'Error while getting all key-value pairs in configuration file: {e}')
            return False
