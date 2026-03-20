from __future__ import annotations

import random
from importlib import resources
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

_MAX_INLINE_RESULTS = 49


class NoFactsFoundError(ValueError):
    def __init__(self, path: Path) -> None:
        super().__init__(f"No facts found in {path}")


def load_facts_from_path(path: Path) -> tuple[str, ...]:
    facts = tuple(
        line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    )
    if not facts:
        raise NoFactsFoundError(path)
    return facts


def load_packaged_facts() -> tuple[str, ...]:
    facts_resource = resources.files("jeff_dean_bot").joinpath("facts.txt")
    with resources.as_file(facts_resource) as facts_path:
        return load_facts_from_path(facts_path)


def levenshtein_distance(left: str, right: str, *, ignore_case: bool = True) -> int:
    if ignore_case:
        left = left.lower()
        right = right.lower()

    if len(left) < len(right):
        return levenshtein_distance(right, left, ignore_case=False)

    if not right:
        return len(left)

    previous_row = list(range(len(right) + 1))
    for row_index, left_char in enumerate(left, start=1):
        current_row = [row_index]
        for column_index, right_char in enumerate(right, start=1):
            insertion_cost = previous_row[column_index] + 1
            deletion_cost = current_row[column_index - 1] + 1
            substitution_cost = previous_row[column_index - 1] + (left_char != right_char)
            current_row.append(min(insertion_cost, deletion_cost, substitution_cost))
        previous_row = current_row

    return previous_row[-1]


def search_facts(
    query: str,
    facts: Sequence[str],
    *,
    max_results: int = _MAX_INLINE_RESULTS,
) -> list[str]:
    normalized_query = query.strip()
    if not normalized_query:
        return list(facts[:max_results])

    lowered_query = normalized_query.lower()
    matches = [
        fact
        for fact in facts
        if lowered_query in fact.lower() or levenshtein_distance(normalized_query, fact) < 3
    ]
    return matches[:max_results]


def fallback_facts(
    facts: Sequence[str],
    *,
    rng: random.Random | None = None,
    limit: int = _MAX_INLINE_RESULTS,
) -> list[str]:
    chooser = rng or random.Random()
    if len(facts) <= limit:
        return list(facts)

    start_index = chooser.randint(0, len(facts) - limit)
    return list(facts[start_index : start_index + limit])


def random_fact(facts: Sequence[str], *, rng: random.Random | None = None) -> str:
    chooser = rng or random.Random()
    return chooser.choice(tuple(facts))
