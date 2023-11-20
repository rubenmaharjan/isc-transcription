import os
import argparse
from lxml import etree
from src.transcribe.models.WhisperxTranscriber import WhisperxTranscriber
from datetime import datetime
from src.utils.ISCLogWrapper import ISCLogWrapper, logging
from src.transcribe.TranscribeFactory import TranscribeFactory
from src.utils.TranscriptionConfig import TranscriptionConfig

# todo add default audio
DEFAULT_AUDIO = None
DEFAULT_XML_PATH = "./config/dev_config.xml"


def setup_logging():
    """
    Set up logging configuration for the application.

    Returns:
    - Logger instance for the application.
    """
    isc_log_wrapper = ISCLogWrapper(
        console_log_output="stdout",
        console_log_level="info",
        console_log_color=True,
        logfile_file=datetime.now().strftime('ISC_%H_%M_%d_%m_%Y.log'),
        logfile_log_level="debug",
        logfile_log_color=False,
        logfile_path="logs"
    )

    if not isc_log_wrapper.set_up_logging():
        print("Failed to set up logging, aborting.")
        return 1

    return logging.getLogger(__name__)


logger = setup_logging()


def parse_command_line_args():
    """
    Parse command line arguments and return the parsed arguments.

    Returns:
    - Parsed command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--audio", help="Specify the input audio file", default=None)
    parser.add_argument(
        "--configxml", help="Specify the input xml config file", default=os.path.abspath(f"{os.getcwd()}/{DEFAULT_XML_PATH}"))

    # new arguments
    parser.add_argument(
        "--model_type", help="Specify the model type for transcription")
    parser.add_argument(
        "--audiodir", help="Specify the directory of audio to transcribe")
    parser.add_argument("--transcriptiondir",
                        help="Specify the directory to store transcriptions")
    parser.add_argument(
        "--hf_token", help="Specify the user token needed for diarization")
    parser.add_argument(
        "--extensions", help="List of audio extensions in audiodir")

    return parser.parse_args()


def get_config_value(parsed_args, key):
    """
    Retrieve the value of a configuration key from parsed arguments or default settings.

    Parameters:
    - parsed_args: Configuration arguments received from the command line.
    - key: Argument name used in the command line and the XML configuration.

    Returns:
    - The value of the specified key.
    """
    if parsed_args:
        logger.info("Using configuration from parsed command line arguments.")

        if not key:
            logger.error(
                "Argument name must be specified to access parsed argument value.")
            return None

        try:
            if getattr(parsed_args,key) != None:
                parsed_key_value = getattr(parsed_args,key)
                logger.info(f'Parsed value of {key} is {parsed_key_value}')
                return parsed_key_value
        except KeyError as e:
            logger.error(f"{key} not found in parsed arguments. Error: {e}")

        try:
            if parsed_args.configXML:
                parsed_configXML_path = parsed_args.configXML

                if not parsed_configXML_path.endswith('.xml'):
                    logger.error(
                        'Wrong file extension. Please provide an XML config file.')
                else:
                    logger.info(
                        "Using configuration from parsed XML file in command line.")
                    validate_configxml(parsed_configXML_path,
                                       "./config_validator.xsd")
                    parsed_config_XML = TranscriptionConfig(
                        parsed_configXML_path)
                    return parsed_config_XML.get(key)

        except AttributeError as e:
            logger.error(
                f"configXML not found in parsed arguments. Please provide a configuration file. Error: {e}")

    # try:
    #     logger.info("Using default configuration set from the codebase.")

    #     audioPathPrefix = os.getcwd()
    #     path = os.path.join(audioPathPrefix, DEFAULT_XML_PATH)
    #     config = TranscriptionConfig(path)
    #     validate_configxml(path, "./config_validator.xsd")
    #     return config.get(key)
    # except Exception as e:
    #     logger.error(
    #         f"No valid config specified. Transcription cannot proceed. Error: {e}")
    #     return None


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
    except Exception as e:
        logger.critical("XML document is not valid according to the schema.", e)


def main():
    #todo: populate configuration variables with the default values
    args = parse_command_line_args()
    # todo:Check for configXML argument
    get_cmd_args = args if args.audio or args.configxml else None 
    audio = get_config_value(get_cmd_args, 'audiodir')
    hf_token = get_config_value(get_cmd_args, 'hf_token')
    logger.info(f"AUDIO: {audio} and HFToken: {hf_token}")

    # if audio and hf_token:
    #     logger.info("Starting Transcription.")
    #     logger.info("CWD: " + os.getcwd())
    #     model = WhisperxTranscriber("small", hf_token, audio)
    #     model.transcribe()
    # else:
    #     logger.error("Config values not set correctly")


if __name__ == '__main__':
    main()
