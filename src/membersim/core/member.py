"""Health plan member model."""

from datetime import date
from typing import Optional

from healthsim.person import Person
from pydantic import Field


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
