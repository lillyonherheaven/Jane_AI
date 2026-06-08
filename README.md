# Jane-AI

> **Secure Arabic AI Voice Assistant** — A local, privacy-first AI agent with realistic voice, RAG memory, PC control, and AES-256 encryption.

[![Version](https://img.shields.io/badge/version-2.0--HARDENED-34d399?style=flat-square)](.)
[![Security](https://img.shields.io/badge/security-AES--256%20%2B%20Sandbox-f43f5e?style=flat-square)](.)
[![Language](https://img.shields.io/badge/language-Python%203.10%2B-00e5ff?style=flat-square)](.)
[![Model](https://img.shields.io/badge/model-Llama%203.2%20%28local%29-a78bfa?style=flat-square)](.)

---

## Overview

Jane-AI is a fully offline, Arabic-first AI assistant that runs on your local machine. It combines a local LLM (via Ollama), real-time speech recognition, RVC voice synthesis, document-aware memory (RAG), PC automation, and a hardened security layer — all in a custom desktop GUI.

---

## Architecture — 6 Phases

### Phase 1 — Core MVP `brain.py` + `audio.py`
The foundation: a conversational AI loop with Arabic speech input and TTS output.
- **Ollama + Llama 3.2** for local inference
- **SpeechRecognition** for microphone input (Arabic `ar-EG`)
- **pyttsx3** for offline TTS
- **Fix #1:** Silent retry on empty/unrecognized audio — no TTS spam on failed input

### Phase 2 — Realistic Voice `voice.py`
Upgrades TTS to a human-sounding RVC voice model.
- **gTTS** generates intermediate MP3
- **RVC** applies a trained voice model for natural output
- **Fix #2:** Cross-platform audio playback via `pygame.mixer` — replaces Linux-only `aplay`

### Phase 3 — RAG Memory `rag.py` + `memory.py`
Gives Jane knowledge from your own documents.
- **LangChain** loads and chunks PDFs from `./Knowledge_Base`
- **ChromaDB** stores and retrieves vector embeddings
- **OllamaEmbeddings** for fully local vector generation
- Every query is automatically augmented with relevant document context

### Phase 4 — Agent & GUI `agent.py` + `gui.py`
Enables PC control and wraps everything in a desktop UI.
- **PyAutoGUI + psutil** for screenshots, system info, app launching
- **CustomTkinter** dark-mode GUI with animated audio waveform
- **Fix #4:** Thread-safe GUI updates — all worker-thread results are routed back to the main thread via `self.after()` callbacks

### Phase 5 — Security Layer `security.py` + `sandbox.py` + `crypto.py` + `secure_brain.py`
Hardens Jane against prompt injection, path traversal, and data leaks.

| Module | Protection |
|---|---|
| `security.py` | Prompt injection regex defense, destructive command detection, input sanitization |
| `sandbox.py` | Filesystem sandboxing — zone-restricted read/write, extension allowlist |
| `crypto.py` | AES-256 file encryption at rest via PBKDF2 key derivation (480,000 iterations) |
| `secure_brain.py` | Full secure pipeline: validate → confirm → execute → audit log |

- **Fix #3:** Absolute path bypass hardened — `Path(path).name` strips any absolute prefix before joining with the sandbox root

### Phase 6 — Launch `requirements.txt`
Final packaging for submission to ITIDA Smart Village.
- Clean dependency list
- 2-minute demo video
- IP registration ready

---

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Install & start Ollama
```bash
# https://ollama.com
ollama pull llama3.2
```

### 3. Set up encryption (first run only)
```bash
python crypto.py
```

### 4. Build the knowledge base
Add your PDF files to `./Knowledge_Base/`, then:
```bash
python rag.py
```

### 5. Launch Jane
```bash
python gui.py
```

---

## Project Structure

```
jane-ai/
 brain.py # Core LLM interface (Ollama)
 audio.py # Speech input + TTS output
 voice.py # RVC human voice pipeline
 rag.py # PDF loading + ChromaDB indexing
 memory.py # RAG-augmented brain
 agent.py # PC control tools
 gui.py # CustomTkinter desktop UI
 security.py # Prompt injection defense
 sandbox.py # Filesystem sandboxing
 crypto.py # AES-256 encryption
 secure_brain.py # Full secure session manager
 requirements.txt # Python dependencies
 Knowledge_Base/ # Your PDF documents
 audio_out/ # Generated audio files
 screenshots/ # PyAutoGUI screenshots
 chroma_db/ # Vector store (auto-generated)
 logs/ # Audit logs
```

---

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) with `llama3.2` pulled
- Microphone access for voice input
- RVC installed at `./RVC/` (Phase 2 only)
- Windows / macOS / Linux

```
ollama>=0.1.7
SpeechRecognition>=3.10.0
pyttsx3>=2.90
gTTS>=2.5.0
pyaudio>=0.2.14
pygame>=2.5.0
langchain>=0.1.0
langchain-community>=0.0.20
chromadb>=0.4.0
pypdf>=3.17.0
customtkinter>=5.2.0
pyautogui>=0.9.54
psutil>=5.9.0
cryptography>=42.0.0
```

---

## Security Notes

- **No data leaves your machine.** Inference, embeddings, and voice are 100% local.
- The `SecureJane` class wraps every input through three layers: sanitization → injection detection → sandbox enforcement.
- Sensitive files can be encrypted at rest with `crypto.py`; plaintext is never written to disk during decryption.
- All security events are logged to `jane_audit.log` and `jane_security.log`.
- Destructive commands (delete, wipe, format, etc.) require manual `YES` confirmation before execution.

---

## Voice Commands (Arabic)

| Command | Action |
|---|---|
| `افتح vscode` | Opens VS Code |
| `سكرين شوت` | Takes a screenshot |
| `معلومات الجهاز` | Reports CPU & RAM usage |
| `توقف` | Exits the assistant |
| Any question | Answered via RAG + Llama 3.2 |

---

## Engineering Fixes (v2)

| # | File | Issue | Fix |
|---|---|---|---|
| 1 | `audio.py` | TTS spam on failed speech input | Silent `continue` — no TTS on empty/unrecognized audio |
| 2 | `voice.py` | `aplay` crashes on non-Linux | `pygame.mixer.music.play()` for cross-platform playback |
| 3 | `sandbox.py` | Absolute path bypass in sandbox | `Path(path).name` strips absolute prefix before joining |
| 4 | `gui.py` | Tkinter crashes from worker threads | All GUI updates routed via `self.after()` to main thread |

---

## License

© 2025 Jane-AI — All Rights Reserved. 
Submitted to **ITIDA Smart Village** innovation program.
