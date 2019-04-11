__all__ = [
    "responsibilities"
]


def _clamp(v, a, b):
    return max(min(v, b), a)


def _clamp01(v):
    return _clamp(v, 0, 1)


def responsibilities(calls, threshold):
    return _clamp01(1 - (calls / threshold))
