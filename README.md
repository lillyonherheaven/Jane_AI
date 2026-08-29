# 🧠 Jane-AI — Local Autonomous AI Companion & Desktop Workspace

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/Ollama-Llama_3.2_%26_Vision-orange?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama" />
  <img src="https://img.shields.io/badge/GUI-CustomTkinter_Monochrome-000000?style=for-the-badge" alt="CustomTkinter" />
  <img src="https://img.shields.io/badge/Storage-ChromaDB_%2B_Rank--BM25-green?style=for-the-badge" alt="ChromaDB" />
  <img src="https://img.shields.io/badge/Privacy-100%25_Air--Gapped-darkred?style=for-the-badge" alt="Air-Gapped" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge" alt="License" />
</p>

---

## 🌟 Overview

**Jane-AI** is a production-ready, 100% local, privacy-first desktop autonomous AI companion and multi-agent operating workspace. Built from the ground up to operate in strictly air-gapped environments, Jane-AI combines on-device inference via **Ollama (Llama 3.2 3B & Vision)** with a minimalist monochrome **CustomTkinter** desktop user interface, **ChromaDB + Rank-BM25 Hybrid RAG**, offline multimodal vision inspection, and deterministic **PyAutoGUI / psutil desktop automation**.

No API keys, no telemetry, no cloud subscriptions, and zero external data transmission.

```
                  ┌─────────────────────────────────────────┐
                  │       Jane-AI Monochrome Desktop GUI     │
                  │  (CustomTkinter • Dual-Tone Minimalism)  │
                  └────────────────────┬────────────────────┘
                                       │
                      ┌────────────────┴────────────────┐
                      │    Local Security Guard Layer   │
                      │  (Regex Sanitizer & Fernet AES) │
                      └────────────────┬────────────────┘
                                       │
                                       ▼
                     ┌───────────────────────────────────┐
                     │    Multi-Agent Cognitive Router   │
                     │  (General • Coder • RAG • SysAdmin)│
                     └─┬───────────────┬───────────────┬─┘
                       │               │               │
        ┌──────────────▼──────┐ ┌──────▼──────┐ ┌──────▼──────────────┐
        │    Local Ollama     │ │  ChromaDB   │ │ Sandboxed Automation │
        │  • Llama 3.2 (3B)   │ │  + BM25     │ │  • PyAutoGUI tools   │
        │  • Llama 3.2 Vision │ │  Hybrid RAG │ │  • psutil Telemetry  │
        └─────────────────────┘ └─────────────┘ └─────────────────────┘
```

---

## 📑 Table of Contents

- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Quick Start Installation](#-quick-start-installation)
- [Multi-Agent Personas](#-multi-agent-personas)
- [Hybrid Retrieval (RAG Vault)](#-hybrid-retrieval-rag-vault)
- [Multimodal Vision Inspector](#-multimodal-vision-inspector)
- [Desktop Automation & Security Sandbox](#-desktop-automation--security-sandbox)
- [Configuration & Settings](#-configuration--settings)
- [Troubleshooting & FAQ](#-troubleshooting--faq)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Key Features

- 🔒 **100% Offline & Private**: Runs entirely on your CPU / GPU. Your documents, queries, codebases, and audio recordings never leave your machine.
- 🧠 **Multi-Agent Specialist Router**: Dynamically shifts between specialized personas (General Assistant, Senior Software Engineer, Academic Researcher, and Systems Administrator).
- 👁️ **Multimodal Screen & IDE Vision**: Instant desktop screenshot capture analyzed through `llama3.2-vision` to debug stack traces, inspect terminal outputs, and review wireframes.
- 📚 **Hybrid Retrieval (RAG Vault)**: Combines dense semantic vector search (`ChromaDB` embeddings) with sparse keyword matching (`Rank-BM25`) using Reciprocal Rank Fusion (RRF).
- 🎙️ **Offline Voice Engine**: Speech-to-text with Sphinx fallback, speech synthesis via `pyttsx3`, and sound effects with `pygame`.
- ⚡ **Desktop Automation Sandbox**: Deterministic PyAutoGUI keystroke automation, system telemetry queries (`psutil`), and path-traversal-locked file operations.
- 🛡️ **Zero-Trust Security & Fernet Vault**: Real-time regex prompt injection defense, blocked command heuristics, and AES-Fernet encrypted local metadata storage in `~/.jane_ai`.
- ⌨️ **Global Quick-Bar Overlay**: Press `Ctrl+Space` anywhere to summon the floating quick-command bar.
- 🎨 **Monochrome Minimalist Interface**: Pure high-contrast dark aesthetic (`#0D0D0D` / `#1A1A1A` / `#FFFFFF`) crafted with `CustomTkinter`.

---

## 🏗️ System Architecture

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Inference Engine** | [Ollama](https://ollama.ai) (`llama3.2:latest`, `llama3.2-vision`) | Local LLM and Vision processing on CPU/GPU |
| **Desktop UI** | [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | Responsive, threaded, dark-mode native desktop GUI |
| **Vector DB** | [ChromaDB](https://www.trychroma.com/) + LangChain | Local document chunking, indexing, and vector similarity |
| **Sparse Search** | [Rank-BM25](https://github.com/dorianbrown/rank_bm25) | Exact terminology matching and code symbol retrieval |
| **Desktop Tools** | [PyAutoGUI](https://pyautogui.readthedocs.io/) + [psutil](https://psutil.readthedocs.io/) | Keyboard automation, screen capture, hardware telemetry |
| **Audio Engine** | SpeechRecognition + `pyttsx3` + `pygame` | Low-latency offline speech input & text-to-speech feedback |
| **Local Security** | `cryptography.fernet` + Regex Guard | Path traversal prevention, injection sanitization, AES vault |

---

## 📂 Project Structure

```
jane_ai_desktop/
├── requirements.txt         # Production-locked Python dependencies
├── main.py                  # Master entry point & environment verification
├── brain.py                 # Multi-LLM cognitive engine & persona routing
├── gui.py                   # CustomTkinter monochrome desktop interface & tabs
├── rag.py                   # ChromaDB + Rank-BM25 hybrid document engine
├── vision.py                # Screen capture & Llama 3.2 Vision multimodal reasoner
├── agent.py                 # Structured desktop tool executor & dispatch table
├── audio.py                 # Offline speech-to-text listener & Sphinx fallback
├── voice.py                 # TTS synthesis & audio playback sound engine
├── memory.py                # Sliding window context & episodic conversation memory
├── security.py              # Regex prompt-injection filter & command sanitizer
├── sandbox.py               # Path-traversal containment & Fernet AES encrypted vault
├── web_search.py            # Local tracker-free DuckDuckGo search integration
├── run_jane.sh              # Unix (Linux / macOS) one-click boot script
└── run_jane.bat             # Windows one-click batch boot script
```

---

## 📋 Prerequisites

1. **Python 3.10+** (Python 3.10, 3.11, or 3.12 recommended).
2. **Ollama Installed & Running**:
   - Download from [ollama.com](https://ollama.com).
   - Pull the required models:
     ```bash
     ollama pull llama3.2
     ollama pull llama3.2-vision
     ```

---

## ⚡ Quick Start Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/jane-ai.git
cd jane-ai
```

### 2. Create and Activate a Virtual Environment

**On Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows (Command Prompt / PowerShell):**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> **Note for Linux users:** If installing `pyaudio` or `customtkinter`, ensure you have system audio libraries:
> ```bash
> sudo apt-get update
> sudo apt-get install python3-tk portaudio19-dev libasound2-dev
> ```

### 4. Start Local Ollama Server
Ensure the Ollama daemon is running in a separate terminal:
```bash
ollama serve
```

### 5. Launch Jane-AI Desktop
```bash
python main.py
```

*Or use the pre-configured launcher scripts:*
- Linux/macOS: `./run_jane.sh`
- Windows: `run_jane.bat`

---

## 🎭 Multi-Agent Personas

Jane-AI automatically routes queries to specialized cognitive sub-agents based on context:

1. **General Assistant (`general`)**:
   - Direct, high-density conversational support with bilingual (English / Arabic) fluency.
2. **Senior Coder Specialist (`coder`)**:
   - Specialized in Python 3.10+, TypeScript, Rust, asynchronous algorithms, type safety, and bug eradication.
3. **Academic Researcher (`researcher`)**:
   - Formulates grounded syntheses from PDF technical papers, research documents, and ChromaDB vector chunks with source citations.
4. **SysAdmin Specialist (`sysadmin`)**:
   - Inspects host RAM, CPU, VRAM, and running processes via `psutil`, executing verified diagnostics.

---

## 🔍 Hybrid Retrieval (RAG Vault)

Jane-AI employs a **Dual-Engine Hybrid Search** architecture for zero-hallucination document querying:

$$\text{Hybrid Score} = \alpha \cdot \text{Vector Cosine Sim} + (1 - \alpha) \cdot \text{BM25 Score}$$

```
[Uploaded Document (PDF / MD / Code)]
                │
                ▼
      [Recursive Text Splitter]
         (Chunk Size: 500, Overlap: 50)
                │
        ┌───────┴────────┐
        ▼                ▼
 [ChromaDB Vectors]  [Rank-BM25 Sparse Index]
   (Dense Semantic)     (Exact Keyword Match)
        │                │
        └───────┬────────┘
                ▼
     [Reciprocal Rank Fusion]
                │
                ▼
      [Top-K Grounded Context] ──► [Llama 3.2 Local LLM] ──► Verified Answer
```

---

## 🛡️ Desktop Automation & Security Sandbox

All host interactions are strictly gated behind deterministic security policies:

| Action | Safety Mechanism |
| :--- | :--- |
| **File I/O** | Locked to `~/.jane_ai/workspace/`. Relative paths resolved; path-traversal (`../`) raises `PermissionError`. |
| **Keystroke Automation** | PyAutoGUI calls executed with bounded execution timeouts and target window validation. |
| **Telemetry Queries** | Read-only hardware telemetry via `psutil` (CPU, memory, storage metrics). |
| **Prompt Injection Defense** | Input stream parsed by `security_guard.py` using regex heuristics (`ignore previous instructions`, `system override`, `rm -rf`). |
| **Encrypted Storage** | Local credentials, settings, and session metadata encrypted with AES-128 Fernet keys stored in `~/.jane_ai/storage/`. |

---

## ⌨️ Global Hotkeys & UI Shortcuts

| Key Combination | Action |
| :--- | :--- |
| <kbd>Ctrl</kbd> + <kbd>Space</kbd> | Toggle Global Floating Quick-Bar Overlay |
| <kbd>Ctrl</kbd> + <kbd>Enter</kbd> | Send message in Chat View |
| <kbd>Esc</kbd> | Dismiss floating widget / modal dialogs |

---

## 🛠️ Troubleshooting & FAQ

#### Q1: "Connection refused on http://localhost:11434"
- **Fix**: Ollama is not running. Run `ollama serve` in your terminal or start the Ollama desktop service.

#### Q2: "Model 'llama3.2' not found"
- **Fix**: Pull the model using `ollama pull llama3.2` and `ollama pull llama3.2-vision`.

#### Q3: PyAudio installation errors on Linux / macOS
- **Fix**: 
  - macOS: `brew install portaudio && pip install pyaudio`
  - Ubuntu/Debian: `sudo apt install portaudio19-dev && pip install pyaudio`

#### Q4: Does Jane-AI send any data to external servers?
- **Answer**: **No.** Jane-AI operates with zero external network calls. Web search (DuckDuckGo) is completely optional and disabled by default.

---

## 🤝 Contributing

Contributions are warmly welcomed! To contribute:

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/NewCapability`).
3. Commit your changes (`git commit -m 'feat: Add offline embedding cache'`).
4. Push to the branch (`git push origin feature/NewCapability`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more details.

---

<p align="center">
  <b>Jane-AI</b> • 100% Local • Zero Cloud • Air-Gapped Intelligence
</p>
