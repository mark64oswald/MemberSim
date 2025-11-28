"""Basic MemberSim usage examples."""

from datetime import date
from decimal import Decimal

from healthsim.person import Address, Gender, PersonName

from membersim.core.member import Member, MemberGenerator
from membersim.core.plan import SAMPLE_PLANS
from membersim.claims.claim import Claim, ClaimLine
from membersim.formats import generate_834, generate_837p, generate_270, generate_271
from membersim.formats.export import to_json
from membersim.quality import generate_care_gaps


def create_sample_member() -> Member:
    """Create a sample member."""
    return Member(
        id="person-001",
        name=PersonName(given_name="Jane", family_name="Smith"),
        birth_date=date(1975, 6, 15),
        gender=Gender.FEMALE,
        address=Address(
            street_address="456 Oak Avenue",
            city="Boston",
            state="MA",
            postal_code="02101",
        ),
        member_id="MEM001",
        relationship_code="18",
        group_id="GRP001",
        coverage_start=date(2024, 1, 1),
        plan_code="PPO_GOLD",
    )


def create_sample_claim(member: Member) -> Claim:
    """Create a sample claim."""
    return Claim(
        claim_id="CLM001",
        member_id=member.member_id,
        subscriber_id=member.member_id,
        provider_npi="1234567890",
        service_date=date(2024, 3, 15),
        claim_type="PROFESSIONAL",
        place_of_service="11",
        principal_diagnosis="J06.9",
        claim_lines=[
            ClaimLine(
                line_number=1,
                procedure_code="99213",
                charge_amount=Decimal("150.00"),
                units=Decimal("1"),
                service_date=date(2024, 3, 15),
                diagnosis_pointers=[1],
            ),
        ],
    )


def main() -> None:
    """Run examples."""
    print("=== MemberSim Basic Usage ===\n")

    # 1. Create member
    print("1. Creating member...")
    member = create_sample_member()
    print(f"   Created: {member.member_id} - {member.name.full_name}")

    # 2. Export as JSON
    print("\n2. Member as JSON:")
    print(to_json(member))

    # 3. Generate 834 enrollment
    print("\n3. X12 834 Enrollment:")
    edi_834 = generate_834([member])
    print(edi_834[:500] + "...\n")

    # 4. Create claim
    print("4. Creating claim...")
    claim = create_sample_claim(member)
    print(f"   Created: {claim.claim_id} - ${claim.total_charge}")

    # 5. Generate 837P
    print("\n5. X12 837P Claim:")
    edi_837 = generate_837p([claim])
    print(edi_837[:500] + "...\n")

    # 6. Check eligibility
    print("6. Eligibility Check (270/271):")
    plan = SAMPLE_PLANS.get(member.plan_code)
    edi_270 = generate_270(member)
    edi_271 = generate_271(member, plan) if plan else None
    print(f"   270 generated: {len(edi_270)} chars")
    print(f"   271 generated: {len(edi_271) if edi_271 else 0} chars")

    # 7. Generate care gaps
    print("\n7. Care Gap Generation:")
    gaps = generate_care_gaps([member], gap_rate=0.4, seed=42)
    for gap in gaps:
        print(f"   {gap.measure_id}: {gap.gap_status}")

    # 8. Use MemberGenerator
    print("\n8. Using MemberGenerator:")
    generator = MemberGenerator(seed=42)
    generated_members = generator.generate_many(count=5)
    for m in generated_members:
        print(f"   {m.member_id}: {m.name.full_name}, Age {m.age}")

    print("\n=== Done ===")


if __name__ == "__main__":
    main()