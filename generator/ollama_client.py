"""
SkillForge — Local Ollama Client Integration
Facilitates connection checking and model inference against a local Ollama daemon.
Supports both /api/chat and /api/generate with automatic localhost / 127.0.0.1 fallback.
"""

import requests
from typing import Dict, Any, List, Optional

GENERATION_TIMEOUT_SECONDS = 300.0


class OllamaClient:
    def __init__(self, endpoint: str = "http://localhost:11434", default_model: str = "qwen2.5:7b"):
        self.endpoint = endpoint.rstrip("/")
        self.default_model = default_model
        # Alternative loopback fallback (e.g. 127.0.0.1 vs localhost)
        if "localhost" in self.endpoint:
            self.fallback_endpoint = self.endpoint.replace("localhost", "127.0.0.1")
        elif "127.0.0.1" in self.endpoint:
            self.fallback_endpoint = self.endpoint.replace("127.0.0.1", "localhost")
        else:
            self.fallback_endpoint = None

    def _get(self, path: str, timeout: float = 3.0) -> requests.Response:
        """Attempts GET request with fallback."""
        try:
            return requests.get(f"{self.endpoint}{path}", timeout=timeout)
        except requests.exceptions.ConnectionError:
            if self.fallback_endpoint:
                return requests.get(f"{self.fallback_endpoint}{path}", timeout=timeout)
            raise

    def _post(
        self,
        path: str,
        json_data: Dict[str, Any],
        timeout: float = GENERATION_TIMEOUT_SECONDS
    ) -> requests.Response:
        """Attempts POST request with fallback."""
        try:
            return requests.post(f"{self.endpoint}{path}", json=json_data, timeout=timeout)
        except requests.exceptions.ConnectionError:
            if self.fallback_endpoint:
                return requests.post(f"{self.fallback_endpoint}{path}", json=json_data, timeout=timeout)
            raise

    def check_connection(self) -> Dict[str, Any]:
        """Checks if the local Ollama daemon is reachable and lists installed models."""
        try:
            resp = self._get("/api/tags", timeout=2.5)
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
                    if isinstance(model, dict) and isinstance(model.get("name"), str)
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
        except requests.exceptions.Timeout as e:
            return {
                "connected": False,
                "endpoint": self.endpoint,
                "models": [],
                "message": f"Timed out connecting to Ollama at {self.endpoint}: {e}"
            }
        except Exception as e:
            return {
                "connected": False,
                "endpoint": self.endpoint,
                "models": [],
                "message": f"Could not connect to Ollama at {self.endpoint}: {e}"
            }

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.2
    ) -> Dict[str, Any]:
        """Calls local Ollama and only falls back routes when the chat API is unsupported."""
        target_model = model or self.default_model

        # Preferred: /api/chat for instruction-tuned models like qwen2.5:7b
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": target_model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }

        try:
            resp = self._post(
                "/api/chat",
                payload,
                timeout=GENERATION_TIMEOUT_SECONDS
            )
            if resp.status_code == 200:
                result = resp.json()
                message = result.get("message")
                content = message.get("content", "") if isinstance(message, dict) else ""
                if not isinstance(content, str) or not content.strip():
                    return {
                        "success": False,
                        "error": "Ollama returned an empty response from /api/chat."
                    }
                return {
                    "success": True,
                    "response": content,
                    "model": target_model
                }
            if resp.status_code not in (404, 405):
                return {
                    "success": False,
                    "error": f"Ollama /api/chat returned HTTP {resp.status_code}: {resp.text[:500]}"
                }
        except requests.exceptions.Timeout as e:
            return {
                "success": False,
                "error": (
                    f"Ollama did not finish generating within "
                    f"{int(GENERATION_TIMEOUT_SECONDS)} seconds. The model may still be loading; "
                    f"please retry. ({e})"
                )
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Could not reach Ollama at {self.endpoint}: {e}"
            }
        except ValueError as e:
            return {
                "success": False,
                "error": f"Ollama returned invalid JSON from /api/chat: {e}"
            }

        # Older Ollama-compatible servers may not implement /api/chat.
        gen_payload = {
            "model": target_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        if system:
            gen_payload["system"] = system

        try:
            resp = self._post(
                "/api/generate",
                gen_payload,
                timeout=GENERATION_TIMEOUT_SECONDS
            )
            if resp.status_code == 200:
                result = resp.json()
                if not isinstance(result, dict):
                    return {
                        "success": False,
                        "error": "Ollama returned an unexpected response from /api/generate."
                    }
                content = result.get("response")
                if not isinstance(content, str) or not content.strip():
                    return {
                        "success": False,
                        "error": "Ollama returned an empty response from /api/generate."
                    }
                return {
                    "success": True,
                    "response": content,
                    "model": target_model
                }
            return {
                "success": False,
                "error": f"Ollama /api/generate returned HTTP {resp.status_code}: {resp.text[:500]}"
            }
        except requests.exceptions.Timeout as e:
            return {
                "success": False,
                "error": (
                    f"Ollama did not finish generating within "
                    f"{int(GENERATION_TIMEOUT_SECONDS)} seconds. The model may still be loading; "
                    f"please retry. ({e})"
                )
            }
        except (requests.exceptions.RequestException, ValueError) as e:
            return {
                "success": False,
                "error": f"Ollama request failed at {self.endpoint}: {e}"
            }
