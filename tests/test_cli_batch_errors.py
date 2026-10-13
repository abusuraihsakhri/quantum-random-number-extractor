"""Batch processing should report failures and never leave stale results."""
import pytest
from cli import main as primary
from qrng_entropy.cli import main as secondary

@pytest.mark.parametrize("entry", [primary, secondary])
def test_invalid_row_returns_error_and_overwrites_stale_file(entry, tmp_path):
    source = tmp_path / "input.csv"
    output = tmp_path / "results.csv"
    source.write_text("task_id,target_identifier,primary_metric,secondary_metric\nA,T,invalid,3\n", encoding="utf-8")
    output.write_text("stale-secret-data", encoding="utf-8")
    assert entry(["batch", "-i", str(source), "-o", str(output)]) == 1
    text = output.read_text(encoding="utf-8")
    assert "stale-secret-data" not in text
    assert "primary_metric" in text
    assert len(text.strip().splitlines()) == 1

@pytest.mark.parametrize("entry", [primary, secondary])
def test_valid_batch(entry, tmp_path):
    source = tmp_path / "input.csv"
    output = tmp_path / "results.csv"
    source.write_text("task_id,target_identifier,primary_metric,secondary_metric\nA,T,20,3\n", encoding="utf-8")
    assert entry(["batch", "-i", str(source), "-o", str(output)]) == 0
    assert len(output.read_text(encoding="utf-8").strip().splitlines()) == 2
