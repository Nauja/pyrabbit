__all__ = ["_clamp", "_clamp01"]


def _clamp(v, a, b):
    return max(min(v, b), a)


def _clamp01(v):
    return _clamp(v, 0, 1)
