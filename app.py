"""
SkillForge — AI Agent Skill Studio
Modern Full-Stack Python Backend serving pure HTML/CSS/JS Frontend.
Zero external server dependencies required (built-in multi-threaded HTTP server).
"""

import sys
import os
import json
import mimetypes
import argparse
import datetime
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# Ensure root directory is on Python path
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from validator.skill_validator import validate_skill
from generator.skill_generator import generate_mock_skill, generate_skill_with_ollama, slugify
from generator.ollama_client import OllamaClient
from evaluator.test_runner import run_skill_tests, improve_skill_content
from exporter.zip_exporter import create_skill_zip, sanitize_folder_name, generate_file_tree_view

# In-memory session state for Ollama detection cache and skills history
SERVER_STATE = {
    "ollama_endpoint": "http://localhost:11434",
    "selected_model": "qwen2.5:7b",
    "active_model": "qwen2.5:7b",
    "ollama_connected": False,
    "ollama_models": [],
    "ollama_status_message": "",
    "skills_history": []
}

FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")


class SkillForgeHTTPHandler(BaseHTTPRequestHandler):
    """Handles static asset serving and REST API endpoints."""

    def log_message(self, format, *args):
        # Concise server logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {self.command} {self.path} - {format % args}\n")

    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def send_error_json(self, message, status=400):
        self.send_json({"success": False, "error": str(message)}, status=status)

    def read_json_body(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length <= 0:
                return {}
            raw = self.rfile.read(content_length)
            return json.loads(raw.decode("utf-8"))
        except Exception as e:
            return {}

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # -------------------------------------------------------------------------
    # GET Request Handler
    # -------------------------------------------------------------------------
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # API Endpoints
        if path == "/api/status":
            self.send_json({
                "ollama_connected": SERVER_STATE["ollama_connected"],
                "ollama_status_message": SERVER_STATE["ollama_status_message"],
                "active_model": SERVER_STATE["active_model"],
                "selected_model": SERVER_STATE["selected_model"],
                "ollama_endpoint": SERVER_STATE["ollama_endpoint"],
                "ollama_models": SERVER_STATE["ollama_models"],
                "skills_count": len(SERVER_STATE["skills_history"])
            })
            return

        # Static File Serving
        if path == "/" or path == "/index.html":
            file_path = os.path.join(FRONTEND_DIR, "index.html")
        else:
            rel_path = path.lstrip("/")
            file_path = os.path.join(FRONTEND_DIR, rel_path)

        # Normalize and ensure no path traversal outside FRONTEND_DIR
        file_path = os.path.abspath(file_path)
        if not file_path.startswith(FRONTEND_DIR) or not os.path.exists(file_path) or os.path.isdir(file_path):
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 Not Found")
            return

        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            if file_path.endswith(".js"):
                mime_type = "application/javascript"
            elif file_path.endswith(".css"):
                mime_type = "text/css"
            else:
                mime_type = "application/octet-stream"

        try:
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"500 Internal Error: {e}".encode("utf-8"))

    # -------------------------------------------------------------------------
    # POST Request Handler
    # -------------------------------------------------------------------------
    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        body = self.read_json_body()

        # 1. Ollama Detect
        if path == "/api/ollama/detect":
            endpoint = body.get("endpoint", SERVER_STATE["ollama_endpoint"])
            client = OllamaClient(endpoint=endpoint)
            res = client.check_connection()
            SERVER_STATE["ollama_endpoint"] = endpoint
            SERVER_STATE["ollama_connected"] = res.get("connected", False)
            SERVER_STATE["ollama_models"] = res.get("models", [])
            SERVER_STATE["ollama_status_message"] = res.get("message", "")
            if res.get("connected") and res.get("models"):
                if "qwen2.5:7b" in res["models"]:
                    SERVER_STATE["selected_model"] = "qwen2.5:7b"
                else:
                    SERVER_STATE["selected_model"] = res["models"][0]
                SERVER_STATE["active_model"] = SERVER_STATE["selected_model"]

            self.send_json(res)
            return

        # 2. Skill Generation
        elif path == "/api/generate":
            task_desc = body.get("task_desc", "").strip()
            if not task_desc:
                self.send_error_json("Task description is required.", status=400)
                return

            category = body.get("category", "Software Development")
            constraints = body.get("constraints", "")
            output_style = body.get("output_style", "Balanced")
            include_checklist = body.get("include_checklist", True)
            use_local_model = body.get("use_local_model", False)
            endpoint = body.get("endpoint", SERVER_STATE["ollama_endpoint"])
            model = body.get("model", SERVER_STATE["selected_model"])
            project_files = body.get("project_files", {})

            try:
                if use_local_model:
                    result = generate_skill_with_ollama(
                        task_desc=task_desc,
                        category=category,
                        constraints=constraints,
                        output_style=output_style,
                        include_checklist=include_checklist,
                        endpoint=endpoint,
                        model=model,
                        project_files=project_files
                    )
                    validation = validate_skill(result["content"])
                    if not validation.get("is_valid"):
                        failed_checks = [
                            check["message"]
                            for check in validation.get("checks", [])
                            if not check.get("passed") and check.get("level") == "error"
                        ]
                        raise ValueError("Generated skill did not pass validation: " + "; ".join(failed_checks))
                else:
                    result = generate_mock_skill(
                        task_desc=task_desc,
                        category=category,
                        constraints=constraints,
                        output_style=output_style,
                        include_checklist=include_checklist,
                        project_files=project_files
                    )
                    validation = validate_skill(result["content"])

                SERVER_STATE["active_model"] = result["model"]
                SERVER_STATE["skills_history"].append({
                    "name": result["name"],
                    "category": category,
                    "content": result["content"],
                    "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                })

                self.send_json({
                    "success": True,
                    "skill": result,
                    "validation": validation
                })
            except Exception as e:
                self.send_error_json(str(e), status=500)
            return

        # 3. Validation
        elif path == "/api/validate":
            skill_content = body.get("skill_content", "")
            val_res = validate_skill(skill_content)
            self.send_json(val_res)
            return

        # 4. Behavioral Tests
        elif path == "/api/test":
            skill_content = body.get("skill_content", "")
            task_desc = body.get("task_desc", "")
            use_local_llm = body.get("use_local_llm", False)
            endpoint = body.get("endpoint", SERVER_STATE["ollama_endpoint"])
            model = body.get("model", SERVER_STATE["selected_model"])

            test_res = run_skill_tests(
                skill_content=skill_content,
                task_desc=task_desc,
                use_local_llm=use_local_llm,
                endpoint=endpoint,
                model=model
            )
            self.send_json(test_res)
            return

        # 5. Self-Improvement
        elif path == "/api/improve":
            skill_content = body.get("skill_content", "")
            failed_tests = body.get("failed_tests", [])
            manual_feedback = body.get("manual_feedback", "").strip()
            use_local_llm = body.get("use_local_llm", False)
            endpoint = body.get("endpoint", SERVER_STATE["ollama_endpoint"])
            model = body.get("model", SERVER_STATE["selected_model"])

            if manual_feedback and not use_local_llm:
                self.send_error_json(
                    "Connect to Ollama and enable local model generation to apply manual feedback.",
                    status=503
                )
                return
            if manual_feedback and len(manual_feedback) > 2000:
                self.send_error_json("Manual feedback must be 2,000 characters or fewer.", status=400)
                return

            try:
                improved = improve_skill_content(
                    current_content=skill_content,
                    failed_tests=failed_tests,
                    use_local_llm=use_local_llm,
                    endpoint=endpoint,
                    model=model,
                    manual_feedback=manual_feedback
                )
            except RuntimeError as e:
                self.send_error_json(str(e), status=502)
                return
            self.send_json({"success": True, "improved_content": improved})
            return

        # 6. ASCII Directory Tree
        elif path == "/api/tree":
            folder_name = body.get("folder_name", "my-skill")
            project_files = body.get("project_files", {})
            safe_slug = sanitize_folder_name(folder_name)
            tree = generate_file_tree_view(safe_slug, project_files=project_files)
            self.send_json({"tree": tree})
            return

        # 7. ZIP Export
        elif path == "/api/export":
            folder_name = body.get("folder_name", "my-skill")
            skill_content = body.get("skill_content", "")
            project_files = body.get("project_files", {})
            safe_slug = sanitize_folder_name(folder_name)

            zip_bytes = create_skill_zip(
                folder_name=safe_slug,
                skill_content=skill_content,
                include_metadata_manifest=True,
                project_files=project_files
            )

            self.send_response(200)
            self.send_header("Content-Type", "application/zip")
            self.send_header("Content-Disposition", f'attachment; filename="{safe_slug}.zip"')
            self.send_header("Content-Length", str(len(zip_bytes)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(zip_bytes)
            return

        else:
            self.send_error_json("Endpoint not found", status=404)


def run_server(host="0.0.0.0", port=8501):
    """Initializes and runs the multi-threaded SkillForge server."""
    client = OllamaClient(endpoint=SERVER_STATE["ollama_endpoint"])
    res = client.check_connection()
    SERVER_STATE["ollama_connected"] = res.get("connected", False)
    SERVER_STATE["ollama_models"] = res.get("models", [])
    SERVER_STATE["ollama_status_message"] = res.get("message", "")
    if res.get("connected") and res.get("models"):
        if "qwen2.5:7b" in res["models"]:
            SERVER_STATE["selected_model"] = "qwen2.5:7b"
        else:
            SERVER_STATE["selected_model"] = res["models"][0]
        SERVER_STATE["active_model"] = SERVER_STATE["selected_model"]

    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, SkillForgeHTTPHandler)
    display_host = "localhost" if host == "0.0.0.0" else host
    print("=" * 64)
    print("  ❖ SkillForge — AI Agent Skill Studio")
    print(f"  ⚡ Pure HTML, CSS, JS Frontend running at:")
    print(f"     http://{display_host}:{port}")
    print("=" * 64)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down SkillForge server...")
        httpd.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SkillForge Web Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8501, help="Port to bind (default: 8501)")
    args = parser.parse_args()

    run_server(host=args.host, port=args.port)
