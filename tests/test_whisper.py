import unittest

from src.transcribe.TranscribeFactory import TranscribeFactory
from src.transcribe.models.Transcribe import Transcribe

class TestWhisper(unittest.TestCase):

    def setUp(self):
        '''
        Define a setup method that initializes variables needed for tests
        '''
        self.whisper = TranscribeFactory.load_class("Whisper")
        self.audio_files = ["tests/files/test_audio.m4a"]
        self.model_size = "tiny"

    def test_whisper(self):
        '''
        Define a test method that checks if whisper object is an instance of Transcribe
        '''
        self.assertIsInstance(self.whisper, Transcribe)

    def test_transcription(self):
        '''
        Define a test method that checks if transcription is successful and result matches the output file
        '''
        self.whisper.setup(audio_files=self.audio_files)
        result = self.whisper.transcribe()
        with open(self.output_file_path, "r") as output_file:
            transcription = output_file.read()
        self.assertEqual(result, transcription)
    
    def test_transcription_text(self):
        '''
        Define a test method that checks if the output of the transcribe method is a string and is not empty
        '''
        self.whisper.setup(audio_files=self.audio_files)
        result = self.whisper.transcribe()
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")


if __name__ == '__main__':
    unittest.main()

