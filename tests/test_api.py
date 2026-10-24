"""
Tests for SkillForge HTTP API and Frontend Serving.
"""

import os
import sys
import io
import json
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import SkillForgeHTTPHandler

class MockSocket:
    def __init__(self, data=b""):
        self.rfile = io.BytesIO(data)
        self.wfile = io.BytesIO()

    def makefile(self, mode, *args, **kwargs):
        if "r" in mode:
            return self.rfile
        return self.wfile

    def sendall(self, data):
        self.wfile.write(data)


def simulate_request(method, path, body=None):
    body_bytes = json.dumps(body).encode("utf-8") if body else b""
    req = f"{method} {path} HTTP/1.1\r\nHost: localhost\r\n"
    if body_bytes:
        req += f"Content-Length: {len(body_bytes)}\r\nContent-Type: application/json\r\n"
    req += "\r\n"
    full_req = req.encode("utf-8") + body_bytes

    sock = MockSocket(full_req)
    SkillForgeHTTPHandler(sock, ("127.0.0.1", 8000), None)
    return sock.wfile.getvalue()


class TestSkillForgeAPI(unittest.TestCase):
    def test_static_index_html(self):
        output = simulate_request("GET", "/")
        self.assertIn(b"200 OK", output)
        self.assertIn(b"SkillForge", output)

    def test_static_css(self):
        output = simulate_request("GET", "/css/style.css")
        self.assertIn(b"200 OK", output)
        self.assertIn(b"sf-sidebar", output)

    def test_static_js_app(self):
        output = simulate_request("GET", "/js/app.js")
        self.assertIn(b"200 OK", output)
        self.assertIn(b"navigateTo", output)

    def test_static_js_markdown(self):
        output = simulate_request("GET", "/js/markdown.js")
        self.assertIn(b"200 OK", output)
        self.assertIn(b"MarkdownRenderer", output)

    def test_api_status(self):
        output = simulate_request("GET", "/api/status")
        self.assertIn(b"200 OK", output)
        self.assertIn(b"ollama_endpoint", output)

    def test_api_generate(self):
        output = simulate_request("POST", "/api/generate", {"task_desc": "Review Python code"})
        self.assertIn(b"200 OK", output)
        self.assertIn(b"success", output)

    def test_api_validate(self):
        valid_md = "---\nname: python-review\ndescription: Review Python code.\n---\n# Purpose\nReview code."
        output = simulate_request("POST", "/api/validate", {"skill_content": valid_md})
        self.assertIn(b"200 OK", output)
        self.assertIn(b"is_valid", output)

    def test_manual_feedback_requires_local_model(self):
        output = simulate_request("POST", "/api/improve", {
            "skill_content": "# Existing skill",
            "manual_feedback": "Add troubleshooting steps.",
            "use_local_llm": False
        })
        self.assertIn(b"503 Service Unavailable", output)
        self.assertIn(b"Connect to Ollama", output)

    def test_manual_feedback_rejects_oversized_request(self):
        output = simulate_request("POST", "/api/improve", {
            "skill_content": "# Existing skill",
            "manual_feedback": "x" * 2001,
            "use_local_llm": True
        })
        self.assertIn(b"400 Bad Request", output)
        self.assertIn(b"2,000 characters or fewer", output)

    def test_manual_feedback_applies_local_model_revision(self):
        with patch("app.improve_skill_content", return_value="---\nname: revised\ndescription: Revised.\n---\n# Revised\n") as improve:
            output = simulate_request("POST", "/api/improve", {
                "skill_content": "# Existing skill",
                "manual_feedback": "Add examples.",
                "use_local_llm": True
            })
        self.assertIn(b"200 OK", output)
        response = json.loads(output.split(b"\r\n\r\n", 1)[1])
        self.assertTrue(response["success"])
        self.assertIn("# Revised", response["improved_content"])
        self.assertEqual(improve.call_args.kwargs["current_content"], "# Existing skill")
        self.assertEqual(improve.call_args.kwargs["manual_feedback"], "Add examples.")

    def test_api_export_zip(self):
        output = simulate_request("POST", "/api/export", {"folder_name": "test-export", "skill_content": "# Test"})
        self.assertIn(b"200 OK", output)
        self.assertIn(b"application/zip", output)
        self.assertIn(b"PK", output)

if __name__ == "__main__":
    unittest.main()
