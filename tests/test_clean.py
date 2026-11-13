from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from tennis_career._clean import _clean_career_matches


_FIXTURES = Path(__file__).parent / "fixtures"


def _read_fixture(filename):
    return (_FIXTURES / filename).read_text(encoding="utf-8")


def test_female_match_calculates_ages_from_birth_dates():
    matches = _clean_career_matches(
        _read_fixture("FemalePlayerCareer.js"),
        "19810926",
        opponent_age_format="birth_date",
    )
    first = matches.iloc[0]
    match_day = date(1995, 10, 30)
    expected_player_age = (match_day - date(1981, 9, 26)).days / 365.25
    expected_opponent_age = (match_day - date(1977, 1, 19)).days / 365.25

    assert first["match_date"] == pd.Timestamp("1995-10-30")
    assert first["player_age"] == pytest.approx(expected_player_age)
    assert first["opponent_age"] == pytest.approx(expected_opponent_age)
    assert first["age_difference"] == pytest.approx(
        expected_player_age - expected_opponent_age
    )
    assert first["age_difference"] < 0
    assert first["result"] == "L"


def test_female_match_with_missing_opponent_birth_date_is_dropped():
    matches = _clean_career_matches(
        _read_fixture("FemalePlayerCareer.js"),
        "19810926",
        opponent_age_format="birth_date",
    )

    assert matches["match_date"].tolist() == [pd.Timestamp("1995-10-30")]


def test_male_matches_use_supplied_opponent_ages():
    matches = _clean_career_matches(
        _read_fixture("MalePlayerCareer.js"),
        "19860603",
        opponent_age_format="age",
    )
    first = matches.iloc[0]
    expected_player_age = (date(2002, 4, 29) - date(1986, 6, 3)).days / 365.25

    assert matches["result"].tolist() == ["L", "L", "W"]
    assert first["opponent_age"] == pytest.approx(22.264202601)
    assert first["age_difference"] == pytest.approx(
        expected_player_age - 22.264202601
    )
