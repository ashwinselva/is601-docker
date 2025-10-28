import sys
from pathlib import Path
import pytest
import logging

# Skip tests if required third-party packages are not installed in the test env.
pytest.importorskip("qrcode")
pytest.importorskip("validators")

# Ensure project root is on sys.path so `from main import ...` works when pytest
# collects tests from the `tests/` directory.
sys.path.append(str(Path(__file__).resolve().parents[1]))

from main import is_valid_url, generate_qr_code


def test_is_valid_url_true():
    assert is_valid_url("https://www.example.com") is True


def test_is_valid_url_false(caplog):
    caplog.set_level(logging.ERROR)
    assert is_valid_url("not_a_url") is False
    assert "Invalid URL provided" in caplog.text


def test_generate_qr_creates_file(tmp_path):
    url = "https://www.example.com"
    out_file = tmp_path / "test_qr.png"
    # Ensure parent dir exists
    out_file.parent.mkdir(parents=True, exist_ok=True)

    # Should create a PNG file when given a valid URL
    generate_qr_code(url, out_file, fill_color='black', back_color='white')

    assert out_file.exists()
    assert out_file.stat().st_size > 0
