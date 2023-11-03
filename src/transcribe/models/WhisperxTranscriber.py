import os
from typing import List
import whisperx
from whisperx import load_audio
from whisperx import DiarizationPipeline
import logging
import subprocess

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class WhisperxTranscriber:
    def __init__(self, model_size: str, hf_token: str, audio_files: str, batch_size: int = 16, compute_type: str = "int8"):
        self.model_size = model_size
        self.hf_token = hf_token
        self.audio_files = audio_files
        self.batch_size = batch_size
        self.compute_type = compute_type
        self.model = whisperx.load_model("base", device="cpu", compute_type=self.compute_type)

    def transcribe(self):
        logger.info(f"Loading {self.model_size} model")
        diarize_model = DiarizationPipeline(use_auth_token=self.hf_token, device="cpu")

         #todo: integrate traversal branch
        audio=self.audio_files
        logger.info(f"Transcribing audio file: {audio}")
        waveform = load_audio(audio)
        result = self.model.transcribe(waveform, batch_size=self.batch_size)
        base_name = os.path.splitext(os.path.basename(audio))[0]
        output_file_path = f"{base_name}.txt"
        logger.info(f"Writing transcription to file: {output_file_path}")

        diarize_segments = diarize_model(audio)
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device='cpu')

        aligned_segments = whisperx.align(result['segments'], model_a, metadata, audio, "cpu", return_char_alignments=False)
        segments_with_speakers = whisperx.assign_word_speakers(diarize_segments, aligned_segments)

        with open(output_file_path, "w+") as output_file:
            for segment in segments_with_speakers["segments"]:
                output_file.write(f"{segment['start']} {segment['end']} {segment['text']}\n")

        logger.info(f"Finished writing transcription to file: {output_file_path}")


        # # Define the base command
        # command = "whisperx" #todo: integrate directory traversal

        # # Define optional flags and their values
        # optional_flags = {
        #     "--compute_type": self.compute_type,
        #     # "--hf_token": self.hf_token,
        #     # "--model": self.model_size,
        #     # "--batch_size": self.batch_size,
        #     # "--output_dir": "output_dir",
        #     # "--language": "en"
        #     # "--diarize": "false"
        # }

        # # Construct the command and its arguments
        # args = [command]
        # for flag, value in optional_flags.items():
        #     if value is not None:
        #         args.extend([flag, value])
        # if self.audio_files:
        #     args.append(self.audio_files)
        # # Run the command using subprocess
        # # try:
        #     completed_process = subprocess.run(args, check=True, stderr=subprocess.PIPE, text=True, shell=True)
        #     print(".......", completed_process.stderr) 
        # # except subprocess.CalledProcessError as e:
        # #     print(f"Error running the command: {e}")