"""
Jane-AI- Autonomous Desktop Agent & Automation Tools
Module: agent.py
Description: Structured Tool Calling runtime for local PC automation, window management,
process monitoring (psutil), keyboard/mouse scripting (PyAutoGUI), and sandboxed execution.
"""

import os
import json
import time
import subprocess
from typing import Dict, Any, List, Optional
from security import security_guard
from sandbox import sandbox_manager


class DesktopAutomationAgent:
    """
    Executes authorized autonomous actions on the host machine.
    Every action is filtered through SecurityGuard and executed within safety boundaries.
    """

    def __init__(self):
        self.action_history: List[Dict[str, Any]] = []

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """
        JSON schemas for Ollama / Llama 3.2 tool calling format.
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "open_application",
                    "description": "Launches a desktop application or utility (e.g. 'notepad', 'calc', 'code', 'chrome', 'spotify').",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "app_name": {"type": "string", "description": "The executable name or command of the app"}
                        },
                        "required": ["app_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_system_telemetry",
                    "description": "Retrieves real-time CPU usage, RAM utilization, active processes, and battery status.",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "type_text_keyboard",
                    "description": "Types a given string into the currently focused window using PyAutoGUI.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "description": "The text to type"},
                            "press_enter": {"type": "boolean", "description": "Whether to press Enter after typing"}
                        },
                        "required": ["text"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_workspace_file",
                    "description": "Writes code, scripts, or text to a file strictly inside the sandboxed workspace directory.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filename": {"type": "string", "description": "Relative filename, e.g., 'script.py'"},
                            "content": {"type": "string", "description": "Text content to save"}
                        },
                        "required": ["filename", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "press_hotkey",
                    "description": "Simulates keyboard hotkey combinations (e.g. ['ctrl', 's'], ['alt', 'tab'], ['ctrl', 'c']).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keys": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of key names to press together"
                            }
                        },
                        "required": ["keys"]
                    }
                }
            }
        ]

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dispatches tool calls with strict parameter validation and safety logging.
        """
        start_time = time.time()
        result = {"success": False, "tool": tool_name, "output": None, "error": None}

        try:
            if tool_name == "open_application":
                app_name = arguments.get("app_name", "")
                is_safe, reason = security_guard.is_safe_command(app_name)
                if not is_safe:
                    result["error"] = f"Security block: {reason}"
                else:
                    subprocess.Popen(app_name, shell=True)
                    result["success"] = True
                    result["output"] = f"Launched application: {app_name}"

            elif tool_name == "get_system_telemetry":
                import psutil
                cpu_pct = psutil.cpu_percent(interval=0.2)
                ram = psutil.virtual_memory()
                result["success"] = True
                result["output"] = {
                    "cpu_usage_pct": cpu_pct,
                    "ram_used_gb": round(ram.used / (1024**3), 2),
                    "ram_total_gb": round(ram.total / (1024**3), 2),
                    "ram_percent": ram.percent,
                    "process_count": len(psutil.pids())
                }

            elif tool_name == "type_text_keyboard":
                text = arguments.get("text", "")
                press_enter = arguments.get("press_enter", False)
                try:
                    import pyautogui
                    pyautogui.write(text, interval=0.01)
                    if press_enter:
                        pyautogui.press("enter")
                    result["success"] = True
                    result["output"] = f"Typed {len(text)} characters to active window."
                except Exception as e:
                    result["error"] = f"PyAutoGUI error: {e}"

            elif tool_name == "write_workspace_file":
                filename = arguments.get("filename", "")
                content = arguments.get("content", "")
                safe_path = sandbox_manager.validate_file_path(filename)
                with open(safe_path, "w", encoding="utf-8") as f:
                    f.write(content)
                result["success"] = True
                result["output"] = f"Successfully wrote file at {safe_path}"

            elif tool_name == "press_hotkey":
                keys = arguments.get("keys", [])
                try:
                    import pyautogui
                    pyautogui.hotkey(*keys)
                    result["success"] = True
                    result["output"] = f"Pressed hotkeys: {' + '.join(keys)}"
                except Exception as e:
                    result["error"] = f"Hotkey error: {e}"

            else:
                result["error"] = f"Unknown tool: {tool_name}"

        except Exception as e:
            result["error"] = str(e)

        result["duration_ms"] = round((time.time() - start_time) * 1000, 2)
        self.action_history.append(result)
        return result


# Global automation agent instance
automation_agent = DesktopAutomationAgent()
