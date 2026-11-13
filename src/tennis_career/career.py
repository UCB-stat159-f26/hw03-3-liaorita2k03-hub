import json
import re
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import urlopen

from ._clean import _clean_career_matches


_BASE_URL = "https://www.tennisabstract.com"
_AGE_FORMATS = {"W": "birth_date", "M": "age"}


def _download_text(path):
    try:
        with urlopen(f"{_BASE_URL}/{path}", timeout=30) as response:
            return response.read().decode("utf-8-sig")
    except (URLError, TimeoutError) as error:
        raise RuntimeError(f"Could not download Tennis Abstract file: {path}") from error


def _name_key(name):
    return "".join(name.split()).casefold()


def _read_player_index():
    text = _download_text("mwplayerlist.js")
    assignment = re.search(r"\bvar\s+playerlist\s*=\s*", text)
    if assignment is None:
        raise RuntimeError("Tennis Abstract player index is missing its player list.")
    entries, _ = json.JSONDecoder().raw_decode(text[assignment.end():])
    return entries


def _find_player(player_name):
    key = _name_key(player_name)
    matches = {
        ("".join(entry[4:].split()), entry[1])
        for entry in _read_player_index()
        if entry.startswith(("(M) ", "(W) ")) and _name_key(entry[4:]) == key
    }
    if not matches:
        raise ValueError(f"Player not found on Tennis Abstract: {player_name}")
    if len(matches) > 1:
        raise ValueError(f"Multiple Tennis Abstract players match: {player_name}")
    return matches.pop()


def _lookup_player(player_name):
    player_id, tour = _find_player(player_name)
    metadata = _download_text(f"jsmatches/{quote(player_id, safe='')}.js")
    birth_date = re.search(r"\bvar\s+dob\s*=\s*(\d{8})\s*;", metadata)
    if birth_date is None:
        raise RuntimeError(f"Tennis Abstract birth date unavailable for {player_id}.")
    return player_id, birth_date.group(1), _AGE_FORMATS[tour]


def get_career_matches(player_name):
    """Return career matches with player age, opponent age, and match result."""
    if not isinstance(player_name, str) or not player_name.strip():
        raise ValueError("Player name must be a nonempty string.")
    player_id, birth_date, age_format = _lookup_player(player_name)
    career_js = _download_text(f"jsmatches/{quote(player_id, safe='')}Career.js")
    return _clean_career_matches(
        career_js, birth_date, opponent_age_format=age_format
    )
