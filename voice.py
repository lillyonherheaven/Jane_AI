"""
Jane-AI- High-Fidelity Voice & Audio Streamer
Module: voice.py
Description: Pygame mixer audio channel streamer with RVC (Retrieval-based Voice Conversion)
voice cloning bridge and sound-effects feedback for listening/thinking/success events.
"""

import os
import time
from pathlib import Path
from typing import Optional


class LocalVoiceStreamer:
    """
    Manages custom voice persona playback and interface audio chime feedback via Pygame.
    """

    def __init__(self):
        self.mixer_initialized = False
        self.rvc_model_path: Optional[str] = None
        self._init_mixer()

    def _init_mixer(self):
        """Initializes Pygame audio mixer in 44.1kHz stereo mode."""
        try:
            import pygame
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.mixer_initialized = True
        except Exception as e:
            print(f"[Voice Streamer Warning] Pygame mixer init note: {e}")
            self.mixer_initialized = False

    def play_chime(self, event_type: str = "activate"):
        """
        Plays subtle UI sound cues (activate, thinking, tool_execute, error).
        """
        if not self.mixer_initialized:
            return

        try:
            import pygame
            # Generates procedural beep or loads audio cue if available
            sound_dir = Path.home() / ".jane_ai" / "sounds"
            target_sound = sound_dir / f"{event_type}.wav"
            if target_sound.exists():
                sound = pygame.mixer.Sound(str(target_sound))
                sound.set_volume(0.4)
                sound.play()
        except Exception as e:
            print(f"[Voice Chime Error]: {e}")

    def stream_rvc_audio(self, wav_path: str):
        """Streams converted RVC audio file to the local speakers."""
        if not self.mixer_initialized or not os.path.exists(wav_path):
            return

        try:
            import pygame
            pygame.mixer.music.load(wav_path)
            pygame.mixer.music.set_volume(0.9)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.05)
        except Exception as e:
            print(f"[Voice Stream Error]: {e}")


# Global voice streamer instance
voice_streamer = LocalVoiceStreamer()
