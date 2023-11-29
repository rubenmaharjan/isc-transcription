# *************************************************************************************************************************
#   helperFunctions.py
#       Provide command-line parsing for an audio transcription application.
#       Validate XML configuration files against a predefined schema using lxml.
# -------------------------------------------------------------------------------------------------------------------
#   Usage:
#       Call parse_command_line_args() to parse and retrieve command-line arguments.
#       Use validate_configxml(xml_file, xsd_file) to validate an XML configuration against an XSD schema.
#
#       Parameters:
#           Command-line parameters are supported for specifying audio files, configuration XML, model type,
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
#   authors: Ruben Maharjan, Bigya Bajarcharya, Mofeoluwa Jide-Jegede, Phil Pfeiffer
# *************************************************************************************************************************

# ***********************************************
# imports
# ***********************************************

# argparse - command-line parsing library
#    ArgumentParser - class to parse command-line options
# config.DEFAULTS - module with default configuration constants
#    DEFAULT_SCHEMA_FILE, DEFAULT_TRANSCRIPTION_DIR, DEFAULT_FILE_EXTENSIONS - constants defining default values
# lxml.etree - XML processing library
#    etree - class for XML document parsing and validation
# logging - logging library
#    getLogger - function to get a logging instance

import argparse
from config.DEFAULTS import DEFAULT_AUDIO, DEFAULT_AUDIO_FILE_EXTENSIONS, DEFAULT_CONFIG_FILE, DEFAULT_CONFIG_FILE_SCHEMA
from lxml import etree
# import logging

# logger = logging.getLogger()

# ***********************************************
#  auxiliary functions
# ***********************************************


def err_to_str(e): return '' if str(e) is None else str(e)


# ***********************************************
#  helper functions proper
# ***********************************************

# =========================================================================================
#    Parse command line arguments and return the parsed arguments.
#   Returns:
#    - Parsed command line arguments as attributes named by the add_argument 'dest' parameters
#
#   Design notes:
#   -.  Defaults for parameters with unspecified defaults managed in the modules that use these parameters
# =========================================================================================

def parse_command_line_args():
    parser = argparse.ArgumentParser(
        description="Process command-line arguments for audio transcription.")
    #
    parser.add_argument("-au", "--audio", help="The input audio file or file directory", dest='audio', default=DEFAULT_AUDIO)
    parser.add_argument("-cx", "--configxml", help="An alternative xml config file", dest='configxml')
    parser.add_argument("-dv", "--device", help="Hardware device for diarization", dest='device')
    parser.add_argument("-ed", "--enable_diarization", help="If true, diarize output after transcription", dest="diarize", default=False)
    parser.add_argument("-ex", "--extensions", nargs='+', help="List of audio extensions in audiodir", dest='extensions', default=DEFAULT_AUDIO_FILE_EXTENSIONS)
    parser.add_argument("-ht", "--hf_token", help="The user token needed for diarization", dest="hf_token")
    parser.add_argument("-lf", "--logfile", help="The file used to log application output", dest="logfile")
    parser.add_argument("-mt", "--model_type", help="The model type for transcription", dest="model_type")
    parser.add_argument("-td", "--transcription_dir", help="The directory to store transcriptions", dest="transcriptionsdir")
    
    return parser.parse_args()


def validate_configxml(logger, xml_file=DEFAULT_CONFIG_FILE, xsd_schema=DEFAULT_CONFIG_FILE_SCHEMA):
    """
    Validate an XML file against an XSD schema.

    Parameters:
      logger:  log object for logging routine status
    - xml_file: Path to the XML file.
    - xsd_file: Path to the XSD schema file.
    """
    # Load the XML file
# TODO I think you need to check for a parse error here 
    xml_doc = etree.parse(xml_file)

    # Load the XML schema
    schema = etree.XMLSchema(file=xsd_schema)

    logger.info('Validating to check if the xml meets schema requirements')

    # Validate the XML document against the schema
    try:
        schema.assertValid(xml_doc)
        logger.info(
            f"XML document ({xml_doc}) is valid according to the schema ({xsd_schema}).")
    except etree.XMLSchemaParseError as xspe:
        logger.critical(f"XML Schema is not valid: {xspe}")
    except etree.DocumentInvalid as di:
        logger.critical(f"XML document is not valid: {di}")
    except Exception as e:
        logger.critical(
            f"An error occurred during XML validation: {err_to_str(e)}")
