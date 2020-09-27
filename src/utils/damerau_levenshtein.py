def damerau_levenshtein(s1: str, s2: str, limit: int) -> bool:
    """Whether Damerau-Levensthein distance is less than limit."""
    if len(s1) < len(s2):
        return damerau_levenshtein(s2, s1, limit)

    if not s2:
        return len(s1) < limit

    if not limit:
        return s1 == s2

    if abs(len(s1) - len(s2)) > limit:
        return False

    if max(len(s1), len(s2)) < limit:
        return True

    if s1[0] == s2[0]:
        try:
            return (
                damerau_levenshtein(s1[1:], s2[1:], limit)
                or damerau_levenshtein(s1[1:], s2, limit - 1)
                or damerau_levenshtein(s1, s2[1:], limit - 1)
                or damerau_levenshtein(s1[1] + s1[0] + s1[1:], s2, limit - 1)
            )

        except IndexError:
            return False

    try:
        return (
            damerau_levenshtein(s1[1:], s2[1:], limit - 1)
            or damerau_levenshtein(s1[1:], s2, limit - 1)
            or damerau_levenshtein(s1, s2[1:], limit - 1)
            or damerau_levenshtein(s1[1] + s1[0] + s1[1:], s2, limit - 1)
        )
    except IndexError:
        return False
