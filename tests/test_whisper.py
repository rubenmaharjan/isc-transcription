import unittest

from src.transcribe.TranscriberFactory import TranscribeFactory
from src.transcribe.models.Transcribe import Transcribe

class TestLogging(unittest.TestCase):

    def setUp(self):
        self.transcribe = TranscribeFactory.load_class("Whisper")

    def test_whisper(self):
        self.assertIsInstance(self.transcribe, Transcribe)

    def test_transcription(self):
        self.transcribe.setup(model_size='tiny', audio='/Users/rubenmaharjan/Documents/ETSU/capstone/sem2/code/isc/ted.mp3', output_file_path="hello.txt").transcribe()

if __name__ == '__main__':
    unittest.main()

