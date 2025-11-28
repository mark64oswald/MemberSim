"""Cohort generation with demographic constraints."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Callable, Generic, Iterator, TypeVar

from membersim.generation.distributions import WeightedChoice
from membersim.generation.seed_manager import SeedManager

logger = logging.getLogger(__name__)

T = TypeVar("T")


@dataclass
class CohortConstraints:
    """Demographic constraints for cohort generation.

    All percentages should sum to 1.0 within their category.
    """

    gender_distribution: dict[str, float] = field(default_factory=lambda: {"M": 0.49, "F": 0.51})
    age_distribution: dict[str, float] = field(
        default_factory=lambda: {
            "0-17": 0.10,
            "18-34": 0.20,
            "35-54": 0.35,
            "55-64": 0.20,
            "65+": 0.15,
        }
    )
    plan_distribution: dict[str, float] = field(
        default_factory=lambda: {
            "HMO": 0.35,
            "PPO": 0.40,
            "HDHP": 0.25,
        }
    )
    state_distribution: dict[str, float] | None = None

    def validate(self) -> list[str]:
        """Validate constraints sum to ~1.0."""
        errors = []
        for name, dist in [
            ("gender", self.gender_distribution),
            ("age", self.age_distribution),
            ("plan", self.plan_distribution),
        ]:
            total = sum(dist.values())
            if abs(total - 1.0) > 0.01:
                errors.append(f"{name} distribution sums to {total}, should be 1.0")
        return errors


@dataclass
class CohortProgress:
    """Track progress of cohort generation."""

    total: int
    completed: int = 0
    failed: int = 0

    @property
    def percent_complete(self) -> float:
        return (self.completed / self.total * 100) if self.total > 0 else 0

    @property
    def is_complete(self) -> bool:
        return self.completed + self.failed >= self.total


class CohortGenerator(Generic[T]):
    """Generate cohorts of entities with demographic constraints.

    Example:
        from membersim.core.member import Member

        constraints = CohortConstraints(
            gender_distribution={"M": 0.45, "F": 0.55},
            plan_distribution={"PPO": 0.6, "HMO": 0.4},
        )

        generator = CohortGenerator(
            entity_factory=create_member,
            constraints=constraints,
            seed=42,
        )

        members = list(generator.generate(count=1000))
    """

    def __init__(
        self,
        entity_factory: Callable[..., T],
        constraints: CohortConstraints | None = None,
        seed: int | None = None,
        progress_callback: Callable[[CohortProgress], None] | None = None,
    ):
        """Initialize cohort generator.

        Args:
            entity_factory: Function that creates entity given kwargs
            constraints: Demographic constraints to satisfy
            seed: Random seed for reproducibility
            progress_callback: Optional callback for progress updates
        """
        self.entity_factory = entity_factory
        self.constraints = constraints or CohortConstraints()
        self.seed_manager = SeedManager(seed or 42)
        self.progress_callback = progress_callback

        # Validate constraints
        errors = self.constraints.validate()
        if errors:
            raise ValueError(f"Invalid constraints: {errors}")

        # Create weighted choices for each distribution
        self._gender_choice = WeightedChoice(
            list(self.constraints.gender_distribution.items()),
            seed=self.seed_manager.get_seed("gender"),
        )
        self._plan_choice = WeightedChoice(
            list(self.constraints.plan_distribution.items()),
            seed=self.seed_manager.get_seed("plan"),
        )

    def _select_age_band(self, age_band: str) -> tuple[int, int]:
        """Convert age band string to (min, max) tuple."""
        if age_band == "0-17":
            return (0, 17)
        elif age_band == "18-34":
            return (18, 34)
        elif age_band == "35-54":
            return (35, 54)
        elif age_band == "55-64":
            return (55, 64)
        elif age_band == "65+":
            return (65, 90)
        else:
            raise ValueError(f"Unknown age band: {age_band}")

    def generate(self, count: int) -> Iterator[T]:
        """Generate cohort of entities satisfying constraints.

        Args:
            count: Number of entities to generate

        Yields:
            Generated entities.
        """
        progress = CohortProgress(total=count)

        # Pre-calculate target counts for each constraint category
        age_choice = WeightedChoice(
            list(self.constraints.age_distribution.items()),
            seed=self.seed_manager.get_seed("age"),
        )

        for i in range(count):
            try:
                # Select demographic attributes
                gender = self._gender_choice.select()
                plan_type = self._plan_choice.select()
                age_band = age_choice.select()
                min_age, max_age = self._select_age_band(age_band)

                # Get deterministic seed for this entity
                entity_seed = self.seed_manager.get_seed(f"entity_{i}")

                # Create entity with selected attributes
                entity = self.entity_factory(
                    seed=entity_seed,
                    gender=gender,
                    plan_type=plan_type,
                    min_age=min_age,
                    max_age=max_age,
                )

                progress.completed += 1
                yield entity

            except Exception as e:
                logger.warning(f"Failed to generate entity {i}: {e}")
                progress.failed += 1

            # Report progress
            if self.progress_callback and (i + 1) % 100 == 0:
                self.progress_callback(progress)

        # Final progress report
        if self.progress_callback:
            self.progress_callback(progress)
