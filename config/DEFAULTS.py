from datetime import datetime

# Default values
DEFAULT_SCHEMA_FILE = 'config/config_schema.xsd'
DEFAULT_TRANSCRIPTION_DIR = 'transcriptions'
DEFAULT_LOG_FILE = 'logs/ISC_DefaultLog.log'
DEFAULT_FILE_EXTENSIONS = ['.mp3', '.wav', '.aac']
DEFAULT_AUDIO = 'sample/Sample.mp3'  # Default audio file if no other source is specified
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
        'transcriptiondir': './transcriptiondir',
        'model_type': 'medium',
        'verbosity': 'true',
        'hf_token': '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',
        'extensions': "['mp3', 'wav']"
    }
