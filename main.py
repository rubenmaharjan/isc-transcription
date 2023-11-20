
import os
from src.transcribe.models.WhisperxTranscriber import WhisperxTranscriber
from datetime import datetime
from src.utils.ISCLogWrapper import ISCLogWrapper, logging
from src.transcribe.TranscribeFactory import TranscribeFactory
from src.utils.TranscriptionConfig import TranscriptionConfig
from config.DEFAULTS import *

def setup_logging():
    """
    Set up logging configuration for the application.

    Returns:
    - Logger instance for the application.
    """
    isc_log_wrapper = ISCLogWrapper(**DEFAULT_LOGGING_CONFIG)

    if not isc_log_wrapper.set_up_logging():
        print("Failed to set up logging, aborting.")
        return 1

    return logging.getLogger(__name__)


logger = setup_logging()

def main():
    config=TranscriptionConfig()

    audio = config.get('audiodir')
    hf_token = config.get('hf_token')
    logger.info(f"AUDIO: {audio} and HFToken: {hf_token}")

    if audio and hf_token:
        logger.info("Starting Transcription.")
        logger.info("CWD: " + os.getcwd())
        model = WhisperxTranscriber("small", hf_token, audio)
        model.transcribe()
    else:
        logger.error("Config values not set correctly")


if __name__ == '__main__':
    main()
