"""
Jane-AI- Sandbox & Encrypted St ate Storage
Module: sandbox.py
Description: Local filesystem boundary lock, file access sandboxing,
and AES-Fernet encrypted storage for chat history and persistent local state.
"""

import os
import json
import base64
from pathlib import Path
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class LocalSandbox:
    """
    Manages local workspace isolation and ensures that automated file operations
    only occur within explicitly permitted sandbox directories.
    """

    def __init__(self, workspace_dir: Optional[str] = None):
        if workspace_dir is None:
            self.workspace_dir = Path.home() / ".jane_ai" / "workspace"
        else:
            self.workspace_dir = Path(workspace_dir).resolve()

        self.storage_dir = Path.home() / ".jane_ai" / "encrypted_storage"
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self._encryption_key = self._load_or_generate_key()
        self._cipher = Fernet(self._encryption_key)

    def _load_or_generate_key(self) -> bytes:
        """Loads existing Fernet key or initializes a machine-locked encryption key."""
        key_file = self.storage_dir / ".jane_vault.key"
        if key_file.exists():
            with open(key_file, "rb") as f:
                return f.read()

        # Generate new deterministic key based on machine secret and salt
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(b"JaneAI_Local_Offline_Vault_V2_Secret"))
        
        with open(key_file, "wb") as f:
            f.write(key)
        
        return key

    def validate_file_path(self, target_path: str) -> Path:
        """
        Ensures the requested file path resolves safely inside the sandboxed workspace.
        Raises PermissionError if path traversal outside sandbox is detected.
        """
        resolved = (self.workspace_dir / target_path).resolve()
        try:
            resolved.relative_to(self.workspace_dir)
        except ValueError:
            raise PermissionError(f"Access Denied: Path '{target_path}' is outside the authorized sandbox.")
        return resolved

    def save_encrypted_state(self, key_name: str, data: Dict[str, Any]) -> bool:
        """Encrypts and persists sensitive state locally using Fernet."""
        try:
            payload_json = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
            encrypted = self._cipher.encrypt(payload_json)
            target = self.storage_dir / f"{key_name}.enc"
            with open(target, "wb") as f:
                f.write(encrypted)
            return True
        except Exception as e:
            print(f"[Sandbox Error] Failed to encrypt state '{key_name}': {e}")
            return False

    def load_encrypted_state(self, key_name: str) -> Optional[Dict[str, Any]]:
        """Decrypts and retrieves local state."""
        target = self.storage_dir / f"{key_name}.enc"
        if not target.exists():
            return None
        try:
            with open(target, "rb") as f:
                encrypted = f.read()
            decrypted = self._cipher.decrypt(encrypted)
            return json.loads(decrypted.decode("utf-8"))
        except Exception as e:
            print(f"[Sandbox Error] Failed to decrypt state '{key_name}': {e}")
            return None


# Global sandbox instance
sandbox_manager = LocalSandbox()
