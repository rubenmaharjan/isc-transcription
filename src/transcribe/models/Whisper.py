from src.transcribe.models.Transcribe import Transcribe
from whisper import load_model
import logging

#  get the root logger
logger = logging.getLogger()

class Whisper(Transcribe):
    """
    A subclass of the Transcribe class that transcribes audio using the Whisper speech recognition library.
    """

    def setup(self, model_size, audio, output_file_path):
        """
        Initializes the Whisper object with the specified model size, audio data, and output file path.

        :param model_size: The size of the Whisper model to use for transcription.
        :param audio: The audio data to transcribe.
        :param output_file_path: The path of the file to write the transcription text to.
        """
        self.model_size = model_size
        self.audio = audio 
        self.output_file_path = output_file_path
        return self

    def transcribe(self):
        """
        Transcribes the audio using the loaded Whisper model and writes the transcription to a file.

        :return: The transcription text as a string.
        """
        logger.info(f"Loading {self.model_size} model")
        model = load_model(self.model_size)
        logger.info("Starting transcription")
        result = model.transcribe(self.audio, fp16=False)
        logger.info("Finished transcription")

        logger.info(f"Writing transcription to file: {self.output_file_path}")
        with open(self.output_file_path, "w+") as output_file:
            output_file.write(result['text'])
        logger.info("Finished writing transcription to file")

        return result['text']
