"""Tests for generation framework."""

import pytest

from membersim.generation import (
    AgeDistribution,
    CohortConstraints,
    CohortGenerator,
    CohortProgress,
    NormalDistribution,
    SeedManager,
    UniformDistribution,
    WeightedChoice,
)

# ============================================================================
# WeightedChoice Tests
# ============================================================================


class TestWeightedChoice:
    """Tests for WeightedChoice."""

    def test_deterministic_with_seed(self) -> None:
        """Same seed should produce same sequence."""
        choice1 = WeightedChoice([("A", 0.5), ("B", 0.5)], seed=42)
        choice2 = WeightedChoice([("A", 0.5), ("B", 0.5)], seed=42)

        results1 = choice1.select_n(100)
        results2 = choice2.select_n(100)

        assert results1 == results2

    def test_respects_weights(self) -> None:
        """Heavily weighted option should be selected more often."""
        choice = WeightedChoice([("A", 0.99), ("B", 0.01)], seed=42)
        results = choice.select_n(1000)

        a_count = results.count("A")
        assert a_count > 900  # Should be ~99%

    def test_empty_choices_raises(self) -> None:
        """Empty choices should raise ValueError."""
        with pytest.raises(ValueError, match="choices cannot be empty"):
            WeightedChoice([])

    def test_negative_weight_raises(self) -> None:
        """Negative weights should raise ValueError."""
        with pytest.raises(ValueError, match="weights cannot be negative"):
            WeightedChoice([("A", -0.5), ("B", 0.5)])

    def test_zero_total_weight_raises(self) -> None:
        """Zero total weight should raise ValueError."""
        with pytest.raises(ValueError, match="total weight cannot be zero"):
            WeightedChoice([("A", 0), ("B", 0)])

    def test_select_returns_value(self) -> None:
        """Select should return one of the values."""
        choice = WeightedChoice([("X", 0.5), ("Y", 0.5)], seed=42)
        result = choice.select()
        assert result in ["X", "Y"]

    def test_select_n_returns_list(self) -> None:
        """Select_n should return list of correct length."""
        choice = WeightedChoice([("A", 1.0)], seed=42)
        results = choice.select_n(5)
        assert len(results) == 5
        assert all(r == "A" for r in results)


# ============================================================================
# UniformDistribution Tests
# ============================================================================


class TestUniformDistribution:
    """Tests for UniformDistribution."""

    def test_sample_within_bounds(self) -> None:
        """Samples should be within min/max bounds."""
        dist = UniformDistribution(min_val=10.0, max_val=20.0, seed=42)
        for _ in range(100):
            value = dist.sample()
            assert 10.0 <= value <= 20.0

    def test_sample_int_within_bounds(self) -> None:
        """Integer samples should be within bounds."""
        dist = UniformDistribution(min_val=1.0, max_val=10.0, seed=42)
        for _ in range(100):
            value = dist.sample_int()
            assert 1 <= value <= 10
            assert isinstance(value, int)

    def test_deterministic_with_seed(self) -> None:
        """Same seed should produce same sequence."""
        dist1 = UniformDistribution(0.0, 100.0, seed=42)
        dist2 = UniformDistribution(0.0, 100.0, seed=42)

        values1 = [dist1.sample() for _ in range(10)]
        values2 = [dist2.sample() for _ in range(10)]

        assert values1 == values2


# ============================================================================
# NormalDistribution Tests
# ============================================================================


class TestNormalDistribution:
    """Tests for NormalDistribution."""

    def test_sample_respects_bounds(self) -> None:
        """Bounded samples should respect min/max."""
        dist = NormalDistribution(mean=50.0, std_dev=10.0, min_val=40.0, max_val=60.0, seed=42)
        for _ in range(100):
            value = dist.sample()
            assert 40.0 <= value <= 60.0

    def test_unbounded_samples(self) -> None:
        """Unbounded distribution should work."""
        dist = NormalDistribution(mean=0.0, std_dev=1.0, seed=42)
        values = [dist.sample() for _ in range(100)]
        # Should have some variation
        assert max(values) != min(values)

    def test_deterministic_with_seed(self) -> None:
        """Same seed should produce same sequence."""
        dist1 = NormalDistribution(50.0, 10.0, seed=42)
        dist2 = NormalDistribution(50.0, 10.0, seed=42)

        values1 = [dist1.sample() for _ in range(10)]
        values2 = [dist2.sample() for _ in range(10)]

        assert values1 == values2


# ============================================================================
# AgeDistribution Tests
# ============================================================================


class TestAgeDistribution:
    """Tests for AgeDistribution."""

    def test_sample_within_default_bounds(self) -> None:
        """Ages should be within 0-100 by default."""
        dist = AgeDistribution(seed=42)
        for _ in range(100):
            age = dist.sample()
            assert 0 <= age <= 100

    def test_sample_respects_custom_bounds(self) -> None:
        """Custom age bounds should be respected."""
        dist = AgeDistribution(min_age=18, max_age=65, seed=42)
        for _ in range(100):
            age = dist.sample()
            assert 18 <= age <= 65

    def test_deterministic_with_seed(self) -> None:
        """Same seed should produce same ages."""
        dist1 = AgeDistribution(seed=42)
        dist2 = AgeDistribution(seed=42)

        ages1 = [dist1.sample() for _ in range(10)]
        ages2 = [dist2.sample() for _ in range(10)]

        assert ages1 == ages2


# ============================================================================
# SeedManager Tests
# ============================================================================


class TestSeedManager:
    """Tests for SeedManager."""

    def test_deterministic_seeds(self) -> None:
        """Same master seed should produce same child seeds."""
        mgr1 = SeedManager(master_seed=42)
        mgr2 = SeedManager(master_seed=42)

        assert mgr1.get_seed("test") == mgr2.get_seed("test")
        assert mgr1.get_seed("member_0") == mgr2.get_seed("member_0")

    def test_different_keys_different_seeds(self) -> None:
        """Different keys should produce different seeds."""
        mgr = SeedManager(master_seed=42)

        seeds = [mgr.get_seed(f"key_{i}") for i in range(100)]
        assert len(set(seeds)) == 100  # All unique

    def test_child_manager(self) -> None:
        """Child managers should be deterministic."""
        mgr1 = SeedManager(master_seed=42)
        mgr2 = SeedManager(master_seed=42)

        child1 = mgr1.child_manager("claims")
        child2 = mgr2.child_manager("claims")

        assert child1.get_seed("claim_0") == child2.get_seed("claim_0")

    def test_get_seeds_iterator(self) -> None:
        """get_seeds should return deterministic sequence."""
        mgr1 = SeedManager(master_seed=42)
        mgr2 = SeedManager(master_seed=42)

        seeds1 = list(mgr1.get_seeds("member", 10))
        seeds2 = list(mgr2.get_seeds("member", 10))

        assert seeds1 == seeds2
        assert len(seeds1) == 10

    def test_reset_clears_cache(self) -> None:
        """Reset should clear the seed cache."""
        mgr = SeedManager(master_seed=42)
        _ = mgr.get_seed("test")
        assert len(mgr._cache) == 1

        mgr.reset()
        assert len(mgr._cache) == 0


# ============================================================================
# CohortConstraints Tests
# ============================================================================


class TestCohortConstraints:
    """Tests for CohortConstraints."""

    def test_default_constraints_valid(self) -> None:
        """Default constraints should be valid."""
        constraints = CohortConstraints()
        errors = constraints.validate()
        assert errors == []

    def test_invalid_gender_distribution(self) -> None:
        """Invalid gender distribution should report error."""
        constraints = CohortConstraints(
            gender_distribution={"M": 0.3, "F": 0.3}  # Sums to 0.6
        )
        errors = constraints.validate()
        assert len(errors) == 1
        assert "gender" in errors[0]

    def test_invalid_age_distribution(self) -> None:
        """Invalid age distribution should report error."""
        constraints = CohortConstraints(
            age_distribution={"0-17": 0.5}  # Sums to 0.5
        )
        errors = constraints.validate()
        assert len(errors) == 1
        assert "age" in errors[0]


# ============================================================================
# CohortProgress Tests
# ============================================================================


class TestCohortProgress:
    """Tests for CohortProgress."""

    def test_percent_complete(self) -> None:
        """Percent complete should be calculated correctly."""
        progress = CohortProgress(total=100, completed=50)
        assert progress.percent_complete == 50.0

    def test_percent_complete_zero_total(self) -> None:
        """Percent complete with zero total should be 0."""
        progress = CohortProgress(total=0, completed=0)
        assert progress.percent_complete == 0

    def test_is_complete(self) -> None:
        """is_complete should check completed + failed >= total."""
        progress = CohortProgress(total=10, completed=8, failed=2)
        assert progress.is_complete

        progress2 = CohortProgress(total=10, completed=5, failed=0)
        assert not progress2.is_complete


# ============================================================================
# CohortGenerator Tests
# ============================================================================


class TestCohortGenerator:
    """Tests for CohortGenerator."""

    def test_generates_correct_count(self) -> None:
        """Should generate requested number of entities."""

        def simple_factory(**kwargs):
            return {"seed": kwargs.get("seed")}

        generator = CohortGenerator(
            entity_factory=simple_factory,
            seed=42,
        )

        entities = list(generator.generate(count=100))
        assert len(entities) == 100

    def test_reproducible_generation(self) -> None:
        """Same seed should produce same cohort."""

        def simple_factory(**kwargs):
            return kwargs

        gen1 = CohortGenerator(entity_factory=simple_factory, seed=42)
        gen2 = CohortGenerator(entity_factory=simple_factory, seed=42)

        cohort1 = list(gen1.generate(count=50))
        cohort2 = list(gen2.generate(count=50))

        assert cohort1 == cohort2

    def test_constraint_validation(self) -> None:
        """Invalid constraints should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid constraints"):
            CohortGenerator(
                entity_factory=lambda **k: k,
                constraints=CohortConstraints(
                    gender_distribution={"M": 0.3, "F": 0.3}  # Sums to 0.6
                ),
            )

    def test_passes_demographic_attributes(self) -> None:
        """Factory should receive demographic attributes."""
        received_kwargs = []

        def capture_factory(**kwargs):
            received_kwargs.append(kwargs)
            return kwargs

        generator = CohortGenerator(
            entity_factory=capture_factory,
            seed=42,
        )

        list(generator.generate(count=10))

        # Check all entities received expected kwargs
        for kwargs in received_kwargs:
            assert "seed" in kwargs
            assert "gender" in kwargs
            assert "plan_type" in kwargs
            assert "min_age" in kwargs
            assert "max_age" in kwargs

    def test_progress_callback(self) -> None:
        """Progress callback should be called."""
        progress_reports = []

        def track_progress(progress: CohortProgress):
            progress_reports.append(progress.completed)

        generator = CohortGenerator(
            entity_factory=lambda **k: k,
            seed=42,
            progress_callback=track_progress,
        )

        list(generator.generate(count=250))

        # Should have progress reports at 100, 200, and final
        assert len(progress_reports) >= 2
