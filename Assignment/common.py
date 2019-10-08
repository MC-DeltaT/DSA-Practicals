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
