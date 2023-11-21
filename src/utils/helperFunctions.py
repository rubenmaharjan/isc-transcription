# *************************************************************************************************************************
#   helperFunctions.py
#       This module provides command-line parsing utilities for an audio transcription application. It leverages the argparse
#       library to parse command-line options and validates XML configuration files against a predefined schema using lxml.
# -------------------------------------------------------------------------------------------------------------------
#   Usage:
#       Call parse_command_line_args() to parse and retrieve command-line arguments.
#       Use validate_configxml(xml_file, xsd_file) to validate an XML configuration against an XSD schema.
#
#       Parameters:
#           Various command-line parameters are supported for specifying audio files, configuration XML, model type,
#           directories for audio files and transcriptions, user tokens for diarization, and allowed file extensions.
#
#       Outputs:
#           Command-line parsing results in a namespace of parsed arguments.
#           XML validation outputs log messages indicating validity or errors.
#
#   Design Notes:
#   -.  The module is designed to be used as a utility in a larger audio transcription application.
#   -.  Logging is configured to provide info and critical feedback for the operations performed.
# ---------------------------------------------------------------------------------------------------------------------
#   last updated: November 2023
#   authors: Ruben Maharjan, Bigya Bajarcharya, Mofeoluwa Jide-Jegede
# *************************************************************************************************************************
# ***********************************************
# imports
# ***********************************************

# argparse - command-line parsing library
#    ArgumentParser - class to parse command-line options

# lxml.etree - XML processing library
#    etree - class for XML document parsing and validation

# logging - logging library
#    getLogger - function to get a logging instance

# config.DEFAULTS - module with default configuration constants
#    DEFAULT_SCHEMA_FILE, DEFAULT_TRANSCRIPTION_DIR, DEFAULT_FILE_EXTENSIONS - constants defining default values

import argparse
from lxml import etree
import logging
from config.DEFAULTS import *


logger = logging.getLogger()

def parse_command_line_args():
    """
    Parse command line arguments and return the parsed arguments.

    Returns:
    - Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description="Process command-line arguments for audio transcription.")
    parser.add_argument("-a", "--audio", help="Specify the input audio file")
    parser.add_argument("-cx", "--configxml", help="Specify the input xml config file", default=DEFAULT_SCHEMA_FILE)
    parser.add_argument("-mt", "--model_type", help="Specify the model type for transcription", default='base')
    parser.add_argument("-ad", "--audiodir", help="Specify the directory of audio to transcribe", default=DEFAULT_TRANSCRIPTION_DIR)
    parser.add_argument("-td", "--transcriptiondir", help="Specify the directory to store transcriptions", default=DEFAULT_TRANSCRIPTION_DIR)
    parser.add_argument("-ht", "--hf_token", help="Specify the user token needed for diarization")
    parser.add_argument("-e", "--extensions", nargs='+', help="List of audio extensions in audiodir", default=DEFAULT_FILE_EXTENSIONS)
    return parser.parse_args()


def validate_configxml(xml_file, xsd_file):
    """
    Validate an XML file against an XSD schema.

    Parameters:
    - xml_file: Path to the XML file.
    - xsd_file: Path to the XSD schema file.
    """
    # Load the XML file
    xml_doc = etree.parse(xml_file)

    # Load the XML schema
    schema = etree.XMLSchema(file=xsd_file)

    logger.info('Validating to check if the xml meets schema requirements')

    # Validate the XML document against the schema
    try:
        schema.assertValid(xml_doc)
        logger.info("XML document is valid according to the schema.")
    except etree.XMLSchemaParseError as xspe:
        logger.critical("XML Schema is not valid: {}".format(xspe))
    except etree.DocumentInvalid as di:
        logger.critical("XML document is not valid: {}".format(di))
    except Exception as e:
        logger.critical("An error occurred during XML validation: {}".format(e))

