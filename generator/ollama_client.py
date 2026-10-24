"""
SkillForge — Local Ollama Client Integration
Facilitates connection checking and model inference against a local Ollama daemon.
"""

from typing import Dict, Any, List, Optional
import requests

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
                if not isinstance(data, dict) or not isinstance(data.get("models", []), list):
                    return {
                        "connected": False,
                        "endpoint": self.endpoint,
                        "models": [],
                        "message": "Ollama returned an unexpected model-list response."
                    }
                models = [
                    model.get("name")
                    for model in data.get("models", [])
                    if isinstance(model, dict) and model.get("name")
                ]
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
        except requests.exceptions.Timeout:
            return {
                "connected": False,
                "endpoint": self.endpoint,
                "models": [],
                "message": f"Connection to Ollama at {self.endpoint} timed out."
            }
        except (requests.exceptions.RequestException, ValueError) as e:
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
            resp = requests.post(f"{self.endpoint}/api/generate", json=payload, timeout=180)
            if resp.status_code == 200:
                result = resp.json()
                if not isinstance(result, dict):
                    return {"success": False, "error": "Ollama returned an unexpected generation response."}
                response = result.get("response")
                if not isinstance(response, str) or not response.strip():
                    return {"success": False, "error": "Ollama returned an empty model response."}
                return {
                    "success": True,
                    "response": response,
                    "model": target_model
                }
            return {
                "success": False,
                "error": f"Ollama error HTTP {resp.status_code}: {resp.text[:500]}"
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": f"Could not connect to Ollama at {self.endpoint}. Start Ollama and try again."
            }
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Ollama generation timed out after 180 seconds."
            }
        except (requests.exceptions.RequestException, ValueError) as e:
            return {
                "success": False,
                "error": f"Failed to reach Ollama: {str(e)}"
            }
