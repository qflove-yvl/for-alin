"""One-command local runner for backend + bot.

Usage:
    python app.py
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

try:
    import httpx
except ImportError:
    print("Missing dependency: httpx. Run: pip install -r requirements.txt")
    raise

ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"
BOT_DIR = ROOT / "bot"
ENV_FILE = ROOT / ".env"
ENV_EXAMPLE = ROOT / ".env.example"


def ensure_env_file() -> None:
    if ENV_FILE.exists():
        return
    ENV_FILE.write_text(ENV_EXAMPLE.read_text())
    print("[bootstrap] Created .env from .env.example")


def validate_env() -> None:
    data = ENV_FILE.read_text()
    if "BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN" in data:
        print("[warning] BOT_TOKEN is still default. Set real token in .env")


def start_backend() -> subprocess.Popen:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(BACKEND_DIR)
    cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    return subprocess.Popen(cmd, cwd=BACKEND_DIR, env=env)


def wait_backend_ready(timeout_s: int = 30) -> bool:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            r = httpx.get("http://127.0.0.1:8000/health", timeout=2.0)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(1)
    return False


def start_bot() -> subprocess.Popen:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(BOT_DIR)
    cmd = [sys.executable, "-m", "app.main"]
    return subprocess.Popen(cmd, cwd=BOT_DIR, env=env)


def stop_process(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=8)
    except subprocess.TimeoutExpired:
        proc.kill()


def main() -> int:
    ensure_env_file()
    validate_env()

    backend = start_backend()
    print("[run] backend started")

    if not wait_backend_ready():
        print("[error] backend healthcheck failed on http://127.0.0.1:8000/health")
        stop_process(backend)
        return 1

    bot = start_bot()
    print("[run] bot started")
    print("[info] API docs: http://127.0.0.1:8000/docs")
    print("[info] Press Ctrl+C to stop everything")

    def handle_sigint(_sig, _frame):
        print("\n[shutdown] stopping services...")
        stop_process(bot)
        stop_process(backend)
        raise SystemExit(0)

    signal.signal(signal.SIGINT, handle_sigint)
    signal.signal(signal.SIGTERM, handle_sigint)

    while True:
        if backend.poll() is not None:
            print("[error] backend exited")
            stop_process(bot)
            return backend.returncode or 1
        if bot.poll() is not None:
            print("[error] bot exited")
            stop_process(backend)
            return bot.returncode or 1
        time.sleep(1)


if __name__ == "__main__":
    raise SystemExit(main())
