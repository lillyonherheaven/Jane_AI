# Jane-AI

**100% Local, Privacy-First Autonomous AI Companion, Multi-Agent & RAG System**

Built with pure Desktop Python 3.10+, Ollama (`llama3.2` & `llama3.2-vision`), CustomTkinter, LangChain, ChromaDB, PyAutoGUI, SpeechRecognition, Pygame, and Keyboard.

---

## ⚡ Key Highlights
- **Zero External API Calls**: All LLM inference, vision processing, audio STT/TTS, and vector embeddings remain 100% on your local machine.
- **Gemini-Inspired Desktop UI**: Dark obsidian palette (`#0F0F12`), deep charcoal cards (`#202124`), glowing cyan-purple accents (`#7C4DFF` / `#00E5FF`), 16px rounded corners, and live audio visualizers.
- **Autonomous Multi-Agent Routing**: Auto-routes to Coder Agent, RAG Academic Researcher, and SysAdmin Agent.
- **Hybrid RAG Knowledge Vault**: Combines ChromaDB dense vector retrieval with Rank-BM25 lexical scoring and Reciprocal Rank Fusion (RRF).
- **Llama 3.2 Vision Engine**: Real-time desktop screenshot analysis and compiler error debugging.
- **Desktop Automation & Security Sandbox**: Safe PyAutoGUI and psutil control protected by regex prompt injection filters and machine-locked Fernet encryption.
- **Global Floating Widget**: Instant access overlay with global hotkey `Ctrl + Space`.

---

## 🚀 Quick Start Guide

### 1. Install Local Models with Ollama
Make sure [Ollama](https://ollama.com/) is installed and running:
```bash
# Pull Llama 3.2 text and multimodal vision models
ollama pull llama3.2
ollama pull llama3.2-vision
```

### 2. Install Python Dependencies
```bash
# Create virtual environment (Python 3.10+)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Launch Jane-AI
```bash
python main.py
# or launch GUI directly:
python gui.py
```

---

## 📂 Project Architecture

```
jane_ai_v2/
├── requirements.txt   # Central dependencies (LLM, Vision, Audio, RAG, GUI)
├── main.py            # Master startup & environment validator
├── brain.py           # Multi-Agent LLM Engine & Persona Router (Ar/En)
├── vision.py          # Llama 3.2 Vision Desktop Inspector
├── audio.py           # Offline STT & TTS Voice Engine
├── voice.py           # Pygame Audio Mixer & RVC Voice Conversion Bridge
├── rag.py             # ChromaDB + Rank-BM25 Hybrid Retrieval Pipeline
├── web_search.py      # Privacy-Preserving DuckDuckGo Search Wrapper
├── memory.py          # Short-Term Sliding Buffer & Episodic Summarizer
├── agent.py           # PyAutoGUI & psutil Structured Automation Tools
├── security.py        # Regex Input Sanitizer & Prompt Injection Guard
├── sandbox.py         # Filesystem Lock & Fernet-Encrypted Vault
└── gui.py             # CustomTkinter Gemini-Themed Threaded Desktop UI
```

---

## 🔒 Privacy & Security Guarantee
Jane-AI stores all session state, episodic memory, and indexed documents in an encrypted vault at `~/.jane_ai/` with machine-level AES-Fernet encryption. No analytics, tracking, or telemetry data ever leaves your computer.
