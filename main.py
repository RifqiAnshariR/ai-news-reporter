import pygame
import time
import wave
import json
import textwrap
import cv2
from typing import List, Tuple, Dict
from text_generator import text

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BORDER_WIDTH = 10
VISEME_PADDING = 10
SUB_BG_PADDING = 10
FPS = 30

def load_config(filepath: str = "config.json") -> dict:
    with open(filepath, "r") as file:
        return json.load(file)

def load_phonemes(filepath: str) -> List[Tuple[float, float, str]]:
    phonemes: List[Tuple[float, float, str]] = []
    with open(filepath, 'r') as file:
        lines = [line.strip().split('\t') for line in file.readlines()]

    for i in range(len(lines) - 1):
        if len(lines[i]) == 2 and len(lines[i + 1]) == 2:
            start = float(lines[i][0])
            end = float(lines[i + 1][0])
            phoneme = lines[i][1]
            phonemes.append((start, end, phoneme))
    return phonemes

def load_visemes(mapping: Dict[str, str]) -> Dict[str, pygame.Surface]:
    visemes: Dict[str, pygame.Surface] = {}
    for viseme_name in set(mapping.values()):
        image_path = f"assets/talking/{viseme_name}.png"
        visemes[viseme_name] = pygame.image.load(image_path)
    return visemes

def split_text_by_duration(text: str, max_chars: int = 35) -> Tuple[List[str], float]:
    with wave.open("output/audio.wav", "rb") as wf:
        duration = wf.getnframes() / wf.getframerate()

    chunks = textwrap.wrap(text, max_chars, break_long_words=False)
    seconds_per_chunk = duration / len(chunks)
    return chunks, seconds_per_chunk

def get_current_subtitle(chunks: List[str], seconds_per_chunk: float, current_time: float) -> str:
    index = int(current_time // seconds_per_chunk)
    return chunks[index] if index < len(chunks) else ""

def get_current_viseme(phonemes: List[Tuple[float, float, str]], mapping: Dict[str, str], current_time: float) -> str:
    for start, end, ph in phonemes:
        if start <= current_time <= end:
            return mapping.get(ph, 'b_talk_1')
    return 'b_talk_1'

def add_rectangle(surface: pygame.Surface, x: int, y: int, width: int, height: int, color: Tuple[int, int, int], border_width: int) -> None:
    pygame.draw.rect(surface, color, (x, y, width, height), border_width)

def main() -> None:
    config = load_config()
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    screen_width = config["screen"]["width"]
    screen_height = config["screen"]["height"]
    screen = pygame.display.set_mode((screen_width, screen_height))
    phoneme_to_viseme = config["phoneme_to_viseme"]

    pygame.display.set_caption("AI News Reporter")
    phonemes = load_phonemes("output/phonemes.dat")
    viseme_images = load_visemes(phoneme_to_viseme)
    subtitle_chunks, chunk_duration = split_text_by_duration(text)
    font = pygame.font.Font("./assets/static/OpenSans-Regular.ttf", 25)
    pygame.mixer.music.load("output/audio.wav")
    content_video = cv2.VideoCapture("./assets/content/video_1.mp4")

    start_time = time.time()
    pygame.mixer.music.play()
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)
        current_time = time.time() - start_time

        ret, frame = content_video.read()
        if ret:
            frame = cv2.resize(frame, (screen_width, screen_height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            content_video_surface = pygame.surfarray.make_surface(frame)
            screen.blit(content_video_surface, (0, 0))

        add_rectangle(screen, 0, 0, screen_width, screen_height, BLACK, BORDER_WIDTH)   # Border

        viseme_name = get_current_viseme(phonemes, phoneme_to_viseme, current_time)
        current_viseme = viseme_images[viseme_name]
        screen.blit(current_viseme,
                    (screen_width - current_viseme.get_width() - VISEME_PADDING,
                     screen_height - current_viseme.get_height() - VISEME_PADDING))

        current_subtitle = get_current_subtitle(subtitle_chunks, chunk_duration, current_time)
        subtitle_surface = font.render(current_subtitle, True, WHITE)
        subtitle_background = subtitle_surface.get_rect(center=(screen_width // 2, screen_height // 2))
        add_rectangle(screen,
                      subtitle_background.x - SUB_BG_PADDING,
                      subtitle_background.y - SUB_BG_PADDING,
                      subtitle_background.width + 2 * SUB_BG_PADDING,
                      subtitle_background.height + 2 * SUB_BG_PADDING,
                      BLACK, 0)
        screen.blit(subtitle_surface, subtitle_background)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not pygame.mixer.music.get_busy():   # Stop when audio finishes
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
