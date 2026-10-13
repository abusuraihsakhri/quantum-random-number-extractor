"""Known-answer and validation tests for the educational bit extractor."""
import pytest
from qrng_entropy.extractor import extract_bits, parse_bits

def test_known_answer():
    r = extract_bits("01 10 00 11 01")
    assert r["output_bits"] == "010"
    assert r["pairs_examined"] == 5
    assert r["pairs_discarded"] == 2
    assert r["input"]["length"] == 10
    assert r["output"]["fraction_ones"] == pytest.approx(1 / 3)

def test_odd_and_degenerate():
    r = extract_bits("00001")
    assert r["trailing_bits_unused"] == 1
    assert r["pairs_discarded"] == 2
    assert r["output"]["length"] == 0
    assert r["output"]["empirical_min_entropy_bits_per_symbol"] is None

@pytest.mark.parametrize("bad", ["", "1", "0102", "true", "0x10", "01\u200b", "010\u0000"])
def test_invalid(bad):
    with pytest.raises(ValueError):
        extract_bits(bad)

def test_separators_and_limit():
    assert parse_bits("0,1;1|0\n") == "0110"
    with pytest.raises(ValueError):
        extract_bits("01" * 500001)
