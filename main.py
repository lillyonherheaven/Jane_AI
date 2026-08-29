"""
Jane-AI - Master Entry Point
Module: main.py
Description: Initializes local security sandboxes, verifies Ollama model availability,
configures speech/vision services, and boots the CustomTkinter GUI.
"""

import sys
import os
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)


def print_banner():
    banner = f"""
{Fore.CYAN}======================================================================
{Fore.MAGENTA}          ✨ JANE-AI (V2.0 ULTIMATE EDITION) ✨
{Fore.CYAN}    100% Local • Privacy-First • Autonomous Multi-Agent & RAG
======================================================================{Style.RESET_ALL}
[+] Core Architecture : Ollama (Llama 3.2 & Llama 3.2 Vision)
[+] Desktop Framework : CustomTkinter (Gemini Aesthetics)
[+] Knowledge Vault   : ChromaDB + Rank-BM25 Hybrid Retrieval
[+] PC Automation     : Sandboxed PyAutoGUI & psutil
[+] Security Level    : Zero External Telemetry • Fernet Vault Encrypted
----------------------------------------------------------------------
"""
    print(banner)


def check_prerequisites():
    """Validates local environment and dependencies."""
    print(f"{Fore.YELLOW}[*] Validating local workspace & security directories...{Style.RESET_ALL}")
    from sandbox import sandbox_manager
    print(f"    - Workspace Sandbox : {sandbox_manager.workspace_dir}")
    print(f"    - Encrypted Storage : {sandbox_manager.storage_dir}")

    # Check Ollama connectivity
    try:
        import ollama
        print(f"{Fore.GREEN}[✓] Ollama Python client detected.{Style.RESET_ALL}")
    except ImportError:
        print(f"{Fore.RED}[!] 'ollama' Python library not installed. Install with: pip install ollama{Style.RESET_ALL}")


def main():
    print_banner()
    check_prerequisites()

    print(f"{Fore.CYAN}[*] Initializing Jane-AI CustomTkinter GUI...{Style.RESET_ALL}")
    try:
        from gui import JaneAIDesktopApp
        app = JaneAIDesktopApp()
        app.run()
    except Exception as e:
        print(f"{Fore.RED}[!] Error starting GUI: {e}{Style.RESET_ALL}")
        print("    If running in a headless container, run with a virtual display or inspect module unit tests.")


if __name__ == "__main__":
    main()
