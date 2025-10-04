import re
from itertools import zip_longest

from thefuzz import fuzz


def get_exact_matches(
        values_sp: list[tuple],
        values_sp_assem: list[tuple]
) -> tuple[list[tuple], list[tuple], list[tuple]]:
    values_sp_assem_map: dict[str: list] = {}
    for i in values_sp_assem:
        key = i[0]
        values_sp_assem_map.setdefault(key, []).append(i)

    matches: list[tuple] = []
    values_sp_rest: list[tuple] = []

    for sp1 in values_sp:
        if not sp1[0]:
            continue
        key = sp1[0]
        if key in values_sp_assem_map and values_sp_assem_map[key]:
            sp2 = values_sp_assem_map[key].pop(0)
            matches.append((
                *sp1[:2],
                sp1[1] - sp2[1],
                *sp2[:2],
                sp1[3],
                sp2[3],
                sp1[4]
            ))
        else:
            values_sp_rest.append(sp1)

    values_sp_assem_rest = [t for values in values_sp_assem_map.values() for t in values]

    return matches, values_sp_rest, values_sp_assem_rest


def get_fuzzy_matches(
        values_sp: list[tuple],
        values_sp_assem: list[tuple]
) -> tuple[list[tuple], list[tuple], list[tuple]]:
    matches: list[tuple] = []
    values_sp_rest: list[tuple] = []
    for sp1 in values_sp:
        match = None
        for sp2 in values_sp_assem:
            score = fuzz.ratio(str(sp1[0]), str(sp2[0]))
            if score >= 80:
                matches.append((
                    *sp1[:2],
                    sp1[1] - sp2[1],
                    *sp2[:2],
                    sp1[3],
                    sp2[3],
                    sp1[4]
                ))
                match = sp2
                break
        if match:
            values_sp_assem.remove(match)
        else:
            values_sp_rest.append(sp1)
    return matches, values_sp_rest, values_sp_assem


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def compare_strings(s1: str, s2: str, threshold: int) -> tuple[bool, int]:
    score = fuzz.token_set_ratio(s1, s2)
    return score >= threshold, score


def match_items(
        values_sp: list[tuple],
        values_sp_assem: list[tuple],
        threshold: int
) -> tuple[list[tuple], list[tuple], list[tuple]]:
    matches: list[tuple] = []
    values_sp_rest: list[tuple] = []
    values_sp_assem_rest = values_sp_assem.copy()

    for sp1 in values_sp:
        s1 = normalize(str(sp1[3]))
        best_match = None
        best_score = 0

        for sp2 in values_sp_assem_rest:
            s2 = normalize(str(sp2[3]))
            is_match, score = compare_strings(s1, s2, threshold)
            if score > best_score:
                best_match = (sp1, sp2)
                best_score = score

        if best_match and best_score >= threshold:
            matches.append((
                *best_match[0][:2],
                best_match[0][1] - best_match[1][1],
                *best_match[1][:2],
                best_match[0][3],
                best_match[1][3],
                best_match[0][4]
            ))
            values_sp_assem_rest.remove(best_match[1])
        else:
            values_sp_rest.append(sp1)

    return matches, values_sp_rest, values_sp_assem_rest


def zip_last(sp1: list[tuple], sp2: list[tuple]) -> list[tuple]:
    sp1.sort(key=lambda x: x[3])
    sp2.sort(key=lambda x: x[3])
    return [(*a[:2], '', *b[:2], a[3], b[3], a[4]) for a, b in zip_longest(sp1, sp2, fillvalue=('', '', '', ''))]
