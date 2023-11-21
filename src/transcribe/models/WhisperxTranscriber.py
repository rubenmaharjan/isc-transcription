# *************************************************************************************************************************
#   WhisperxTranscriber.py
#       This module contains the WhisperxTranscriber class, which uses the Whisper speech recognition library to transcribe
#       audio files. It supports batch processing, diarization, and can be adapted for different compute environments.
#       It has now been enhanced with the integration of the IscFileSearch class to handle batch processing of audio files
#       within a directory, in addition to transcribing individual files.
# -------------------------------------------------------------------------------------------------------------------------
#   Usage:
#      from WhisperxTranscriber import WhisperxTranscriber
#      transcriber = WhisperxTranscriber(model_size='base', hf_token='your_hf_token', audio_files='path_to_audio_or_directory')
#      transcriber.transcribe()
#
#      Parameters:
#         model_size - The size of the Whisper model to use (e.g., 'tiny', 'base', 'small', 'medium', 'large')
#         hf_token - Hugging Face authentication token for using models hosted on Hugging Face
#         audio_files - The path to the audio file or directory containing audio files to transcribe
#         batch_size - The number of audio segments to process simultaneously (default=16)
#         compute_type - The type of computation (precision) to use, such as 'int8' or 'float16' (default='int8')
#
#      Outputs:
#         A text file for each input audio file, containing the transcribed text with timestamps and speaker identification.
#         When a directory is provided, it will transcribe all supported audio files within that directory.
#
#   Design Notes:
#   -.  The WhisperxTranscriber is optimized for CPU usage by default but can be configured for GPU.
#   -.  It features a diarization pipeline to distinguish between different speakers within the audio.
#   -.  Outputs include aligned segments with speaker labels to enhance transcript readability.
#   -.  The integration with IscFileSearch allows for efficient handling of multiple audio files within a directory.
# -------------------------------------------------------------------------------------------------------------------------
#   TODO:
#   -.  Add support for GPU-based diarization and transcription for enhanced performance.
#   -.  Improve error handling for unsupported audio formats and failed transcriptions.
#   -.  Provide options for outputting character-level aligned segments.
# -------------------------------------------------------------------------------------------------------------------------
#   last updated: November 2023
#   authors: Ruben Maharjan, Bigya Bajarcharya, Mofeoluwa Jide-Jegede
# *************************************************************************************************************************
# ***********************************************
# imports
# ***********************************************

# os - operating system interface
#    path.basename - get the base name of pathname
#    path.splitext - split the pathname into a pair (root, ext)

# typing - support for type hints
#    List - list type hint support

# whisperx - speech recognition library with diarization support
#    load_audio - function to load audio files into memory
#    DiarizationPipeline - class for performing speaker diarization
#    load_align_model - function to load alignment model
#    align - function to align transcriptions with audio
#    assign_word_speakers - function to assign speakers to words

# IscFileSearch - utility class to search for audio files within a directory
#    IscFileSearch - class for finding audio files with specific extensions

# logging - logging library
#    basicConfig - function to configure the logging
#    getLogger - function to get a logging instance

# subprocess - subprocess management
#    call - run a command in a subprocess

import os
from typing import List
import whisperx
from whisperx import load_audio, DiarizationPipeline, load_align_model, align, assign_word_speakers
from src.utils.IscFileSearch import IscFileSearch 
import logging
import subprocess


# Setup logger for informational messages
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('WhisperxTranscriber')


class WhisperxTranscriber:
    def __init__(self, model_size, hf_token, audio_files, output_dir=None, batch_size=16, compute_type="int8"):
        self.model_size = model_size
        self.hf_token = hf_token
        self.audio_files = audio_files
        self.output_dir = output_dir if output_dir is not None else 'transcription_dir'
        self.batch_size = batch_size
        self.compute_type = compute_type
        self.model = whisperx.load_model("base", device="cpu", compute_type=self.compute_type)

    def transcribe(self):
        logger.info(f"Loading {self.model_size} model")
        diarize_model = DiarizationPipeline(use_auth_token=self.hf_token, device="cpu")

        # Check if the audio_files attribute is a directory or a single file
        if os.path.isdir(self.audio_files):
            file_search = IscFileSearch(self.audio_files)
            audio_files = file_search.traverse_directory()  # Use the IscFileSearch method to list all audio files
        else:
            audio_files = [self.audio_files]  # Wrap the single file in a list for consistent processing

        # Loop through all files to transcribe them
        for audio in audio_files:
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
