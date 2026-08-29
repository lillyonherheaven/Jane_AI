"""
Jane-AI - Security & Prompt Injection Guard
Module: security.py
Description: Local regex-based input sanitizer, jailbreak shield, prompt injection
detection, and high-risk desktop execution blocking without external telemetry.
"""

import re
from typing import Tuple, List, Dict, Any


class SecurityGuard:
    """
    Local multi-tier security filter for user inputs and autonomous tool calls.
    Prevents prompt injection, directory traversal attacks, destructive shell executions,
    and dangerous system payload generation.
    """

    # Known prompt injection & jailbreak heuristics (case-insensitive)
    INJECTION_PATTERNS: List[re.Pattern] = [
        re.compile(r"ignore\s+(all\s+)?previous\s+instructions?", re.IGNORECASE),
        re.compile(r"disregard\s+(all\s+)?prior\s+prompts?", re.IGNORECASE),
        re.compile(r"you\s+are\s+now\s+(DAN|unfiltered|jailbroken|godmode)", re.IGNORECASE),
        re.compile(r"system\s*:\s*override", re.IGNORECASE),
        re.compile(r"<\|im_start\|>|<\|im_end\|>|<\|system\|>", re.IGNORECASE),
        re.compile(r"bypass\s+(safety|security|sandbox)", re.IGNORECASE),
        re.compile(r"reveal\s+(internal|system)\s+(prompt|instructions)", re.IGNORECASE),
    ]

    # Prohibited dangerous shell/system execution commands
    DANGEROUS_SYSTEM_PATTERNS: List[re.Pattern] = [
        re.compile(r"rm\s+-rf\s+(/|~|\*)", re.IGNORECASE),
        re.compile(r"format\s+[c-z]:", re.IGNORECASE),
        re.compile(r"del\s+/f\s+/s\s+/q\s+c:\\", re.IGNORECASE),
        re.compile(r"chmod\s+-R\s+777\s+/", re.IGNORECASE),
        re.compile(r":\(\)\{\s*:\|:&\s*\};:", re.IGNORECASE), # Fork bomb
        re.compile(r"mkfs\.[a-z0-9]+\s+/dev/", re.IGNORECASE),
        re.compile(r"shutdown(\.exe)?\s+(-s|-r|/s|/r)", re.IGNORECASE),
        re.compile(r"powershell(\.exe)?\s+-w\s+hidden", re.IGNORECASE),
        re.compile(r"Invoke-WebRequest.*\|\s*iex", re.IGNORECASE),
    ]

    def __init__(self, strict_mode: bool = True):
        self.strict_mode = strict_mode
        self.blocked_events_count = 0

    def sanitize_user_input(self, text: str) -> Tuple[bool, str, str]:
        """
        Validates and sanitizes text entered by the user or received via speech.
        
        Returns:
            (is_safe: bool, sanitized_text: str, reason: str)
        """
        if not text or not text.strip():
            return False, "", "Empty input"

        raw = text.strip()

        # Check for prompt injection attempts
        for pattern in self.INJECTION_PATTERNS:
            if pattern.search(raw):
                self.blocked_events_count += 1
                return False, raw, f"Blocked prompt injection signature: {pattern.pattern}"

        # Normalize control characters and excessive whitespace
        cleaned = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", raw)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        return True, cleaned, "Input passed validation"

    def is_safe_command(self, command: str) -> Tuple[bool, str]:
        """
        Audits a generated system tool command before PyAutoGUI or subprocess execution.
        """
        if not command:
            return False, "Command is empty"

        for pattern in self.DANGEROUS_SYSTEM_PATTERNS:
            if pattern.search(command):
                self.blocked_events_count += 1
                return False, f"Prohibited destructive command detected ({pattern.pattern})"

        # Path traversal guard for file operations
        if "../../../" in command or "..\\..\\..\\" in command:
            return False, "Excessive path traversal sequence detected"

        return True, "Command is secure"

    def get_security_telemetry(self) -> Dict[str, Any]:
        """Returns local security metrics for the GUI dashboard."""
        return {
            "status": "ACTIVE_PROTECTION",
            "strict_mode": self.strict_mode,
            "blocked_events": self.blocked_events_count,
            "air_gapped": True
        }


# Singleton security instance
security_guard = SecurityGuard()
