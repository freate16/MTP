from __future__ import annotations

import os
os.environ['GDAL_DATA'] = r'D:\anaconda\geo_dl\Library\share\gdal'

import argparse
import contextlib
import io
import json
import sys
import traceback
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


PROJECT_ROOT = Path(__file__).resolve().parent.parent
WEBSITE_DIR = PROJECT_ROOT / "website"
RAG_DIR = PROJECT_ROOT / "chatbot" / "rag"

if str(RAG_DIR) not in sys.path:
    sys.path.insert(0, str(RAG_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class ChatHandler(SimpleHTTPRequestHandler):
    server_version = "GLOFChatServer/1.0"

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        super().end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.end_headers()

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/health":
            self._send_json({"ok": True, "service": "glof-chatbot"})
            return
        super().do_GET()

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path != "/api/chat":
            self.send_error(404, "Unknown endpoint")
            return

        try:
            payload = self._read_json()
            question = str(payload.get("question", "")).strip()
            route = str(payload.get("route", "auto")).strip() or "auto"
            if not question:
                self._send_json({"error": "Question is required."}, status=400)
                return

            response = self._run_chatbot(question, route)
            self._send_json(response)
        except SystemExit as exc:
            self._send_json({"error": str(exc)}, status=500)
        except Exception as exc:
            self._send_json(
                {
                    "error": str(exc),
                    "traceback": traceback.format_exc(),
                },
                status=500,
            )

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length > 20000:
            raise ValueError("Request body is too large.")
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw or "{}")

    def _run_chatbot(self, question: str, route: str) -> dict:
        from chatbot.agentic_rag.agent import run_reasoning_agent

        log_buffer = io.StringIO()
        with contextlib.redirect_stdout(log_buffer):
            try:
                run_reasoning_agent(question, max_steps=8)
            except Exception as e:
                print(f"Agent crashed: {e}")

        # Extract the final answer and logs
        output_str = log_buffer.getvalue()

        final_answer = "No final answer reached by the agent."
        logs = []
        for line in output_str.splitlines():
            line = line.strip()
            if not line: continue
            if "Final Answer:" not in line:
                logs.append(line)

        # Robust multi-line extraction
        if "Final Answer:" in output_str:
            # Split by Final Answer:, take the second half
            after_final = output_str.split("Final Answer:", 1)[1]
            # The agent prints '============================================================'
            # and '[Agent Finished Successfully]' after the final answer. We split by the first '=' line to trim it.
            final_answer = after_final.split("=======")[0].strip()

        return {
            "answer": final_answer,
            "route": "agentic",
            "has_kg_context": True,
            "logs": logs[-40:]
        }

    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve the GLOF website and chatbot API locally.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not WEBSITE_DIR.exists():
        raise SystemExit(f"Website directory not found: {WEBSITE_DIR}")

    handler = partial(ChatHandler, directory=str(WEBSITE_DIR))
    server = ThreadingHTTPServer((args.host, args.port), handler)
    url = f"http://{args.host}:{args.port}"
    print(f"Serving website: {WEBSITE_DIR}")
    print(f"Chat API: {url}/api/chat")
    print(f"Open: {url}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
