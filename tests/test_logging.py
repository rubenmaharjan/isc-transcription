import unittest
from datetime import datetime
from src.utils.ISCLogWrapper import ISCLogWrapper 

class TestLogging(unittest.TestCase):

    def setUp(self):
        self.isc_log_wrapper = ISCLogWrapper(console_log_output="stdout", console_log_level="info", console_log_color=True,
                               logfile_file="logger_test" + datetime.now().strftime('mylogfile_%H_%M_%d_%m_%Y.log'), logfile_log_level="debug", logfile_log_color=False, logfile_path="logs")

    def test_logging_setup(self):
        self.assertTrue(self.isc_log_wrapper.set_up_logging())


if __name__ == '__main__':
    unittest.main()

