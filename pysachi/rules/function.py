__all__ = ["responsibilities"]
from .utils import *


def responsibilities(calls, threshold):
    return _clamp01(1 - (calls / threshold))
