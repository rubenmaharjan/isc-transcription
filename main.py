import os
from datetime import datetime
from src.utils.ISCLogWrapper import ISCLogWrapper, logging
from src.transcribe.TranscribeFactory import TranscribeFactory

def main():

    # Set up logging
    isc_log_wrapper = ISCLogWrapper(console_log_output="stdout", console_log_level="info", console_log_color=True,
                           logfile_file=datetime.now().strftime('ISC_%H_%M_%d_%m_%Y.log'), logfile_log_level="debug", logfile_log_color=False, logfile_path="logs")
    if (not isc_log_wrapper.set_up_logging()):
        print("Failed to set up logging, aborting.")
        return 1
    
    logger = logging.getLogger(__name__)

    logger.info("Starting Transcription.")
    logger.info("CWD: " + os.getcwd())
    model = TranscribeFactory.load_class("Whisper")
    audio_files = ['test_audio.m4a']
    model.setup(audio_files)
    model.transcribe()


if __name__ == '__main__':
    main()
