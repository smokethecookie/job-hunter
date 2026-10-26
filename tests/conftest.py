import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "mcp-servers" / "hunter"))
sys.path.insert(0, str(ROOT / "automation"))

import server  # noqa: E402
import reminder  # noqa: E402


@pytest.fixture
def data_dir(tmp_path, monkeypatch):
    """Point the server and reminder at a temporary data folder."""
    monkeypatch.setattr(server, "DATA_DIR", tmp_path)
    monkeypatch.setattr(server, "REPORTS_DIR", tmp_path / "reports")
    monkeypatch.setattr(reminder, "DATA_DIR", tmp_path)
    monkeypatch.setattr(reminder, "APPLICATIONS_FILE", tmp_path / "applications.json")
    return tmp_path
