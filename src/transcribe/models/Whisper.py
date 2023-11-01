# import os
# from typing import List
# import whisperx
# from whisperx import load_model
# from whisperx.audio import load_audio

# class Whisperx:
#     def __init__(self, model_size: str, audio_files: List[str], batch_size: int = 16, compute_type: str = "int8"):
#         self.model_size = model_size
#         self.audio_files = audio_files
#         self.batch_size = batch_size
#         self.compute_type = compute_type
#         self.model = whisperx.load_model(self.model_size, device="cpu", compute_type=self.compute_type)

#     def transcribe(self):
#         for audio in self.audio_files:
#             waveform = load_audio(audio)
#             result = self.model.transcribe(waveform, batch_size=self.batch_size)
#             base_name = os.path.splitext(os.path.basename(audio))[0]
#             output_file_path = f"{base_name}.txt"
            
#             with open(output_file_path, "w+") as output_file:
#                 for segment in result["segments"]:
#                     output_file.write(f"{segment['start']} {segment['end']} {segment['text']}\n")


import os
import gc
from typing import List
import whisperx
from whisperx import load_model
from whisperx.audio import load_audio
# from diarization_pipeline import DiarizationPipeline  # Assuming the necessary import for DiarizationPipeline
import configparser
import logging

# setup logger
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

class Whisperx:
    def __init__(self, model_size: str, hf_token: str, audio_files: List[str], batch_size: int = 16, compute_type: str = "int8"):
        self.model_size = model_size
        self.hf_token = hf_token
        self.audio_files = audio_files
        self.batch_size = batch_size
        self.compute_type = compute_type
        self.model = whisperx.load_model(self.model_size, device="cpu", compute_type=self.compute_type)

    def transcribe(self):
        logger.info(f"Loading {self.model_size} model")
        diarize_model = whisperx.DiarizationPipeline(use_auth_token=self.hf_token, device="cpu")

        for audio in self.audio_files:
            logger.info(f"Transcribing audio file: {audio}")
            waveform = load_audio(audio)
            result = self.model.transcribe(waveform, batch_size=self.batch_size)
            base_name = os.path.splitext(os.path.basename(audio))[0]
            output_file_path = f"{base_name}.txt"
            logger.info(f"Writing transcription to file: {output_file_path}")

            diarize_segments = diarize_model(audio)
            aligned_segments = whisperx.align(result['segments'], diarize_model, None, audio, "cpu", return_char_alignments=False)["segments"]  # Assuming model_a should be diarize_model and metadata should be None
            segments_with_speakers = assign_word_speakers(diarize_segments, aligned_segments)  # Assuming necessary import for assign_word_speakers

            with open(output_file_path, "w+") as output_file:
                for segment in segments_with_speakers:
                    # Assuming segments_with_speakers is a list of segments, and each segment is a dictionary with 'start', 'end', and 'text' keys.
                    output_file.write(f"{segment['start']} {segment['end']} {segment['text']}\n")

            logger.info(f"Finished writing transcription to file: {output_file_path}")
