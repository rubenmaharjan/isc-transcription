import os
from typing import List
import whisperx
from whisperx import load_model
from whisperx.audio import load_audio

class Whisperx:
    def __init__(self, model_size: str, audio_files: List[str], batch_size: int = 16, compute_type: str = "int8"):
        self.model_size = model_size
        self.audio_files = audio_files
        self.batch_size = batch_size
        self.compute_type = compute_type
        self.model = whisperx.load_model(self.model_size, device="cpu", compute_type=self.compute_type)

    def transcribe(self):
        for audio in self.audio_files:
            waveform = load_audio(audio)
            result = self.model.transcribe(waveform, batch_size=self.batch_size)
            base_name = os.path.splitext(os.path.basename(audio))[0]
            output_file_path = f"{base_name}.txt"
            
            with open(output_file_path, "w+") as output_file:
                for segment in result["segments"]:
                    output_file.write(f"{segment['start']} {segment['end']} {segment['text']}\n")

