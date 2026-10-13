from pathlib import Path

from fastapi.testclient import TestClient
from agents.api import app
from cli import main as primary_cli
from qrng_entropy.cli import main as secondary_cli


def test_both_clis_write_known_answer(tmp_path, capsys):
    source = tmp_path / "input.txt"
    dest = tmp_path / "bits.txt"
    source.write_text("01 10 00 11 01", encoding="utf-8")
    for cli in (primary_cli, secondary_cli):
        assert cli(["extract", "-i", str(source), "-o", str(dest)]) == 0
        assert dest.read_text(encoding="utf-8") == "010\n"
    assert "Extracted 3 bits" in capsys.readouterr().err


def test_cli_rejects_invalid_file(tmp_path):
    source = tmp_path / "invalid.txt"
    source.write_text("0112", encoding="utf-8")
    assert primary_cli(["extract", "-i", str(source)]) == 1
    assert secondary_cli(["extract", "-i", str(source)]) == 1


def test_browser_ui_and_api():
    client = TestClient(app)
    page = client.get("/")
    assert page.status_code == 200
    assert "extractor.js" in page.text
    assert client.get("/extractor.js").status_code == 200
    response = client.post("/api/extract", json={"bits": "01 10 00 11 01"})
    assert response.status_code == 200
    assert response.json()["output_bits"] == "010"
    assert client.post("/api/extract", json={"bits": "0102"}).status_code == 422
