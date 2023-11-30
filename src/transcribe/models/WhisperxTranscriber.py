# TODO Request – look to factor my changes, Mofe's updated doc, and support for model parameterization into whisperXTranscriber.py.
# TODO Specific requests for changes:
# •	If Main is invoking IscFileSearch, you don't need to invoke it here.
# •	Upgrade to support optional diarization
# •	Upgrade to support GPU-based transcription.  That was important for optimizing performance on my Dell 7770.

# *************************************************************************************************************************
#   WhisperxTranscriber.py – Transcribe and diarize recordings
# *************************************************************************************************************************
#
#   Usage:
#       This module contains the WhisperxTranscriber class, which uses the WhisperX speech recognition library to transcribe
#       and optionally diarize 
#       audio files. WhisperX is a third party library that augments OpenAI's transcription library, 
#       Whisper, with support for diarization.  The WhisperxTranscriber class It supports uses the IscFileSearch class to support the batch 
#       processing, diarization, and can be adapted for different compute environments.
#       It has now been enhanced with the integration of the IscFileSearch class to handle batch processing of audio files 
#       wwithin a directory, in addition to transcribing individual files.
# -------------------------------------------------------------------------------------------------------------------------#  
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
#   Design and Implementation Notes:
#   -.  The WhisperxTranscriber uses WhisperX, a library isthat is downloadable  available from at https://github.com/m-bain/whisperX.  
#       -.  WhisperX isWhisperX is a third party library that augments OpenAI's transcription library, 
#       Whisper transcription service, withto support for diarization.
#            -.  It features a diarization pipeline to distinguish between#  different speakers within the audio.
#            -.  Outputs include aligned segments with speaker labels to enhance transcript readability.
#       -.  To access it, Users of WhisperX prospective users must create an account at that URL and requestobtain a keya token.
#   -.  The WhisperxTranscriber is optimized for CPU usage by default but can be configured for GPU.
#   -.  It features a diarization pipeline to distinguish between#  different speakers within the audio.
#   -.  Outputs include aligned segments with speaker labels to enhance transcript readability.
#   -.  The integration with IscFileSearch allows for efficient handling of multiple audio files within a directory.
# -------------------------------------------------------------------------------------------------------------------------
#   TODO:
#   -.  Parameterize the model type.
#   -.  Add support for GPU-based diarization and transcription for enhanced performance.
#   -.  Improve error handling for unsupported audio formats and failed transcriptions.
#   -.  Provide options for outputting character-level aligned segments.
# -------------------------------------------------------------------------------------------------------------------------
#   last updated: November 2023
#   authors: Ruben Maharjan, Bigya Bajarcharya, Mofeoluwa Jide-Jegede, Phil Pfeiffer
# *************************************************************************************************************************

# ***********************************************
# imports
# ***********************************************

# config.DEFAULTS - module containing default configuration values for the logging setup
#    DEFAULT_WHISPER_CONFIG - a dictionary containing the default logging configuration settings
# IscFileSearch - utility class to search for audio files within a directory
#    IscFileSearch - class for finding audio files with specific extensions
# os - operating system interface
#    path.basename - get the base name of pathname
#    path.splitext - split the pathname into a pair (root, ext)

# logging - logging library
#    basicConfig - function to configure the logging
#    getLogger - function to get a logging instance
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

# pathlib - File system path manipulation
#    PurePath.parts - split file path into constituent segments

from config.DEFAULTS import DEFAULT_WHISPER_CONFIG
import os
from typing import List
import whisperx
from whisperx import load_audio, DiarizationPipeline, load_align_model, align, assign_word_speakers
from src.utils.IscFileSearch import IscFileSearch 
import logging
import pathlib

# ***************************************************************************************************************************

#  logging support
# ***************************************************************************************************************************

# Setup logger for informational messages
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('WhisperxTranscriber')

# ***************************************************************************************************************************
# WhisperxTranscriber:
#    Use the WhisperX library to transcribe and diarize a recording
#
#      Key methods:Parameters:
#     __init__():  create an instance of the diarizer, overlaying parameters from config on the defaults
#         Parameters:
#            config_dict: a dictionary that defines the following parameters"
#               batch_size – The number of audio segments to process simultaneously
#               compute_type – The type of computation (precision) to use, such as 'int8' or 'float16'
#               hf_token – Hugging Face authentication token for using models hosted on Hugging Face
#               device – device to support (default = 'cpu')
#               diarize – specify whether to diarize as well as transcribe (default = True)
#           config_dict: a dictionary that defines the following parameters"
#               model_size – The size of the Whisper model to use (e.g., 'tiny', 'base', 'small', 'medium', 'large')
#             hf_token – Hugging Face authentication token for using models hosted on Hugging Face
#             audio_files - The path to the audio file or directory containing audio files to transcribe
#             transcription_dir –<what exactly will this directory contain??>
#               output_dir –<what exactly will this directory contain??>
#               transcription_dir –<what exactly will this directory contain??>
#             batch_size – The number of audio segments to process simultaneously (default=16)
#             compute_type – The type of computation (precision) to use, such as 'int8' or 'float16' (default='int8')
#             device – device to support (default = 'cpu')
#             diarize – specify whether to diarize as well as transcribe (default = True)#           logger: a logging object for capturing status messages
#
#       transcribe()
#         Parameters:
#           audio – file to transcribe

#
#           Outputs:
#           A text file for audio, containing the transcribed text with timestamps and speaker identification.
#           When a directory is provided, it will transcribe all supported audio files within that directory.
# ***************************************************************************************************************************
#
class WhisperxTranscriber:
    def __init__(self, config_dict, logger):
        #  set operating parameters
        #
        self.audio_files        = config_dict.get('audio_files')
        self.batch_size         = config_dict.get('batch_size', DEFAULT_WHISPER_CONFIG['batch_size'])
        self.compute_type       = config_dict.get('compute_type', DEFAULT_WHISPER_CONFIG['compute_type'])
        self.device             = config_dict.get('device', DEFAULT_WHISPER_CONFIG['device'])
        self.enable_diarization = config_dict.get('diarize', DEFAULT_WHISPER_CONFIG['diarize'])
        self.hf_token           = config_dict.get('hf_token', DEFAULT_WHISPER_CONFIG['hf_token'])
        self.model_size         = config_dict.get('model_size', DEFAULT_WHISPER_CONFIG['model_size'])
        self.output_dir         = config_dict.get('output_dir', DEFAULT_WHISPER_CONFIG['transcription_dir'])
        self.transcription_dir  = config_dict.get('transcription_dir', DEFAULT_WHISPER_CONFIG['transcription_dir'])
       
        self.logger = logger
        #
        #  set up operations
        #
        self.logger.info(f"Loading {self.model_size} model")
        self.model = whisperx.load_model(self.model_size, self.device, compute_type=self.compute_type)

        if self.enable_diarization:
            diarize_model = DiarizationPipeline(use_auth_token=self.hf_token, device=self.device)

# TODO please redo the logic to make diarization optional and to support GPU use
    def transcribe(self, audio_file):
        logger.info(f"Loading {self.model_size} model")
        diarize_model = DiarizationPipeline(use_auth_token=self.hf_token, device=self.device)

        # Check if the audio_files attribute is a directory or a single file
        if os.path.isdir(self.audio_files):
            file_search = IscFileSearch(self.audio_files)
            audio_files = file_search.traverse_directory()  # Use the IscFileSearch method to list all audio files
        else:
            audio_files = [self.audio_files]  # Wrap the single file in a list for consistent processing

        # Loop through all files to transcribe them
        for audio in audio_files:
            self.logger.info(f"Transcribing audio file: {audio}")
            waveform = load_audio(audio)
            result = self.model.transcribe(waveform, batch_size=self.batch_size)

# TODO If you're specifying output_dir as a parameter, why are you not providing an option to set the file path to output_dir or transcription_dir?
# try this
            p = pathlib.PurePath(os.path.abspath(audio)).parts
            output_dir = p[0] + self.transcription_dir
            base_name  = (p[2:][:-1])+(os.path.splitext(p[-1])[0],)
            output_filename = '/'.join( output_dir + base_name)           
            self.logger.info(f"Writing transcription to directory {output_dir} as {base_name}.*")

# TODO the following should only be needed if diarization is supported, right?
            if self.enable_diarization:       
                self.logger.info(f"Diarizing audio file: {audio}")
                diarize_segments = diarize_model(audio)

                model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=self.device)

                aligned_segments = whisperx.align(result['segments'], model_a, metadata, audio, self.device, return_char_alignments=False)
                segments_with_speakers = whisperx.assign_word_speakers(diarize_segments, aligned_segments)

    #TODO: Check for and log write errors!

                with open(output_filename, "w+") as output_file:
                    for segment in segments_with_speakers["segments"]:
                        output_file.write(f"{segment['start']} {segment['end']} {segment['text']}\n")

                self.logger.info(f"Finished writing transcription to file: {output_filename}")

            else:
                self.logger.info(f"Transcribing audio file without diarization: {audio}")
                model = whisperx.load_model(self.model_size, self.device, compute_type=self.compute_type)
                result = model.transcribe(audio, batch_size=self.batch_size)
                with open(output_filename, "w+") as output_file:
                    for segment in result["segments"]:
                        output_file.write(f"{segment['start']} {segment['end']} {segment['text']}\n")

                self.logger.info(f"Finished writing non-diarized transcription to file: {output_filename}")
                