from pathlib import Path

import pytest

from app.certificates import verify_report
from app.contracts import ChallengeRequest
from app.demo import fixture
from app.lab import challenge
from tools.local_smoke import ROOT, offline_environment, tamper_report


def test_offline_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NEXUS_API_KEY", "must-not-propagate")
    monkeypatch.setenv("OTHER_SECRET", "must-not-propagate")
    monkeypatch.setenv("ALPHALITMUS_ENABLE_NEXUS", "true")
    monkeypatch.setenv("ALPHALITMUS_ENABLE_NEXUS_BACKTEST", "true")
    monkeypatch.setenv("HTTPS_PROXY", "must-not-propagate")
    temporary = ROOT / ".smoke-test-temp"
    env = offline_environment(temporary)
    assert "must-not-propagate" not in env.values()
    assert env["ALPHALITMUS_ENABLE_NEXUS"] == "false"
    assert env["ALPHALITMUS_ENABLE_NEXUS_BACKTEST"] == "false"
    assert env["ALPHALITMUS_ENV"] == "test"
    assert all(Path(env[key]).is_relative_to(ROOT) for key in ("TEMP", "TMP", "TMPDIR", "HOME"))


def test_reason_tamper_preserves_original() -> None:
    report = challenge(ChallengeRequest(research=fixture("mixed")))
    before = report.model_dump(mode="json")
    damaged = tamper_report(report)
    assert report.model_dump(mode="json") == before
    changed = damaged.model_dump(mode="json")
    changed["test_matrix"][0]["reason"] = before["test_matrix"][0]["reason"]
    assert changed == before
    assert verify_report(report).valid
    checked = verify_report(damaged)
    assert not checked.valid
    assert "CONTENT_HASH_MISMATCH" in checked.errors
