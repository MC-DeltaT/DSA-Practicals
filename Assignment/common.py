import random


__all__ = [
    "NormalDistribution"
]


class NormalDistribution:
    def __init__(self, mean: float, std: float) -> None:
        self._mean = mean
        self._std = std

    def __call__(self) -> float:
        return random.normalvariate(self._mean, self._std)


def hash_str(s: str):
    res = 0
    for c in s:
        res = 33 * res + ord(c)
    return res
