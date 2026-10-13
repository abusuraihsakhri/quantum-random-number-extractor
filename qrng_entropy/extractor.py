"""Demonstration bias extractor for recorded binary measurement outcomes.

Von Neumann extraction assumes independent, identically distributed input bits.
It does not establish that a source is quantum, unpredictable, or SP 800-90B compliant.
"""
import math
import re

MAX_BITS = 1_000_000

def parse_bits(text: str) -> str:
    """Read 0/1 symbols separated by optional whitespace, commas or semicolons."""
    if not isinstance(text, str):
        raise ValueError("Input must be text containing binary outcomes")
    if len(text) > MAX_BITS * 4:
        raise ValueError("Input file exceeds the supported size")
    if re.search(r"[^01\s,;|]", text):
        raise ValueError("Only 0, 1, whitespace, commas, semicolons and | are allowed")
    bits = re.sub(r"[\s,;|]", "", text)
    if len(bits) < 2:
        raise ValueError("At least two binary observations are required")
    if len(bits) > MAX_BITS:
        raise ValueError(f"At most {MAX_BITS:,} observations are supported")
    return bits

def _stats(bits: str) -> dict:
    n = len(bits)
    if not n:
        return {"length": 0, "ones": 0, "fraction_ones": None, "empirical_min_entropy_bits_per_symbol": None}
    ones = bits.count("1")
    p = ones / n
    return {
        "length": n,
        "ones": ones,
        "fraction_ones": p,
        # Plug-in empirical statistic; NOT a confidence-bound entropy assessment.
        "empirical_min_entropy_bits_per_symbol": -math.log2(max(p, 1 - p)),
    }

def extract_bits(bits: str) -> dict:
    """Von Neumann: 01 -> 0, 10 -> 1; 00/11 discarded; trailing odd bit unused."""
    bits = parse_bits(bits)
    out = []
    discarded = 0
    for i in range(0, len(bits) - 1, 2):
        pair = bits[i:i+2]
        if pair == "01":
            out.append("0")
        elif pair == "10":
            out.append("1")
        else:
            discarded += 1
    result = "".join(out)
    return {
        "method": "von_neumann",
        "input": _stats(bits),
        "output": _stats(result),
        "output_bits": result,
        "pairs_examined": len(bits) // 2,
        "pairs_discarded": discarded,
        "trailing_bits_unused": len(bits) % 2,
        "assumptions": "Independent and identically distributed Bernoulli input bits; bias correction is not source certification.",
    }
