"""
Jane-AI - Multi-Agent Brain & Intelligent Router
Module: brain.py
Description: Central orchestration engine powered by local Llama 3.2 via Ollama.
Routes requests across specialized sub-agents (Coder, RAG Researcher, System Admin),
enforces bilingual personas (Arabic / English), and synthesizes multi-modal tool responses.
"""

import json
from typing import Dict, Any, List, Optional, Generator
from security import security_guard
from memory import memory_manager
from agent import automation_agent
from vision import vision_engine


class AgentPersona:
    CODER = "coder"
    RESEARCHER = "researcher"
    SYSADMIN = "sysadmin"
    GENERAL = "general"


class JaneBrain:
    """
    Multi-Agent LLM Coordinator for Jane-AI V2.0.
    100% offline reasoning with automatic prompt specialization and language alignment.
    """

    SYSTEM_PROMPTS = {
        "en": {
            AgentPersona.GENERAL: (
                "You are Jane-AI (V2.0 Ultimate Edition), a brilliant, warm, and highly capable local autonomous AI companion. "
                "You operate 100% locally on the user's desktop with absolute privacy. "
                "You are concise, helpful, and insightful. If tools are needed, suggest or trigger them cleanly."
            ),
            AgentPersona.CODER: (
                "You are Jane-AI's Lead Software Engineering Agent. "
                "You write production-grade, modular, type-annotated code in Python, TypeScript, C++, Rust, and Go. "
                "Always adhere to clean architecture, handle edge cases, and provide concise execution steps."
            ),
            AgentPersona.RESEARCHER: (
                "You are Jane-AI's Academic & RAG Research Specialist. "
                "Synthesize dense academic documents, PDFs, and notes into structured scientific summaries. "
                "Cite retrieved source sections and ensure high factual precision."
            ),
            AgentPersona.SYSADMIN: (
                "You are Jane-AI's System Administration & Desktop Automation Specialist. "
                "You assist the user with operating system tasks, hardware optimization, process management, and terminal automation safely."
            )
        },
        "ar": {
            AgentPersona.GENERAL: (
                "أنتِ 'جين' (Jane-AI V2.0 الإصدار الفائق)، الرفيقة الذكية المستقلة التي تعمل محلياً 100% وبخصوصية تامة على جهاز المستخدم. "
                "تتميزين بالذكاء واللطف والدقة الفائقة، وتتحدثين باللغة العربية الفصحى الجميلة أو الإنجليزية حسب رغبة المستخدم."
            ),
            AgentPersona.CODER: (
                "أنتِ وكيلة هندسة البرمجيات والتطوير في Jane-AI. متخصصة في كتابة كود برمجي احترافي ونظيف، "
                "وتصحيح الأخطاء البرمجية وشرح المفاهيم التقنية بدقة ووضوح."
            ),
            AgentPersona.RESEARCHER: (
                "أنتِ باحثة المعرفة والوثائق الأكاديمية في Jane-AI. تقومين بتحليل ملفات PDF واستخراج المعرفة بدقة وتلخيصها."
            ),
            AgentPersona.SYSADMIN: (
                "أنتِ مسؤولة إدارة النظام والأتمتة المكتبية في Jane-AI. تساعدين في إدارة موارد الجهاز والمهام بكفاءة وأمان تام."
            )
        }
    }

    def __init__(self, default_model: str = "llama3.2:latest"):
        self.default_model = default_model
        self.active_persona = AgentPersona.GENERAL
        self.language_mode = "en"  # "en" or "ar"

    def detect_language(self, text: str) -> str:
        """Detects whether user prompt contains Arabic characters."""
        arabic_chars = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
        if arabic_chars > 3 or (len(text) > 0 and arabic_chars / len(text) > 0.25):
            return "ar"
        return "en"

    def route_agent_persona(self, user_input: str) -> str:
        """
        Dynamically classifies the request intent into the optimal sub-agent persona.
        """
        lower = user_input.lower()

        # Code keywords
        if any(w in lower for w in ["code", "python", "bug", "function", "class", "react", "typescript", "debug", "refactor", "كود", "برمجة", "دالة", "خطأ"]):
            return AgentPersona.CODER

        # RAG / Research keywords
        if any(w in lower for w in ["pdf", "paper", "research", "document", "summarize doc", "rag", "vault", "بحث", "ملف", "وثيقة", "دراسة", "لخص"]):
            return AgentPersona.RESEARCHER

        # SysAdmin / Automation keywords
        if any(w in lower for w in ["cpu", "ram", "memory usage", "process", "open app", "terminal", "system", "automation", "المعالج", "الذاكرة", "افتح", "نظام"]):
            return AgentPersona.SYSADMIN

        return AgentPersona.GENERAL

    def process_query(self, user_input: str, enable_web: bool = False, enable_rag: bool = True, force_persona: Optional[str] = None) -> Dict[str, Any]:
        """
        Coordinates full inference pipeline:
        1. Security check & sanitization
        2. Persona routing & language detection
        3. Memory & RAG enrichment
        4. Ollama Llama 3.2 execution
        """
        # 1. Security Check
        is_safe, sanitized_text, sec_reason = security_guard.sanitize_user_input(user_input)
        if not is_safe:
            return {
                "success": False,
                "response": f"[Jane-AI Security Alert]: Query blocked for safety: {sec_reason}",
                "persona": AgentPersona.GENERAL,
                "language": "en"
            }

        # 2. Routing
        lang = self.detect_language(sanitized_text)
        self.language_mode = lang
        persona = force_persona or self.route_agent_persona(sanitized_text)
        self.active_persona = persona

        # 3. Memory & Context Enrichment
        enriched_context = memory_manager.build_enriched_context(
            user_query=sanitized_text,
            enable_web=enable_web,
            enable_rag=enable_rag
        )

        system_prompt = self.SYSTEM_PROMPTS[lang].get(persona, self.SYSTEM_PROMPTS[lang][AgentPersona.GENERAL])
        if enriched_context:
            system_prompt += f"\n\n{enriched_context}"

        # 4. Assemble Messages for Ollama
        messages = [{"role": "system", "content": system_prompt}]
        for turn in memory_manager.get_recent_history():
            messages.append({"role": turn["role"], "content": turn["content"]})
        messages.append({"role": "user", "content": sanitized_text})

        # 5. Local Ollama Inference
        try:
            import ollama

            response = ollama.chat(
                model=self.default_model,
                messages=messages,
                options={"temperature": 0.7}
            )
            reply = response.get("message", {}).get("content", "No response received.")
            
            # Record turn in local memory
            memory_manager.add_turn("user", sanitized_text)
            memory_manager.add_turn("assistant", reply)

            return {
                "success": True,
                "response": reply,
                "persona": persona,
                "language": lang,
                "model": self.default_model
            }

        except ImportError:
            fallback_msg = (
                f"Jane-AI local brain is active (Persona: {persona.upper()}). "
                f"To connect to the local Llama 3.2 engine, install the 'ollama' Python library and launch 'ollama run llama3.2'."
            )
            memory_manager.add_turn("user", sanitized_text)
            memory_manager.add_turn("assistant", fallback_msg)
            return {
                "success": True,
                "response": fallback_msg,
                "persona": persona,
                "language": lang,
                "model": self.default_model
            }
        except Exception as e:
            err_msg = f"[Ollama Engine Status]: {str(e)}. Please ensure Ollama is running on localhost:11434 with 'llama3.2'."
            return {
                "success": False,
                "response": err_msg,
                "persona": persona,
                "language": lang,
                "model": self.default_model
            }


# Global Brain Instance
jane_brain = JaneBrain()
