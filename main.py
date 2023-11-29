# *************************************************************************************************************************
#   main.py 
#       This script serves as the entry point for the audio transcription application, incorporating the WhisperxTranscriber
#       for processing audio files. It utilizes command-line argument handling, logging via ISCLogWrapper, XML configuration
#       validation with TranscriptionConfig, and file searching with IscFileSearch.
# -------------------------------------------------------------------------------------------------------------------
#   Usage:
#      python main.py --audio [path_to_audio_file] --configxml [path_to_config_file] [Other_Arguments]
#      Arguments and defaults:
#         -a, --audio [path] : Path to the audio file or directory for transcription.
#         -cx, --configxml [path] : XML configuration file. Default is 'config/default_config.xml'
#         -mt, --model_type [type] : Whisper model type for transcription. Defaults to 'base'.
#         -ad, --audiodir [dir] : Directory containing audio files for transcription. Defaults to 'audio_files'.
#         -td, --transcription_dir [dir] : Directory to store transcription files. Defaults to 'transcriptions'.
#         -ht, --hf_token [token] : Hugging Face token for model access with diarization.
#         -e, --extensions [ext] : List of allowed audio file extensions. Defaults to ['.mp3', '.wav', '.aac'].
#      Outputs:
#         Processes and transcribes audio files, outputting transcription files in the specified directory.
#         Application activity and errors are logged.
# ---------------------------------------------------------------------------------------------------------------------
#   TODO:
#   -.  Enhance error handling for argument parsing and configuration validation.
#   -.  Expand support for various input/output formats and sources.
#   -.  Refactor for improved modularity and testability.
# ---------------------------------------------------------------------------------------------------------------------
#   last updated:  November 2023
#   authors:       Ruben Maharjan, Bigya Bajarcharya, Mofeoluwa Jide-Jegede
# *************************************************************************************************************************
# ***********************************************
# imports
# ***********************************************

# os - module providing a portable way of using operating system dependent functionality
#   os.path - submodule of os for manipulating paths
#   os.path.isdir, os.path.isfile - functions to check if a path is a directory or a file

# Custom packages for the transcription model and utilities
# src.transcribe.models.WhisperxTranscriber - custom package for the transcription model
#   WhisperxTranscriber - class to handle transcription process using Whisper models

# src.utils.ISCLogWrapper - custom wrapper for logging functionalities
#   ISCLogWrapper - class to configure and initiate logging
#   logging.getLogger - method to return a logger instance with the specified name

# src.utils.TranscriptionConfig - custom configuration handler for transcription settings
#   TranscriptionConfig - class to manage transcription configuration from an XML file

# src.utils.IscFileSearch - module for searching and handling files within directories
#   IscFileSearch - class for searching files and performing file operations in a specified directory

import os
from src.transcribe.models.WhisperxTranscriber import WhisperxTranscriber
from src.utils.ISCLogWrapper import ISCLogWrapper, logging
from src.utils.TranscriptionConfig import TranscriptionConfig
from src.utils.IscFileSearch import IscFileSearch 

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
    config = TranscriptionConfig()

    # Get the audio path which could be a directory or a file
    audio_path = config.get('audiodir')
    hf_token = config.get('hf_token')
    transcription_dir = config.get('transcription_dir')

    
    # Initialize a list to store audio file paths
    audio_files = []

    # Check if the audio path is a directory
    if os.path.isdir(audio_path):
        # Use IscFileSearch to get all audio files in the directory
        file_search = IscFileSearch(audio_path)

        # Use the traverse_directory method if it's a directory
        audio_files = file_search.traverse_directory()  
    elif os.path.isfile(audio_path):
        # If it's a single file, append it to the list
        audio_files.append(audio_path)
    else:
        logger.error("The specified audio path is neither a file nor a directory.")
        return 

    if not audio_files:
        logger.error("No audio files found in the specified path.")
        return  

    if hf_token:
        for audio in audio_files:
            logger.info(f"Starting transcription for {audio}")
            # Instantiate the WhisperxTranscriber model with the audio file
            model = WhisperxTranscriber(model_size="small", hf_token=hf_token, audio_files=audio, output_dir=transcription_dir)
            model.transcribe() 
    else:
        logger.error("HF Token not provided.")

if __name__ == '__main__':
    main()