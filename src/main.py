import os
import sys
from logging_wrapper import set_up_logging, logging
from hell import hell

def main():

    # Set up logging
    script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if (not set_up_logging(console_log_output="stdout", console_log_level="info", console_log_color=True,
                           logfile_file=script_name + ".log", logfile_log_level="debug", logfile_log_color=False,
                           log_line_template="%(color_on)s[%(created)d] [%(threadName)s] [%(levelname)-8s] [%(filename)s:%(lineno)d] %(message)s%(color_off)s")):
        print("Failed to set up logging, aborting.")
        return 1

    # Log some messages
    logging.debug("Debug message")
    logging.info("Info message")
    logging.warning("Warning message")
    logging.error("Error message")
    logging.critical("Critical message")


main()
