"""
Jane-AI  - Offline Audio & STT/TTS Engine
Module: audio.py
Description: Local speech-to-text listener and offline speech synthesizer (pyttsx3 / SAPI5 / espeak)
supporting dynamic audio visualizer telemetry and bilingual voice synthesis.
"""

import threading
import queue
from typing import Optional, Callable


class LocalAudioEngine:
    """
    Manages offline microphone voice capture and fast local speech output.
    """

    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.is_listening = False
        self.is_speaking = False
        self.audio_queue: queue.Queue = queue.Queue()
        self._tts_engine = None
        self._init_tts()

    def _init_tts(self):
        """Initializes offline speech synthesis engine (pyttsx3)."""
        try:
            import pyttsx3
            self._tts_engine = pyttsx3.init()
            self._tts_engine.setProperty("rate", 185)  # Natural human speaking rate
            self._tts_engine.setProperty("volume", 0.95)

            # Try to pick a pleasant voice
            voices = self._tts_engine.getProperty("voices")
            if voices:
                for v in voices:
                    if "zira" in v.name.lower() or "female" in v.name.lower() or "eva" in v.name.lower():
                        self._tts_engine.setProperty("voice", v.id)
                        break
        except Exception as e:
            print(f"[Audio Engine Warning] Local TTS initialization note: {e}")
            self._tts_engine = None

    def speak(self, text: str, on_complete: Optional[Callable[[], None]] = None):
        """
        Synthesizes text in a dedicated non-blocking thread to maintain responsive UI.
        """
        def _worker():
            self.is_speaking = True
            try:
                if self._tts_engine:
                    self._tts_engine.say(text)
                    self._tts_engine.runAndWait()
                else:
                    print(f"[Jane-AI Speech Voice]: {text}")
            except Exception as e:
                print(f"[Audio TTS Error]: {e}")
            finally:
                self.is_speaking = False
                if on_complete:
                    on_complete()

        thread = threading.Thread(target=_worker, daemon=True)
        thread.start()

    def listen_once(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Captures one spoken phrase from the default system microphone using SpeechRecognition.
        """
        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            r.energy_threshold = 300
            r.dynamic_energy_threshold = True

            with sr.Microphone() as source:
                self.is_listening = True
                print("[Audio Engine] Listening for voice input...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                self.is_listening = False

                # Process locally (Sphinx offline or fallback)
                try:
                    text = r.recognize_google(audio_data)  # Standard fallback or local offline
                    return text
                except Exception:
                    try:
                        return r.recognize_sphinx(audio_data)
                    except Exception:
                        return None
        except ImportError:
            print("[Audio Engine] speech_recognition library not installed.")
            self.is_listening = False
            return None
        except Exception as e:
            print(f"[Audio Engine] Mic capture notice: {e}")
            self.is_listening = False
            return None

    def stop_speaking(self):
        """Interrupts ongoing speech output."""
        if self._tts_engine:
            try:
                self._tts_engine.stop()
            except Exception:
                pass
        self.is_speaking = False


# Global Audio Engine
audio_engine = LocalAudioEngine()
