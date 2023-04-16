import os
import sys
from utils.logging_wrapper import ISCLogWrapper, logging


def main():

    # Set up logging
    script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    isc_log_wrapper = ISCLogWrapper(console_log_output="stdout", console_log_level="info", console_log_color=True,
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


main()
