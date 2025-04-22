import subprocess
import sys

def generate_phonemes(rhubarb_path: str, audio_path: str, output_path: str) -> None:
    try:
        subprocess.run(
            [rhubarb_path, "-o", output_path, audio_path],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print("Failed to generate phonemes:", e)
        sys.exit(1)

if __name__ == "__main__":
    generate_phonemes(rhubarb_path="C:/Rhubarb-Lip-Sync-1.14.0-Windows/rhubarb.exe",
                      audio_path="output/audio.wav",
                      output_path="output/phonemes.dat")
