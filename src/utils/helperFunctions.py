
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

