"""
Jane-AI - Gemini-Inspired CustomTkinter Desktop UI
Module: gui.py
Description: Modern, sleek CustomTkinter interface matching Google Gemini Desktop aesthetics:
- Obsidian background (#0F0F12), Deep Charcoal cards (#202124), Glowing Cyan-Purple accents (#7C4DFF / #00E5FF)
- Multi-threaded non-blocking chat, real-time audio visualizer waveform indicator
- Left sidebar with active agent metrics, memory monitor, and live CPU/RAM gauge
- Floating quick-access overlay widget toggled via global hotkey (Ctrl + Space)
"""

import sys
import threading
import time
import queue
from typing import Optional

try:
    import customtkinter as ctk
    from PIL import Image, ImageTk
except ImportError:
    ctk = None

from brain import jane_brain, AgentPersona
from audio import audio_engine
from voice import voice_streamer
from vision import vision_engine
from memory import memory_manager
from rag import rag_engine
from security import security_guard


class GeminiTheme:
    BG_DARK = "#0F0F12"
    CARD_SURFACE = "#202124"
    CARD_HOVER = "#2B2D31"
    ACCENT_PURPLE = "#7C4DFF"
    ACCENT_CYAN = "#00E5FF"
    ACCENT_GRADIENT_START = "#7C4DFF"
    ACCENT_GRADIENT_END = "#00E5FF"
    TEXT_MAIN = "#FFFFFF"
    TEXT_MUTED = "#9AA0A6"
    USER_BUBBLE = "#2B2D31"
    BOT_BUBBLE = "#1A1A22"
    BORDER_COLOR = "#33353D"


class JaneAIDesktopApp:
    """
    Primary CustomTkinter Desktop Window with multi-threading and Gemini aesthetics.
    """

    def __init__(self):
        if ctk is None:
            print("[GUI Error] CustomTkinter is not installed. Please run: pip install customtkinter")
            return

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Jane-AI (V2.0 Ultimate Edition) - 100% Local Companion")
        self.root.geometry("1180x760")
        self.root.minsize(960, 640)
        self.root.configure(fg_color=GeminiTheme.BG_DARK)

        self.overlay_window: Optional[ctk.CTkToplevel] = None
        self.is_recording = False
        self.visualizer_active = False

        self._setup_layout()
        self._bind_hotkeys()
        self._start_system_monitor_thread()

    def _setup_layout(self):
        """Constructs modern two-panel Gemini desktop layout."""
        # Main Grid
        self.root.grid_columnconfigure(0, weight=0)  # Sidebar
        self.root.grid_columnconfigure(1, weight=1)  # Chat & workspace
        self.root.grid_rowconfigure(0, weight=1)

        # ----------------------------------------------------
        # 1. Left Sidebar (300px fixed)
        # ----------------------------------------------------
        self.sidebar = ctk.CTkFrame(
            self.root,
            width=280,
            corner_radius=0,
            fg_color=GeminiTheme.CARD_SURFACE,
            border_width=1,
            border_color=GeminiTheme.BORDER_COLOR
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar.grid_propagate(False)

        # Brand Header
        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="✨ Jane-AI v2.0",
            font=ctk.CTkFont(family="Plus Jakarta Sans", size=20, weight="bold"),
            text_color=GeminiTheme.TEXT_MAIN
        )
        self.logo_label.pack(anchor="w", padx=20, pady=(20, 4))

        self.sub_label = ctk.CTkLabel(
            self.sidebar,
            text="100% Local & Privacy-First",
            font=ctk.CTkFont(size=12),
            text_color=GeminiTheme.ACCENT_CYAN
        )
        self.sub_label.pack(anchor="w", padx=20, pady=(0, 16))

        # Agent Persona Selector
        self.persona_title = ctk.CTkLabel(
            self.sidebar,
            text="ACTIVE AGENT ROUTER",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=GeminiTheme.TEXT_MUTED
        )
        self.persona_title.pack(anchor="w", padx=20, pady=(10, 4))

        self.persona_var = ctk.StringVar(value="auto")
        self.persona_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Auto Router", "Coder Agent", "RAG Researcher", "SysAdmin Agent"],
            command=self._on_persona_change,
            fg_color="#2D2F38",
            button_color=GeminiTheme.ACCENT_PURPLE,
            button_hover_color="#9266FF",
            text_color=GeminiTheme.TEXT_MAIN,
            corner_radius=10
        )
        self.persona_menu.pack(fill="x", padx=20, pady=(0, 15))

        # Feature Toggles (Web / RAG / Voice)
        self.rag_switch = ctk.CTkSwitch(
            self.sidebar,
            text="ChromaDB RAG Vault",
            progress_color=GeminiTheme.ACCENT_PURPLE,
            text_color=GeminiTheme.TEXT_MAIN
        )
        self.rag_switch.select()
        self.rag_switch.pack(anchor="w", padx=20, pady=6)

        self.web_switch = ctk.CTkSwitch(
            self.sidebar,
            text="Privacy Web Search",
            progress_color=GeminiTheme.ACCENT_CYAN,
            text_color=GeminiTheme.TEXT_MAIN
        )
        self.web_switch.pack(anchor="w", padx=20, pady=6)

        # Hardware Gauge Card
        self.hw_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="#18181E",
            corner_radius=12,
            border_width=1,
            border_color=GeminiTheme.BORDER_COLOR
        )
        self.hw_frame.pack(fill="x", padx=16, pady=20)

        self.hw_title = ctk.CTkLabel(
            self.hw_frame,
            text="SYSTEM METRICS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=GeminiTheme.TEXT_MUTED
        )
        self.hw_title.pack(anchor="w", padx=12, pady=(10, 4))

        self.cpu_label = ctk.CTkLabel(self.hw_frame, text="CPU Usage: 0%", font=ctk.CTkFont(size=12), text_color=GeminiTheme.TEXT_MAIN)
        self.cpu_label.pack(anchor="w", padx=12, pady=2)

        self.ram_label = ctk.CTkLabel(self.hw_frame, text="RAM: Calculating...", font=ctk.CTkFont(size=12), text_color=GeminiTheme.TEXT_MAIN)
        self.ram_label.pack(anchor="w", padx=12, pady=(0, 10))

        # Vision Screenshot Quick Action
        self.vision_btn = ctk.CTkButton(
            self.sidebar,
            text="📸 Analyze Screen (Vision)",
            command=self._trigger_screen_analysis,
            fg_color="#2D2F38",
            hover_color=GeminiTheme.CARD_HOVER,
            corner_radius=10
        )
        self.vision_btn.pack(fill="x", padx=16, pady=(10, 6))

        self.overlay_btn = ctk.CTkButton(
            self.sidebar,
            text="⚡ Toggle Floating Widget",
            command=self.toggle_floating_overlay,
            fg_color=GeminiTheme.ACCENT_PURPLE,
            hover_color="#9266FF",
            corner_radius=10
        )
        self.overlay_btn.pack(fill="x", padx=16, pady=(6, 20))

        # ----------------------------------------------------
        # 2. Main Right Chat Panel
        # ----------------------------------------------------
        self.main_panel = ctk.CTkFrame(self.root, fg_color=GeminiTheme.BG_DARK, corner_radius=0)
        self.main_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_panel.grid_rowconfigure(0, weight=1)
        self.main_panel.grid_rowconfigure(1, weight=0)
        self.main_panel.grid_columnconfigure(0, weight=1)

        # Scrollable Chat History
        self.chat_box = ctk.CTkScrollableFrame(
            self.main_panel,
            fg_color="#121217",
            corner_radius=16,
            border_width=1,
            border_color=GeminiTheme.BORDER_COLOR
        )
        self.chat_box.grid(row=0, column=0, sticky="nsew", pady=(0, 15))

        # Audio Visualizer Bar (Listening / Thinking / Speaking)
        self.visualizer_frame = ctk.CTkFrame(self.main_panel, height=8, fg_color="#18181E", corner_radius=4)
        self.visualizer_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        self.visualizer_status = ctk.CTkLabel(
            self.visualizer_frame,
            text="Ready • Ollama Llama 3.2 Offline",
            font=ctk.CTkFont(size=11),
            text_color=GeminiTheme.TEXT_MUTED
        )
        self.visualizer_status.pack(side="left", padx=10)

        # Input Area (Rounded pill container)
        self.input_container = ctk.CTkFrame(
            self.main_panel,
            fg_color=GeminiTheme.CARD_SURFACE,
            corner_radius=16,
            border_width=1,
            border_color=GeminiTheme.BORDER_COLOR
        )
        self.input_container.grid(row=2, column=0, sticky="ew")
        self.input_container.grid_columnconfigure(0, weight=1)

        self.input_entry = ctk.CTkEntry(
            self.input_container,
            placeholder_text="Ask Jane-AI anything or type a desktop automation command...",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            border_width=0,
            text_color=GeminiTheme.TEXT_MAIN
        )
        self.input_entry.grid(row=0, column=0, padx=(16, 8), pady=12, sticky="ew")
        self.input_entry.bind("<Return>", lambda e: self._handle_send_message())

        # Mic Button
        self.mic_btn = ctk.CTkButton(
            self.input_container,
            text="🎙️",
            width=40,
            height=40,
            command=self._toggle_voice_record,
            fg_color="#2D2F38",
            hover_color="#3E4250",
            corner_radius=12
        )
        self.mic_btn.grid(row=0, column=1, padx=(0, 8), pady=8)

        # Send Button
        self.send_btn = ctk.CTkButton(
            self.input_container,
            text="➤",
            width=44,
            height=40,
            command=self._handle_send_message,
            fg_color=GeminiTheme.ACCENT_PURPLE,
            hover_color="#9266FF",
            corner_radius=12,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.send_btn.grid(row=0, column=2, padx=(0, 10), pady=8)

        # Initial Welcome Bubble
        self._add_message_bubble(
            "assistant",
            "👋 Hello! I am **Jane-AI (V2.0 Ultimate Edition)**, your 100% local, privacy-first AI companion.\n"
            "• Running locally with Ollama (Llama 3.2 & Vision)\n"
            "• Academic ChromaDB Hybrid RAG + Privacy Search\n"
            "• Full Desktop PC Automation & Voice Interaction\n"
            "How can I assist your workflow today?"
        )

    def _add_message_bubble(self, sender: str, text: str):
        """Renders Gemini-style message bubble with 16px corner radius."""
        is_user = sender == "user"
        align = "e" if is_user else "w"
        bg_color = GeminiTheme.USER_BUBBLE if is_user else GeminiTheme.BOT_BUBBLE
        border = None if is_user else GeminiTheme.BORDER_COLOR

        wrapper = ctk.CTkFrame(self.chat_box, fg_color="transparent")
        wrapper.pack(fill="x", padx=12, pady=6, anchor=align)

        bubble = ctk.CTkFrame(
            wrapper,
            fg_color=bg_color,
            corner_radius=16,
            border_width=1 if border else 0,
            border_color=border or "transparent"
        )
        bubble.pack(anchor=align, padx=(80 if is_user else 0, 0 if is_user else 80))

        sender_label = ctk.CTkLabel(
            bubble,
            text="You" if is_user else "✨ Jane-AI",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=GeminiTheme.ACCENT_CYAN if not is_user else GeminiTheme.TEXT_MUTED
        )
        sender_label.pack(anchor="w", padx=14, pady=(8, 2))

        msg_label = ctk.CTkLabel(
            bubble,
            text=text,
            font=ctk.CTkFont(size=13),
            text_color=GeminiTheme.TEXT_MAIN,
            wraplength=600,
            justify="left"
        )
        msg_label.pack(anchor="w", padx=14, pady=(2, 10))

    def _handle_send_message(self):
        text = self.input_entry.get().strip()
        if not text:
            return
        self.input_entry.delete(0, "end")

        self._add_message_bubble("user", text)
        self.visualizer_status.configure(text="⚡ Thinking... (Local Ollama Llama 3.2)")

        def _worker():
            enable_web = bool(self.web_switch.get())
            enable_rag = bool(self.rag_switch.get())
            
            result = jane_brain.process_query(
                user_input=text,
                enable_web=enable_web,
                enable_rag=enable_rag
            )
            response_text = result.get("response", "No response.")
            
            # Update UI on main thread
            self.root.after(0, lambda: self._add_message_bubble("assistant", response_text))
            self.root.after(0, lambda: self.visualizer_status.configure(text="Ready • Listening"))

            # Speak response if enabled
            audio_engine.speak(response_text[:150])

        threading.Thread(target=_worker, daemon=True).start()

    def _toggle_voice_record(self):
        """Starts background voice capture."""
        self.visualizer_status.configure(text="🎙️ Listening to microphone...")
        def _voice_worker():
            spoken_text = audio_engine.listen_once()
            if spoken_text:
                self.root.after(0, lambda: self.input_entry.insert(0, spoken_text))
                self.root.after(0, self._handle_send_message)
            else:
                self.root.after(0, lambda: self.visualizer_status.configure(text="Ready • Standby"))
        threading.Thread(target=_voice_worker, daemon=True).start()

    def _trigger_screen_analysis(self):
        """Captures screen and runs Llama 3.2 Vision."""
        self.visualizer_status.configure(text="📸 Capturing screen & analyzing with Llama 3.2 Vision...")
        def _vis_worker():
            result = vision_engine.analyze_desktop()
            analysis = result.get("analysis", "No analysis.")
            self.root.after(0, lambda: self._add_message_bubble("assistant", f"🖥️ **Screen Analysis**:\n{analysis}"))
            self.root.after(0, lambda: self.visualizer_status.configure(text="Ready"))
        threading.Thread(target=_vis_worker, daemon=True).start()

    def _on_persona_change(self, choice: str):
        mapping = {
            "Auto Router": None,
            "Coder Agent": AgentPersona.CODER,
            "RAG Researcher": AgentPersona.RESEARCHER,
            "SysAdmin Agent": AgentPersona.SYSADMIN
        }
        jane_brain.active_persona = mapping.get(choice, AgentPersona.GENERAL)

    def toggle_floating_overlay(self):
        """Toggles minimalist floating quick-access widget."""
        if self.overlay_window and self.overlay_window.winfo_exists():
            self.overlay_window.destroy()
            self.overlay_window = None
            return

        self.overlay_window = ctk.CTkToplevel(self.root)
        self.overlay_window.title("Jane-AI Quick Bar")
        self.overlay_window.geometry("560x90+400+100")
        self.overlay_window.attributes("-topmost", True)
        self.overlay_window.configure(fg_color="#18181E")

        entry = ctk.CTkEntry(
            self.overlay_window,
            placeholder_text="✨ Fast command (Ctrl+Space to toggle)...",
            font=ctk.CTkFont(size=14),
            fg_color="#202124",
            corner_radius=12
        )
        entry.pack(fill="both", expand=True, padx=12, pady=12)
        entry.focus()
        entry.bind("<Return>", lambda e: self._quick_overlay_submit(entry.get()))

    def _quick_overlay_submit(self, query: str):
        if not query:
            return
        if self.overlay_window:
            self.overlay_window.destroy()
            self.overlay_window = None
        self._add_message_bubble("user", query)
        self._handle_send_message()

    def _bind_hotkeys(self):
        """Attempts to bind global hotkey Ctrl+Space."""
        try:
            import keyboard
            keyboard.add_hotkey("ctrl+space", self.toggle_floating_overlay)
        except Exception as e:
            print(f"[Hotkey Note]: Global keyboard hotkey notice: {e}")

    def _start_system_monitor_thread(self):
        """Background thread updating CPU and RAM stats."""
        def _monitor():
            while True:
                try:
                    import psutil
                    cpu = psutil.cpu_percent(interval=1.0)
                    ram = psutil.virtual_memory()
                    ram_text = f"RAM: {ram.percent}% ({round(ram.used/(1024**3), 1)}/{round(ram.total/(1024**3), 1)}GB)"
                    self.root.after(0, lambda: self.cpu_label.configure(text=f"CPU Usage: {cpu}%"))
                    self.root.after(0, lambda: self.ram_label.configure(text=ram_text))
                except Exception:
                    pass
                time.sleep(2)

        threading.Thread(target=_monitor, daemon=True).start()

    def run(self):
        """Launches the CustomTkinter event loop."""
        self.root.mainloop()


if __name__ == "__main__":
    app = JaneAIDesktopApp()
    app.run()
