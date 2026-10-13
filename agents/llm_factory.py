"""
Deterministic local placeholder. No external LLM service is implemented.
"""
from typing import Dict, Any, Optional
from .base import PHIGuard


class MockLLM:
    def __init__(self, system_name: str = "Quantum Random Number Extractor"):
        self.system_name = system_name

    def invoke(self, prompt: str) -> str:
        PHIGuard.assert_no_phi(prompt)
        return f"[{self.system_name} Mock]: No external model was called. Input received: '{prompt[:60]}...'. This response does not verify scientific or regulatory compliance."


class LLMFactory:
    """Provide a local deterministic test adapter only."""

    @staticmethod
    def create(provider: str = "mock", system_name: str = "Quantum Random Number Extractor"):
        prov = str(provider).lower()
        if prov in ["mock", "deterministic", "test"]:
            return MockLLM(system_name)
        raise ValueError("Unsupported model provider: only mock/deterministic/test is implemented")
