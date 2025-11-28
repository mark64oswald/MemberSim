"""Health plan member model."""

from __future__ import annotations

import random
from datetime import date, timedelta
from typing import Optional

from faker import Faker
from healthsim.person import Address, Gender, Person, PersonName
from pydantic import Field

from membersim.generation import SeedManager, WeightedChoice


class Member(Person):
    """Health plan member with demographics and coverage relationship.

    Extends healthsim-core Person with health plan specific attributes.
    """

    model_config = {"frozen": True}

    member_id: str = Field(..., description="Unique member identifier")
    subscriber_id: Optional[str] = Field(
        None, description="For dependents, reference to subscriber"
    )
    relationship_code: str = Field("18", description="18=Self, 01=Spouse, 19=Child")
    group_id: str = Field(..., description="Employer/group identifier")
    coverage_start: date = Field(..., description="Coverage effective date")
    coverage_end: Optional[date] = Field(
        None, description="Coverage termination date (None if active)"
    )
    plan_code: str = Field(..., description="Benefit plan identifier")
    pcp_npi: Optional[str] = Field(None, description="Assigned PCP NPI (for HMO plans)")

    @property
    def is_subscriber(self) -> bool:
        """Check if this member is the subscriber (self)."""
        return self.relationship_code == "18"

    @property
    def is_active(self) -> bool:
        """Check if coverage is currently active."""
        today = date.today()
        if self.coverage_end is None:
            return self.coverage_start <= today
        return self.coverage_start <= today <= self.coverage_end


class MemberGenerator:
    """Generate synthetic members with scenario support.

    Example:
        generator = MemberGenerator(seed=42)
        member = generator.generate_one()

        # Or with constraints
        member = generator.generate_one(gender="F", min_age=50, max_age=74)
    """

    def __init__(self, seed: int | None = None):
        """Initialize member generator.

        Args:
            seed: Random seed for reproducibility.
        """
        self.seed_manager = SeedManager(seed or 42)
        self._faker = Faker()
        self._faker.seed_instance(seed or 42)
        self._rng = random.Random(seed)
        self._counter = 0

        # Distribution choices
        self._gender = WeightedChoice(
            [("M", 0.49), ("F", 0.51)],
            seed=self.seed_manager.get_seed("gender"),
        )
        self._plan_type = WeightedChoice(
            [("HMO", 0.35), ("PPO", 0.40), ("HDHP", 0.25)],
            seed=self.seed_manager.get_seed("plan"),
        )
        self._relationship = WeightedChoice(
            [("18", 0.60), ("01", 0.25), ("19", 0.15)],  # Self, Spouse, Child
            seed=self.seed_manager.get_seed("relationship"),
        )

    def _generate_birth_date(self, min_age: int = 0, max_age: int = 90) -> date:
        """Generate a birth date within age constraints."""
        today = date.today()
        age = self._rng.randint(min_age, max_age)
        birth_year = today.year - age
        birth_month = self._rng.randint(1, 12)
        birth_day = self._rng.randint(1, 28)  # Safe for all months
        return date(birth_year, birth_month, birth_day)

    def _generate_coverage_start(self) -> date:
        """Generate a coverage start date."""
        today = date.today()
        # Start within last 3 years
        days_ago = self._rng.randint(0, 1095)
        return today - timedelta(days=days_ago)

    def generate_one(
        self,
        seed: int | None = None,
        gender: str | None = None,
        plan_type: str | None = None,
        min_age: int = 0,
        max_age: int = 90,
        **overrides,
    ) -> Member:
        """Generate a single member.

        Args:
            seed: Optional seed for this specific member
            gender: Gender code ("M" or "F")
            plan_type: Plan type ("HMO", "PPO", "HDHP")
            min_age: Minimum age
            max_age: Maximum age
            **overrides: Override any generated attributes

        Returns:
            Generated Member instance.
        """
        self._counter += 1

        # Use provided seed or generate deterministic one
        if seed is not None:
            member_rng = random.Random(seed)
        else:
            member_seed = self.seed_manager.get_seed(f"member_{self._counter}")
            member_rng = random.Random(member_seed)

        # Select or use provided attributes
        selected_gender = gender or self._gender.select()
        selected_plan = plan_type or self._plan_type.select()
        relationship = overrides.get("relationship_code") or self._relationship.select()

        # Generate name based on gender
        if selected_gender == "M":
            first_name = self._faker.first_name_male()
        else:
            first_name = self._faker.first_name_female()
        last_name = self._faker.last_name()

        # Generate address
        address = Address(
            street=self._faker.street_address(),
            city=self._faker.city(),
            state=self._faker.state_abbr(),
            zip_code=self._faker.zipcode(),
        )

        # Generate dates
        birth_date = self._generate_birth_date(min_age, max_age)
        coverage_start = self._generate_coverage_start()

        # Generate IDs
        member_id = overrides.get("member_id") or f"MEM{self._counter:06d}"
        group_id = overrides.get("group_id") or f"GRP{member_rng.randint(1, 100):03d}"

        return Member(
            id=f"person-{self._counter:06d}",
            name=PersonName(given_name=first_name, family_name=last_name),
            birth_date=birth_date,
            gender=Gender.MALE if selected_gender == "M" else Gender.FEMALE,
            address=address,
            member_id=member_id,
            relationship_code=relationship,
            group_id=group_id,
            coverage_start=coverage_start,
            plan_code=selected_plan,
        )

    def generate_many(self, count: int, **kwargs) -> list[Member]:
        """Generate multiple members.

        Args:
            count: Number of members to generate
            **kwargs: Passed to generate_one

        Returns:
            List of generated members.
        """
        return [self.generate_one(**kwargs) for _ in range(count)]
