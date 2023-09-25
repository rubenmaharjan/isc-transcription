import os
from datetime import datetime
from src.utils.ISCLogWrapper import ISCLogWrapper, logging
from src.transcribe.TranscribeFactory import TranscribeFactory
from src.utils.TranscriptionConfig import TranscriptionConfig

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


    # create a TranscriptionConfig object and read the XML file
    path1 = os.getcwd()
    # print("Tpath1: ", path1)
    path = os.path.join(path1, "src/config_file/mock_data/config.xml")

    config = TranscriptionConfig(path)

    # get all the key-value pairs of config file
    model = config.get_all()
    print("Model: ", model)

if __name__ == '__main__':
    main()
