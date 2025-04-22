from TTS.api import TTS
from text_generator import text
import torch

def generate_speech(text: str, output_path: str, model_name: str, speaker: str) -> None:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS(model_name=model_name, progress_bar=True).to(device)
    tts.tts_to_file(
        text=text,
        file_path=output_path,
        speaker=speaker,
        split_sentences=True
    )

if __name__ == "__main__":
    generate_speech(text=text,
                    output_path="output/audio.wav",
                    model_name="tts_models/en/vctk/vits",
                    speaker="p228")
