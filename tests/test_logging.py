import unittest
import logging
import os
import sys
import tempfile
from io import StringIO
from unittest.mock import patch

from src.utils.logging_wrapper import ISCLogWrapper 


class TestISCLogWrapper(unittest.TestCase):

    def test_set_up_logging(self):

        # Set up test variables
        console_log_output = "stdout"
        console_log_level = "INFO"
        console_log_color = True
        logfile_file = "test.log"
        logfile_path = tempfile.gettempdir()
        logfile_log_level = "DEBUG"
        logfile_log_color = False

        # Instantiate the class
        log_wrapper = ISCLogWrapper(console_log_output, console_log_level, console_log_color, 
                                    logfile_file, logfile_path, logfile_log_level, logfile_log_color)

        # Call the set_up_logging method and assert that it returns True
        self.assertTrue(log_wrapper.set_up_logging())

        # Check that the logger was created and has the correct log level
        logger = logging.getLogger()
        self.assertEqual(logger.level, logging.DEBUG)

        # Check that the console handler was created and added to the logger
        console_handler = logger.handlers[0]
        self.assertIsInstance(console_handler, logging.StreamHandler)
        self.assertEqual(console_handler.stream, sys.stdout)
        self.assertEqual(console_handler.level, logging.INFO)

        # Check that the console formatter was created and set on the console handler
        console_formatter = console_handler.formatter
        self.assertIsInstance(console_formatter, logging.Formatter)
        self.assertEqual(console_formatter._fmt, "%(color_on)s[%(asctime)s.%(msecs)03d] [%(threadName)s] [%(levelname)-8s] [%(filename)s:%(lineno)d] %(message)s%(color_off)s")
        self.assertTrue(console_formatter.color)

        # Check that the log file handler was created and added to the logger
        logfile_handler = logger.handlers[1]
        self.assertIsInstance(logfile_handler, logging.FileHandler)
        self.assertEqual(logfile_handler.baseFilename, os.path.join(logfile_path, logfile_file))
        self.assertEqual(logfile_handler.level, logging.DEBUG)

        # Check that the log file formatter was created and set on the log file handler
        logfile_formatter = logfile_handler.formatter
        self.assertIsInstance(logfile_formatter, logging.Formatter)
        self.assertEqual(logfile_formatter._fmt, "%(color_on)s[%(asctime)s.%(msecs)03d] [%(threadName)s] [%(levelname)-8s] [%(filename)s:%(lineno)d] %(message)s%(color_off)s")
        self.assertFalse(logfile_formatter.color)

        # Clean up the log file
        os.remove(os.path.join(logfile_path, logfile_file))

    def test_set_up_logging_invalid_output(self):

        # Set up test variables with an invalid console log output
        console_log_output = "invalid_output"
        console_log_level = "INFO"
        console_log_color = True
        logfile_file = "test.log"
        logfile_path = tempfile.gettempdir()
        logfile_log_level = "DEBUG"
        logfile_log_color = False

        # Instantiate the class
        log_wrapper = ISCLogWrapper(console_log_output, console_log_level, console_log_color, 
                                    logfile_file, logfile_path, logfile_log_level, logfile_log_color)

        # Use a context manager to capture stdout
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            # Call the set_up_logging method and assert that it returns False
            self.assertFalse(log_wrapper.set_up_logging())
            # Assert that the correct error message was printed to stdout
            self.assertIn("Failed to set console output: invalid output:", fake_stdout.getvalue())

        os.remove(os.path.join(logfile_path, logfile_file))

if __name__ == '__main__':
    unittest.main()