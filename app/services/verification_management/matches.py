import re
from itertools import chain

from rapidfuzz import fuzz, process

from .excel_utils import _get_cell


def get_matches(spec_ws, spec_model_ws) -> dict[str, list]:
    final_spec: dict[str, list] = {
        'spec': list(_get_cell(spec_ws, min_col=1, max_col=4, min_row=3, values_only=True)),
        'model_spec': list(_get_cell(spec_model_ws, min_row=2, values_only=True)),
        'fuzzy_matches': [],
        'last_matches': [],
    }

    final_spec = final_spec | _split_secondary_items(final_spec['model_spec'])

    final_spec = final_spec | _match_exact_by_article(final_spec['spec'], final_spec['model_spec'])

    spec = final_spec['spec']
    model_spec = final_spec['model_spec']
    fuzzy_thresholds: tuple[int, ...] = (90, 80)
    for t in fuzzy_thresholds:
        matches, spec, model_spec = _match_fuzzy_by_article(spec, model_spec, t)
        final_spec['fuzzy_matches'].extend(matches)

    last_thresholds: tuple[int, ...] = (80, 70, 60, 50, 40, 30)
    for t in last_thresholds:
        matches, spec, model_spec = _match_items_by_description(spec, model_spec, t)
        final_spec['last_matches'].extend(matches)

    final_spec.update({
        'spec': spec,
        'model_spec': model_spec,
    })

    return final_spec


def _split_secondary_items(spec: list[tuple]) -> dict[str, list]:
    primary: list[tuple] = []
    secondary: list[tuple] = []
    keywords: set[str] = {
        'хомут',
        'рама',
        'труба',
        'отвод',
        'патрубок',
        'фланец',
        'переход',
        'тройник',
        'трубка',
    }
    for row in spec:
        name = str(row[3]).lower()
        if any(name.startswith(k) for k in keywords):
            secondary.append(row)
        else:
            primary.append(row)

    return {
        'model_spec': primary,
        'secondary_items': secondary
    }


def _match_exact_by_article(
        spec: list[tuple],
        model_spec: list[tuple]
) -> dict[str, list]:
    """Точное совпадение по первому столбцу."""
    model_spec_map: dict[str: list] = {}
    for row in model_spec:
        model_spec_map.setdefault(row[0], []).append(row)

    matches: list[tuple] = []
    spec_rest: list[tuple] = []

    for sp1 in spec:
        key = sp1[0]
        if not key:
            continue

        rows = model_spec_map.get(key)
        if rows:
            sp2 = rows.pop(0)
            matches.append(_add_compare_count(sp1, sp2))
        else:
            spec_rest.append(sp1)

    model_spec_rest = list(chain.from_iterable(model_spec_map.values()))

    return {
        'exact_matches': matches,
        'spec': spec_rest,
        'model_spec': model_spec_rest
    }


def _match_fuzzy_by_article(
        spec: list[tuple],
        model_spec: list[tuple],
        threshold: int
) -> tuple[list[tuple], list[tuple], list[tuple]]:
    """Нечеткое совпадение по 1-му столбцу"""
    if not spec or not model_spec:
        return [], spec, model_spec

    candidates = [str(row[0]) for row in model_spec]

    matches: list[tuple[tuple, tuple]] = []
    spec_rest: list[tuple] = []
    used_indices: set[int] = set()

    for sp1 in spec:
        key = str(sp1[0])
        if not key:
            spec_rest.append(sp1)
            continue
        result = process.extractOne(  # type: ignore[arg-type]
            key,
            candidates,
            scorer=fuzz.QRatio,
            score_cutoff=threshold
        )

        if result:
            matched_value, score, idx = result
            if idx not in used_indices:
                matches.append(_add_compare_count(sp1, model_spec[idx]))
                used_indices.add(idx)
            else:
                spec_rest.append(sp1)
        else:
            spec_rest.append(sp1)

    model_spec_rest = [
        row for i, row in enumerate(model_spec)
        if i not in used_indices
    ]

    return matches, spec_rest, model_spec_rest


def _match_items_by_description(
        spec: list[tuple],
        model_spec: list[tuple],
        threshold: int
) -> tuple[list[tuple], list[tuple], list[tuple]]:
    """Нечеткое совпадение по 4-му столбцу (описанию)."""
    normalized_sp = [(sp, _normalize(str(sp[3]))) for sp in spec]
    normalized_assem = [(sp, _normalize(str(sp[3]))) for sp in model_spec]

    candidates = [desc for _, desc in normalized_assem]
    index_map = {desc: sp for sp, desc in normalized_assem}

    matches: list[tuple] = []
    spec_rest: list[tuple] = []
    used_indices: set[int] = set()

    for sp1, s1 in normalized_sp:
        if not s1.strip():
            spec_rest.append(sp1)
            continue

        result = process.extractOne(  # type: ignore[arg-type]
            s1,
            candidates,
            scorer=fuzz.token_set_ratio,
            score_cutoff=threshold,
        )

        if result:
            matched_str, score, idx = result
            if idx not in used_indices:
                matches.append(_add_compare_count(sp1, index_map[matched_str]))
                used_indices.add(idx)
            else:
                spec_rest.append(sp1)
        else:
            spec_rest.append(sp1)

    model_spec_rest = [
        t for i, (t, _) in enumerate(normalized_assem)
        if i not in used_indices
    ]

    return matches, spec_rest, model_spec_rest


def _add_compare_count(sp1: tuple, sp2: tuple) -> tuple[tuple, tuple]:
    return (
        (sp1[0], sp1[1], int(sp1[1]) - int(sp2[1]), sp1[2], sp1[3]),
        (sp2[0], sp2[1], None, sp2[2], sp2[3]),
    )


def _normalize(text: str) -> str:
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', text.lower())).strip()
