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

import os
import xml.etree.ElementTree as ET
import copy 

from config.DEFAULTS import (DEFAULT_CONFIG_FILE, DEFAULT_CONFIG_FILE_SCHEMA,
                             DEFAULT_WHISPER_CONFIG)
from src.utils.helperFunctions import (err_to_str, logger,
                                       parse_command_line_args,
                                       validate_configxml)

# ***********************************************
#  main module
# ***********************************************


# **************************************************************************
# read XML configuration files for the transcription system.
# **************************************************************************


class TranscriptionConfig():
    def __init__(self):
        self.command_line_args = copy.deepcopy(parse_command_line_args())
        self.config_data = copy.deepcopy(DEFAULT_WHISPER_CONFIG)

        try:
            config_file, fail_if_missing = copy.deepcopy(self.command_line_args.configxml), True
        except AttributeError:
            config_file, fail_if_missing = copy.deepcopy(DEFAULT_CONFIG_FILE), False

        self.root = None
        if os.path.isfile(config_file):
            try:
                self.root = ET.parse(config_file).getroot()
            except Exception as e:
                logger.error(f"Error loading config file: {config_file} - {err_to_str(e)}")
        
        if not self.root:
            err_msg = f"Config file not found: {config_file}"
            if fail_if_missing:
                logger.error(err_msg)
            else:
                logger.warning(err_msg)
        else:
            validate_configxml(logger, config_file, DEFAULT_CONFIG_FILE_SCHEMA)
            try:
                for child in self.root:
                    self.config_data[child.tag] = child.text
            except Exception as e:
                logger.error(f"Error loading config file: {config_file} - {err_to_str(e)}")

        for key, value in self.command_line_args.items():
            if value is not None:
                self.config_data[key] = value

        print(f"Config data: {self.config_data}")

    def get(self, key):
        """
        Get the value for the specified key in the configuration file.
        """
        try:
            return self.config_data.get(key)
        except Exception as e:
            logger.error(
                f'Could not find element in configuration file: {err_to_str(e)}')
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
            logger.error(f'Error while setting element value: {err_to_str(e)}')
            return False

    def get_all(self):
        """
        Get all key-value pairs in the configuration file.
        """
        result = {}
        try:
            for child in self.root:
                result[child.tag] = child.text
            return result
        except Exception as e:
            logger.error(
                f'Error while getting all key-value pairs in configuration file: {err_to_str(e)}')
            return False
