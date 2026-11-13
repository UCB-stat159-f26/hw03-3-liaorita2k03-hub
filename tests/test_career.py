from pathlib import Path
from urllib.error import URLError

import pytest

from tennis_career import career
from tennis_career import get_career_matches


_FIXTURES = Path(__file__).parent / "fixtures"
_PLAYER_INDEX = 'var playerlist = ["(W) Serena Williams", "(M) Rafael Nadal"];'


@pytest.fixture
def requested_paths(monkeypatch):
    calls = []
    responses = {
        "mwplayerlist.js": _PLAYER_INDEX,
        "jsmatches/SerenaWilliams.js": "var dob=19810926;",
        "jsmatches/RafaelNadal.js": "var dob=19860603;",
    }
    fixture_files = {
        "jsmatches/SerenaWilliamsCareer.js": "FemalePlayerCareer.js",
        "jsmatches/RafaelNadalCareer.js": "MalePlayerCareer.js",
    }

    def fake_download(path):
        calls.append(path)
        if path in responses:
            return responses[path]
        if path in fixture_files:
            return (_FIXTURES / fixture_files[path]).read_text(encoding="utf-8")
        pytest.fail(f"Unexpected download path: {path}")

    monkeypatch.setattr(career, "_download_text", fake_download)
    return calls


@pytest.mark.parametrize("name", ["serena williams", "Serena Williams", "SerenaWilliams"])
def test_serena_name_variants(name, requested_paths):
    matches = get_career_matches(name)

    assert matches.iloc[0]["result"] == "L"
    assert matches.iloc[0]["age_difference"] < 0
    assert requested_paths == [
        "mwplayerlist.js",
        "jsmatches/SerenaWilliams.js",
        "jsmatches/SerenaWilliamsCareer.js",
    ]


def test_nadal_uses_opponent_age(requested_paths):
    matches = get_career_matches("Rafael Nadal")

    assert matches.iloc[0]["opponent_age"] == pytest.approx(22.264202601)
    assert requested_paths[-1] == "jsmatches/RafaelNadalCareer.js"


def test_unknown_player_stops_after_index_lookup(requested_paths):
    with pytest.raises(ValueError, match="Player not found on Tennis Abstract: GastonSanchez"):
        get_career_matches("GastonSanchez")

    assert requested_paths == ["mwplayerlist.js"]


def test_download_failure_has_its_own_error(monkeypatch):
    def fail_download(*args, **kwargs):
        raise URLError("simulated connection failure")

    monkeypatch.setattr(career, "urlopen", fail_download)

    with pytest.raises(RuntimeError, match="Could not download Tennis Abstract file"):
        get_career_matches("Serena Williams")
