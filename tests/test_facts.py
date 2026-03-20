from __future__ import annotations

from typing import TYPE_CHECKING

from jeff_dean_bot.facts import (
    fallback_facts,
    levenshtein_distance,
    load_facts_from_path,
    search_facts,
)

if TYPE_CHECKING:
    from pathlib import Path

FACTS = (
    "Jeff Dean proved that P=NP on a whiteboard.",
    "Jeff Dean's keyboard has a dedicated speed-of-light key.",
    "Jeff Dean warns compilers.",
)


def test_load_facts_from_path_skips_empty_lines(tmp_path: Path) -> None:
    facts_file = tmp_path / "facts.txt"
    facts_file.write_text("Alpha\n\nBeta\n", encoding="utf-8")

    assert load_facts_from_path(facts_file) == ("Alpha", "Beta")


def test_levenshtein_distance_is_case_insensitive_by_default() -> None:
    assert levenshtein_distance("Jeff", "jeff") == 0


def test_search_facts_matches_substrings() -> None:
    assert search_facts("compilers", FACTS) == ["Jeff Dean warns compilers."]


def test_search_facts_returns_empty_list_for_no_match() -> None:
    assert search_facts("totally missing", FACTS) == []


def test_fallback_facts_returns_requested_window() -> None:
    results = fallback_facts(FACTS, limit=2)

    assert len(results) == 2
    assert set(results).issubset(set(FACTS))
