"""Deductible and OOP accumulator tracking."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class Accumulator(BaseModel):
    """Track deductible and OOP accumulations for a member."""

    member_id: str = Field(..., description="Member reference")
    plan_year: int = Field(..., description="Benefit year")

    # Deductible tracking
    deductible_applied: Decimal = Field(Decimal("0"), description="Amount applied to deductible")
    deductible_limit: Decimal = Field(..., description="Deductible limit for this member")

    # OOP tracking
    oop_applied: Decimal = Field(Decimal("0"), description="Amount applied to OOP max")
    oop_limit: Decimal = Field(..., description="OOP maximum for this member")

    last_updated: datetime = Field(default_factory=datetime.now)

    @property
    def deductible_remaining(self) -> Decimal:
        """Calculate remaining deductible."""
        return max(Decimal("0"), self.deductible_limit - self.deductible_applied)

    @property
    def deductible_met(self) -> bool:
        """Check if deductible has been met."""
        return self.deductible_applied >= self.deductible_limit

    @property
    def oop_remaining(self) -> Decimal:
        """Calculate remaining OOP."""
        return max(Decimal("0"), self.oop_limit - self.oop_applied)

    @property
    def oop_met(self) -> bool:
        """Check if OOP max has been reached."""
        return self.oop_applied >= self.oop_limit

    def apply_payment(self, deductible_amount: Decimal, oop_amount: Decimal) -> "Accumulator":
        """Apply a payment to accumulators, returning new accumulator state."""
        return Accumulator(
            member_id=self.member_id,
            plan_year=self.plan_year,
            deductible_applied=min(
                self.deductible_limit, self.deductible_applied + deductible_amount
            ),
            deductible_limit=self.deductible_limit,
            oop_applied=min(self.oop_limit, self.oop_applied + oop_amount),
            oop_limit=self.oop_limit,
            last_updated=datetime.now(),
        )
