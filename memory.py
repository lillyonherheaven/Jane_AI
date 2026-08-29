"""
Jane-AI - Memory & Context Synthesis
Module: memory.py
Description: Manages short-term conversation sliding buffers, episodic summarization,
and intelligent RAG + Web context merging for multi-agent reasoning.
"""

from typing import List, Dict, Any, Optional
from rag import rag_engine
from web_search import local_searcher
from sandbox import sandbox_manager


class JaneMemoryManager:
    """
    Coordinates conversational context, historical session recall,
    and automatic context compression when token limits approach threshold.
    """

    def __init__(self, max_short_term_turns: int = 10):
        self.max_short_term_turns = max_short_term_turns
        self.short_term_history: List[Dict[str, str]] = []
        self.episodic_summary: str = ""
        self.user_profile: Dict[str, Any] = {
            "name": "User",
            "language_pref": "bilingual_ar_en",
            "code_style": "clean_modular_typed",
            "voice_enabled": True
        }
        self._load_persisted_memory()

    def _load_persisted_memory(self):
        """Loads encrypted memory snapshot from local vault."""
        saved = sandbox_manager.load_encrypted_state("conversation_memory")
        if saved:
            self.episodic_summary = saved.get("episodic_summary", "")
            self.short_term_history = saved.get("short_term_history", [])
            self.user_profile = saved.get("user_profile", self.user_profile)

    def persist_memory(self):
        """Saves encrypted state."""
        sandbox_manager.save_encrypted_state("conversation_memory", {
            "episodic_summary": self.episodic_summary,
            "short_term_history": self.short_term_history,
            "user_profile": self.user_profile
        })

    def add_turn(self, role: str, content: str):
        """Appends a new user or assistant turn and triggers summarization if buffer is full."""
        self.short_term_history.append({"role": role, "content": content})
        if len(self.short_term_history) > (self.max_short_term_turns * 2):
            self._compress_context()
        self.persist_memory()

    def _compress_context(self):
        """Summarizes older conversation turns into episodic memory."""
        older_turns = self.short_term_history[:-4]
        self.short_term_history = self.short_term_history[-4:]

        condensed_text = " ".join([f"{t['role'].upper()}: {t['content'][:80]}" for t in older_turns])
        if self.episodic_summary:
            self.episodic_summary += f" | Prior topics: {condensed_text}"
        else:
            self.episodic_summary = f"Prior topics: {condensed_text}"

    def build_enriched_context(self, user_query: str, enable_web: bool = False, enable_rag: bool = True) -> str:
        """
        Synthesizes RAG documents, episodic memory, and optional privacy search into prompt context.
        """
        sections: List[str] = []

        # 1. Episodic Long-Term Recall
        if self.episodic_summary:
            sections.append(f"[LONG-TERM EPISODIC MEMORY]:\n{self.episodic_summary}\n")

        # 2. Local Knowledge RAG
        if enable_rag:
            rag_results = rag_engine.hybrid_search(user_query, top_k=3)
            rag_context = rag_engine.format_rag_context(rag_results)
            if rag_context:
                sections.append(rag_context)

        # 3. Privacy Web Search Context
        if enable_web:
            search_results = local_searcher.search_duckduckgo(user_query, max_results=3)
            web_context = local_searcher.format_search_context(search_results)
            if web_context:
                sections.append(web_context)

        return "\n\n".join(sections)

    def get_recent_history(self) -> List[Dict[str, str]]:
        """Returns active short-term turns for Ollama message formatting."""
        return self.short_term_history.copy()

    def clear_memory(self):
        """Clears short-term buffer and episodic memory."""
        self.short_term_history.clear()
        self.episodic_summary = ""
        self.persist_memory()


# Global Memory Instance
memory_manager = JaneMemoryManager()
