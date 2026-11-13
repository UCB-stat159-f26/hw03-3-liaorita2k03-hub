import json
import re

import pandas as pd


_COLUMNS = [
    "match_date",
    "player_age",
    "opponent_age",
    "age_difference",
    "result",
]
_DAYS_PER_YEAR = 365.25


def _parse_matches(js_text):
    assignment = re.search(r"\bmorematchmx\s*=\s*", js_text)
    if assignment is None:
        raise ValueError("Career file is missing the morematchmx array.")
    rows, _ = json.JSONDecoder().raw_decode(js_text[assignment.end():])
    if not isinstance(rows, list):
        raise ValueError("Expected morematchmx to be an array.")
    return rows


def _parse_date(value):
    return pd.to_datetime(value, format="%Y%m%d", errors="coerce")


def _age_on(match_date, birth_date):
    return (match_date - birth_date).days / _DAYS_PER_YEAR


def _get_opponent_age(value, match_date, opponent_age_format):
    if opponent_age_format == "birth_date":
        return _age_on(match_date, _parse_date(value))
    return pd.to_numeric(value, errors="coerce")


def _clean_match(row, player_birth_date, opponent_age_format):
    match_date = _parse_date(row[0])
    player_age = _age_on(match_date, player_birth_date)
    opponent_age = _get_opponent_age(row[16], match_date, opponent_age_format)
    return (
        match_date,
        player_age,
        opponent_age,
        player_age - opponent_age,
        row[4],
    )


def _clean_career_matches(js_text, player_birth_date, *, opponent_age_format):
    if opponent_age_format not in {"birth_date", "age"}:
        raise ValueError("Opponent age format must be 'birth_date' or 'age'.")
    birth_date = _parse_date(player_birth_date)
    if pd.isna(birth_date):
        raise ValueError("Player birth date must be a valid date in YYYYMMDD format.")

    rows = _parse_matches(js_text)
    matches = [
        _clean_match(row, birth_date, opponent_age_format)
        for row in rows
        if len(row) > 16
    ]
    frame = pd.DataFrame(matches, columns=_COLUMNS)
    return frame.dropna(subset=["player_age", "opponent_age"]).reset_index(drop=True)
