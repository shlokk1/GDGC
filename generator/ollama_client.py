"""
SkillForge — Local Ollama Client Integration
Facilitates connection checking and model inference against a local Ollama daemon.
"""

import requests
from typing import Dict, Any, List, Optional

class OllamaClient:
    def __init__(self, endpoint: str = "http://localhost:11434", default_model: str = "qwen2.5:7b"):
        self.endpoint = endpoint.rstrip("/")
        self.default_model = default_model

    def check_connection(self) -> Dict[str, Any]:
        """Checks if the local Ollama daemon is reachable and lists installed models."""
        try:
            resp = requests.get(f"{self.endpoint}/api/tags", timeout=1.5)
            if resp.status_code == 200:
                data = resp.json()
                models = [m.get("name") for m in data.get("models", [])]
                return {
                    "connected": True,
                    "endpoint": self.endpoint,
                    "models": models,
                    "message": f"Connected to Ollama! Found {len(models)} local model(s)."
                }
            return {
                "connected": False,
                "endpoint": self.endpoint,
                "models": [],
                "message": f"Ollama responded with status HTTP {resp.status_code}."
            }
        except requests.exceptions.ConnectionError:
            return {
                "connected": False,
                "endpoint": self.endpoint,
                "models": [],
                "message": f"Could not connect to Ollama at {self.endpoint}. Daemon is offline or not installed."
            }
        except Exception as e:
            return {
                "connected": False,
                "endpoint": self.endpoint,
                "models": [],
                "message": f"Connection check failed: {str(e)}"
            }

    def generate(self, prompt: str, system: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
        """Calls local Ollama API to generate completion (Phase 2 capability)."""
        target_model = model or self.default_model
        payload = {
            "model": target_model,
            "prompt": prompt,
            "stream": False
        }
        if system:
            payload["system"] = system

        try:
            resp = requests.post(f"{self.endpoint}/api/generate", json=payload, timeout=60)
            if resp.status_code == 200:
                result = resp.json()
                return {
                    "success": True,
                    "response": result.get("response", ""),
                    "model": target_model
                }
            return {
                "success": False,
                "error": f"Ollama error HTTP {resp.status_code}: {resp.text}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to reach Ollama: {str(e)}"
            }
