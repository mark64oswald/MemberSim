"""Distribution classes for weighted random selection."""

from __future__ import annotations

import random
from typing import Generic, Sequence, TypeVar

T = TypeVar("T")


class WeightedChoice(Generic[T]):
    """Select from options with specified probabilities.

    Example:
        gender = WeightedChoice([("M", 0.49), ("F", 0.51)]).select()
        plan_type = WeightedChoice([
            ("HMO", 0.4),
            ("PPO", 0.35),
            ("HDHP", 0.25)
        ]).select()
    """

    def __init__(
        self,
        choices: Sequence[tuple[T, float]],
        seed: int | None = None,
    ):
        """Initialize weighted choice.

        Args:
            choices: List of (value, weight) tuples. Weights need not sum to 1.
            seed: Optional random seed for reproducibility.
        """
        if not choices:
            raise ValueError("choices cannot be empty")

        self._values = [c[0] for c in choices]
        self._weights = [c[1] for c in choices]
        self._rng = random.Random(seed)

        # Validate weights
        if any(w < 0 for w in self._weights):
            raise ValueError("weights cannot be negative")
        if sum(self._weights) == 0:
            raise ValueError("total weight cannot be zero")

    def select(self) -> T:
        """Select a random value according to weights."""
        return self._rng.choices(self._values, weights=self._weights, k=1)[0]

    def select_n(self, n: int) -> list[T]:
        """Select n values (with replacement) according to weights."""
        return self._rng.choices(self._values, weights=self._weights, k=n)


class UniformDistribution:
    """Generate values uniformly between min and max."""

    def __init__(
        self,
        min_val: float,
        max_val: float,
        seed: int | None = None,
    ):
        self.min_val = min_val
        self.max_val = max_val
        self._rng = random.Random(seed)

    def sample(self) -> float:
        """Sample a value from the distribution."""
        return self._rng.uniform(self.min_val, self.max_val)

    def sample_int(self) -> int:
        """Sample an integer value from the distribution."""
        return self._rng.randint(int(self.min_val), int(self.max_val))


class NormalDistribution:
    """Generate values from normal distribution with optional bounds."""

    def __init__(
        self,
        mean: float,
        std_dev: float,
        min_val: float | None = None,
        max_val: float | None = None,
        seed: int | None = None,
    ):
        self.mean = mean
        self.std_dev = std_dev
        self.min_val = min_val
        self.max_val = max_val
        self._rng = random.Random(seed)

    def sample(self) -> float:
        """Sample a value, optionally bounded."""
        value = self._rng.gauss(self.mean, self.std_dev)
        if self.min_val is not None:
            value = max(value, self.min_val)
        if self.max_val is not None:
            value = min(value, self.max_val)
        return value


class AgeDistribution:
    """Generate ages appropriate for health plan populations."""

    def __init__(
        self,
        min_age: int = 0,
        max_age: int = 100,
        commercial_weight: float = 0.7,
        medicare_weight: float = 0.2,
        pediatric_weight: float = 0.1,
        seed: int | None = None,
    ):
        """Initialize age distribution.

        Default weights approximate typical commercial health plan.
        """
        self.min_age = min_age
        self.max_age = max_age
        self._rng = random.Random(seed)

        # Define age band ranges
        band_definitions = {
            "pediatric": (0, 17, pediatric_weight),
            "commercial": (18, 64, commercial_weight),
            "medicare": (65, 100, medicare_weight),
        }

        # Build valid bands based on min/max age constraints
        valid_bands: list[tuple[str, float]] = []
        self._band_ranges: dict[str, tuple[int, int]] = {}

        for band_name, (band_min, band_max, weight) in band_definitions.items():
            # Adjust band range to fit within constraints
            effective_min = max(band_min, min_age)
            effective_max = min(band_max, max_age)

            # Only include band if it has a valid range
            if effective_min <= effective_max:
                valid_bands.append((band_name, weight))
                self._band_ranges[band_name] = (effective_min, effective_max)

        if not valid_bands:
            raise ValueError(f"No valid age bands for range {min_age}-{max_age}")

        self._bands = WeightedChoice(valid_bands, seed=seed)

    def sample(self) -> int:
        """Sample an age from the distribution."""
        band = self._bands.select()
        min_a, max_a = self._band_ranges[band]
        return self._rng.randint(min_a, max_a)
