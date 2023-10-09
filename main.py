import os
import argparse
from datetime import datetime
from src.utils.ISCLogWrapper import ISCLogWrapper, logging
from src.transcribe.TranscribeFactory import TranscribeFactory
from src.utils.TranscriptionConfig import TranscriptionConfig

def setup_logging():
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

def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", help="Specify the input audio file")
    parser.add_argument("--configxml", help="Specify the input xml config file")
    return parser.parse_args()

def get_audio_source(config, cmd_audio, cmd_config, logger):
    if cmd_audio:
        logger.info('Starting transcription with cmd_audio audio directory')
        return cmd_audio
    elif cmd_config:
        if cmd_config.endswith('.xml'):
            try:
                extract_config = TranscriptionConfig(cmd_config)
                if 'audiodir' in extract_config:
                    logger.info('Starting transcription with cmd_config audio directory')
                    return extract_config.get('audiodir')
                else:
                    logger.error("The configuration file does not contain 'audiodir'.")
            except Exception as e:
                logger.error("Error while reading the configuration file:", e)
        else:
            logger.error("Wrong file name or extension for the configuration file.")
    logger.info('Starting transcription with default audio directory')
    return config.get('audiodir')

def main():
    logger = setup_logging()
    
    path1 = os.getcwd()
    path = os.path.join(path1, "config/dev_config.xml")
    config = TranscriptionConfig(path)
    
    args = parse_command_line_args()
    audio = get_audio_source(config, args.audio, args.configxml, logger)

    if audio:
        logger.info("Starting Transcription.")
        logger.info("CWD: " + os.getcwd())
        model = TranscribeFactory.load_class("Whisper")
        model.setup(audio)
        model.transcribe()
    else:
        logger.error("Cannot access audio file")

if __name__ == '__main__':
    main()
