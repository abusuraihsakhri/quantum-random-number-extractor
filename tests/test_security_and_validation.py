"""
Security and input validation tests for Quantum Random Number Extractor.
"""
import sys
import os
import warnings
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import math
from agents.base import AuditTrail, PHIGuard, SecurityException, assert_no_phi
from agents.models import SystemTaskPayload, UrgencyLevel


class TestAuditTrailSecurity:
    """Test that audit trail uses secure key generation."""

    def test_audit_trail_generates_ephemeral_key_without_env(self):
        """Without AUDIT_SECRET_KEY, should generate a random key and warn."""
        os.environ.pop("AUDIT_SECRET_KEY", None)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            trail = AuditTrail()
            assert len(w) == 1
            assert "AUDIT_SECRET_KEY not set" in str(w[0].message)
            assert issubclass(w[0].category, RuntimeWarning)
        # Key should be 64 hex chars (32 bytes)
        assert len(trail.secret_key) == 64

    def test_audit_trail_uses_env_key_when_set(self):
        """With AUDIT_SECRET_KEY set, should use that key."""
        os.environ["AUDIT_SECRET_KEY"] = "my-test-secret-key"
        try:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                trail = AuditTrail()
                assert len(w) == 0
            assert trail.secret_key == b"my-test-secret-key"
        finally:
            os.environ.pop("AUDIT_SECRET_KEY", None)

    def test_audit_trail_uses_explicit_key(self):
        """Explicit key parameter should take precedence."""
        os.environ["AUDIT_SECRET_KEY"] = "env-key"
        try:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                trail = AuditTrail(secret_key="explicit-key")
                assert len(w) == 0
            assert trail.secret_key == b"explicit-key"
        finally:
            os.environ.pop("AUDIT_SECRET_KEY", None)

    def test_audit_trail_unique_ephemeral_keys(self):
        """Each instance without env var should get a unique key."""
        os.environ.pop("AUDIT_SECRET_KEY", None)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            t1 = AuditTrail()
            t2 = AuditTrail()
        assert t1.secret_key != t2.secret_key


class TestPHIGuard:
    """Test PHI detection patterns."""

    def test_mrn_detection(self):
        with pytest.raises(SecurityException):
            assert_no_phi("Patient MRN-12345678")

    def test_ssn_detection(self):
        with pytest.raises(SecurityException):
            assert_no_phi("SSN: 123-45-6789")

    def test_phone_detection(self):
        with pytest.raises(SecurityException):
            assert_no_phi("Call 555-123-4567")

    def test_email_detection(self):
        with pytest.raises(SecurityException):
            assert_no_phi("Email: patient@hospital.org")

    def test_clean_text_passes(self):
        assert_no_phi("Analytical specimen KEY-001 optimal")  # Should not raise

    def test_empty_text_passes(self):
        assert_no_phi("")  # Should not raise

    def test_none_handled(self):
        assert_no_phi(None)  # Should not raise

    def test_redact_phi(self):
        result = PHIGuard.redact_phi("Patient MRN-12345678 is here")
        assert "REDACTED_IDENTIFIER" in result
        assert "MRN-12345678" not in result


class TestInputValidation:
    """Test SystemTaskPayload input validation."""

    def test_nan_metric_rejected(self):
        with pytest.raises(Exception):  # ValidationError
            SystemTaskPayload(task_id="T1", target_identifier="K1", primary_metric=float("nan"))

    def test_inf_metric_rejected(self):
        with pytest.raises(Exception):  # ValidationError
            SystemTaskPayload(task_id="T1", target_identifier="K1", primary_metric=float("inf"))

    def test_negative_inf_metric_rejected(self):
        with pytest.raises(Exception):  # ValidationError
            SystemTaskPayload(task_id="T1", target_identifier="K1", secondary_metric=float("-inf"))

    def test_empty_task_id_rejected(self):
        with pytest.raises(Exception):  # ValidationError
            SystemTaskPayload(task_id="", target_identifier="K1", primary_metric=10.0)

    def test_whitespace_task_id_rejected(self):
        with pytest.raises(Exception):  # ValidationError
            SystemTaskPayload(task_id="   ", target_identifier="K1", primary_metric=10.0)

    def test_valid_payload_accepted(self):
        p = SystemTaskPayload(task_id="T1", target_identifier="K1", primary_metric=10.0, secondary_metric=5.0)
        assert p.task_id == "T1"
        assert p.primary_metric == 10.0

    def test_zero_metrics_accepted(self):
        p = SystemTaskPayload(task_id="T1", target_identifier="K1", primary_metric=0.0, secondary_metric=0.0)
        assert p.primary_metric == 0.0

    def test_negative_metrics_accepted(self):
        """Negative values are mathematically finite and should be accepted."""
        p = SystemTaskPayload(task_id="T1", target_identifier="K1", primary_metric=-5.0, secondary_metric=-3.0)
        assert p.primary_metric == -5.0


class TestAuditIntegrity:
    """Test audit trail integrity verification."""

    def test_empty_trail_is_valid(self):
        os.environ.pop("AUDIT_SECRET_KEY", None)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            trail = AuditTrail()
        assert trail.verify_integrity() is True

    def test_single_entry_is_valid(self):
        os.environ.pop("AUDIT_SECRET_KEY", None)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            trail = AuditTrail()
        trail.log("test", "tier1", "EVENT", {"data": "value"})
        assert trail.verify_integrity() is True

    def test_multiple_entries_is_valid(self):
        os.environ.pop("AUDIT_SECRET_KEY", None)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            trail = AuditTrail()
        for i in range(5):
            trail.log("test", "tier1", "EVENT", {"index": i})
        assert trail.verify_integrity() is True
        assert len(trail.get_trail()) == 5
