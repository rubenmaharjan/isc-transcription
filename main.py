# *************************************************************************************************************************
#   main.py 
#       This is the entry point for the transcription application using the WhisperxTranscriber. It handles command-line 
#       arguments, sets up logging, validates XML configuration, and initiates the transcription process.
# -------------------------------------------------------------------------------------------------------------------
#   Usage:
#      python main.py --audio [path_to_audio_file] --configxml [path_to_config_file] [Other_Arguments]
#      Arguments and defaults:
#         -a, --audio [path] : Specify the path to the input audio file to be transcribed.
#         -cx, --configxml [path] : Specify the path to the XML configuration file. Default 'config/default_config.xml'
#         -mt, --model_type [type] : Specify the Whisper model type for transcription. Default 'base'
#         -ad, --audiodir [dir] : Specify the directory of audio files to transcribe. Default 'audio_files'
#         -td, --transcriptiondir [dir] : Specify the directory to store transcriptions. Default 'transcriptions'
#         -ht, --hf_token [token] : Hugging Face authentication token for using models with diarization.
#         -e, --extensions [ext] : List of audio file extensions in audiodir. Default ['.mp3', '.wav', '.aac']
#      Outputs:
#         Initiates the transcription process and outputs transcription files in the specified directory.
#         Generates logs of the application's activities and errors.
# ---------------------------------------------------------------------------------------------------------------------
#   TODO:
#   -.  Improve error handling for command-line argument parsing and XML validation.
#   -.  Extend the application to handle different input/output formats and sources.
#   -.  Refactor the code for better modularity and testability.
# ---------------------------------------------------------------------------------------------------------------------
#   last updated:  November 2023
#   authors:       Ruben Maharjan, Bigya Bajarcharya, Mofeoluwa Jide-Jegede
# *************************************************************************************************************************
# ***********************************************
# imports
# ***********************************************

# os - for file path operations
#   getcwd - get the current working directory

# Custom packages for the transcription model and utilities
# src.transcribe.models.WhisperxTranscriber - custom package for the transcription model
#   WhisperxTranscriber - class to handle transcription process using Whisper models

# src.utils.ISCLogWrapper - custom wrapper for logging functionalities
#   ISCLogWrapper - class to configure and initiate logging
#   logging.getLogger - method to return a logger instance with the specified name

# src.utils.TranscriptionConfig - custom configuration handler for transcription settings
#   TranscriptionConfig - class to manage transcription configuration from an XML file

import os
from src.transcribe.models.WhisperxTranscriber import WhisperxTranscriber
from src.utils.ISCLogWrapper import ISCLogWrapper, logging
from src.utils.TranscriptionConfig import TranscriptionConfig

def setup_logging():
    """
    Set up logging configuration for the application.

    Returns:
    - Logger instance for the application.
    """
    isc_log_wrapper = ISCLogWrapper()

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
