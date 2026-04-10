"""
Centralised run logger for all agents.

Usage:
    from agents.logger import log

    log.info("message")          # timestamped to console + file
    log.agent_start("Worker", 3) # structured agent lifecycle events
    log.agent_end("Worker", 3, elapsed_seconds=42)
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

_ROOT = Path(__file__).parent.parent
_LOG_DIR = _ROOT / "logs"
_LOG_DIR.mkdir(exist_ok=True)

_run_ts = datetime.now().strftime("%Y%m%d_%H%M%S")
_LOG_FILE = _LOG_DIR / f"run_{_run_ts}.log"

# ── internal logger ────────────────────────────────────────────────────────────
_logger = logging.getLogger("trainer")
_logger.setLevel(logging.WARNING)

_fmt = logging.Formatter("%(asctime)s  %(levelname)-7s  %(message)s", datefmt="%H:%M:%S")

# file handler — full detail
_fh = logging.FileHandler(_LOG_FILE, encoding="utf-8")
_fh.setLevel(logging.DEBUG)
_fh.setFormatter(_fmt)
_logger.addHandler(_fh)

# console handler — info and above
_ch = logging.StreamHandler(sys.stdout)
_ch.setLevel(logging.INFO)
_ch.setFormatter(_fmt)
_logger.addHandler(_ch)


# ── public helpers ─────────────────────────────────────────────────────────────
class _AgentLogger:
    """Thin wrapper that adds structured agent lifecycle methods."""

    def debug(self, msg: str) -> None:
        _logger.debug(msg)

    def info(self, msg: str) -> None:
        _logger.info(msg)

    def warning(self, msg: str) -> None:
        _logger.warning(msg)

    def error(self, msg: str) -> None:
        _logger.error(msg)

    def agent_start(self, agent: str, label: str | int = "") -> datetime:
        """Log that an agent started. Returns start time for elapsed calculation."""
        suffix = f" — {label}" if label != "" else ""
        _logger.info(f"[{agent}] START{suffix}")
        return datetime.now()

    def agent_end(self, agent: str, label: str | int = "", *, start: datetime) -> None:
        """Log that an agent finished, including elapsed seconds."""
        elapsed = int((datetime.now() - start).total_seconds())
        suffix = f" — {label}" if label != "" else ""
        _logger.info(f"[{agent}] END{suffix}  ({elapsed}s)")

    @property
    def log_file(self) -> Path:
        return _LOG_FILE


log = _AgentLogger()
