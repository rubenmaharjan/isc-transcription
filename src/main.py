import os
import sys
from utils.logging_wrapper import ISCLogWrapper, logging
# main class for configuration file
from config_file.TranscriptionConfig import TranscriptionConfig


def main():

    # Set up logging
    script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    isc_log_wrapper = ISCLogWrapper(console_log_output="stdout", console_log_level="debug", console_log_color=True,
                                    logfile_file=script_name + ".log", logfile_log_level="debug", logfile_log_color=False, logfile_path="logs")
    if (not isc_log_wrapper.set_up_logging()):
        print("Failed to set up logging, aborting.")
        return 1

    # Log some messages
    logging.debug("Debug message")
    logging.info("Info message")
    logging.warning("Warning message")
    logging.error("Error message")
    logging.critical("Critical message")

    # create a TranscriptionConfig object and read the XML file
    path1 = os.getcwd()
    # print("Tpath1: ", path1)
    path = os.path.join(path1, "src/config_file/mock_data/config.xml")

    # print("Path:",path)
    config = TranscriptionConfig(path)

    # get the value for the 'model' key
    config.delete_key('test/level/one')
    model = config.get_all()
    print("Model: ", model)

    config.save_changes()


main()
