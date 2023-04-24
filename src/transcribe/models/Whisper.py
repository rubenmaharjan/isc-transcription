from src.transcribe.models.Transcribe import Transcribe
from whisper import load_model
import logging
from typing import List

#  get the logger
logger = logging.getLogger(__name__)

class Whisper(Transcribe):
    """
    A subclass of the Transcribe class that transcribes audio using the Whisper speech recognition library.
    """

    def setup(self, audio_files: List[str]) -> Transcribe:
        """
        Initializes the Whisper object with the specified model size, audio data, and output file path.

        :param model_size: The size of the Whisper model to use for transcription.
        :param audio_files: The list of audio files to transcribe.
        :param model: The path of the file to write the transcription text to.

        :return: self
        """
        # TODO Read from config
        self.model_size = "tiny"
        self.audio_files = audio_files 
        self.model = load_model(self.model_size, in_memory=True)
        return self

    def transcribe(self):
        """
        Transcribes the audio using the loaded Whisper model and writes the transcription to a file.

        :return: None
        """
        logger.info(f"Loading {self.model_size} model")
        for audio in self.audio_files:
            logger.info("Starting transcription")
            result = self.model.transcribe(audio, fp16=False)
            logger.info("Finished transcription")

            # TODO Use the utils to get the output file path
            #logger.info(f"Writing transcription to file: {self.output_file_path}")
            with open(audio.split('.')[0]+".txt", "w+") as output_file:
                output_file.write(result['text'])
            logger.info("Finished writing transcription to file")
