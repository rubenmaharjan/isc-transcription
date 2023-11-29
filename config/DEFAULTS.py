# *************************************************************************************************************************
#   DEFAULTS.py
#       This configuration module defines default values and settings used across an audio transcription system.
#       It includes paths, file extensions, logging configurations, model types, and other constants that provide
#       default behavior for the system's operation.
# -------------------------------------------------------------------------------------------------------------------
#   Usage:
#       The constants defined in this module are imported and used by other modules to ensure consistent default
#       behavior throughout the application. These defaults can be overridden by user-specified configurations.
#
#       Parameters:
#           No parameters are accepted as this module only defines constants.
#
#       Outputs:
#           This module does not generate any outputs. It only provides constants for import into other modules.
#
#   Design Notes:
#   -.  Default paths and filenames are provided for schema files, transcription directories, and log files.
#   -.  Default settings include file extensions for audio files, model types for transcription, and logging configurations.
#   -.  The datetime module is used to timestamp log files.
# ---------------------------------------------------------------------------------------------------------------------
#   last updated: November 2023
#   authors: Bigya Bajarcharya, Mofeoluwa Jide-Jegede
# *************************************************************************************************************************
# ***********************************************
# imports
# ***********************************************

# datetime - module for manipulating dates and times
#    datetime.now - function to get the current date and time

from datetime import datetime

# Default values
DEFAULT_SCHEMA_FILE = 'config/config_schema.xsd'
DEFAULT_TRANSCRIPTION_DIR = 'transcriptions'
DEFAULT_LOG_FILE = 'logs/ISC_DefaultLog.log'
DEFAULT_FILE_EXTENSIONS = ['.mp3', '.wav', '.aac']
DEFAULT_AUDIO = './'  # Default audio file if no other source is specified
ALLOWED_MODEL_TYPES = ['tiny', 'base', 'small', 'medium', 'large']
DEFAULT_MODEL_TYPE = 'base'
DEFAULT_LOGGING_CONFIG = {
    'console_log_output': "stdout",
    'console_log_level': "info",
    'console_log_color': True,
    'logfile_file': datetime.now().strftime('ISC_%H_%M_%d_%m_%Y.log'),
    'logfile_log_level': "debug",
    'logfile_log_color': False,
    'logfile_path': "logs"
}
DEFAULT_XML_PATH = "./config/dev_config.xml"
DEFAULT_WHISPER_CONFIGS = {
        'library': 'whisper',
        'audiodir': './sample/Sample.mp3',
        'transcription_dir': './transcriptions',
        'model_type': 'medium',
        'verbosity': 'true',
        'hf_token': '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',
        'extensions': "['mp3', 'wav']"
    }
