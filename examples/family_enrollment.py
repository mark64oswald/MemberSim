"""Family enrollment example with subscriber and dependents."""

from datetime import date

from healthsim.person import Address, Gender, PersonName

from membersim.core.member import Member
from membersim.formats import generate_834


def create_family() -> tuple[Member, list[Member]]:
    """Create a family with subscriber and dependents."""

    # Shared address
    address = Address(
        street_address="789 Family Lane",
        city="Chicago",
        state="IL",
        postal_code="60601",
    )

    # Subscriber (Employee)
    subscriber = Member(
        id="person-sub-001",
        name=PersonName(given_name="John", family_name="Doe"),
        birth_date=date(1985, 3, 20),
        gender=Gender.MALE,
        address=address,
        member_id="SUB001",
        subscriber_id="SUB001",
        relationship_code="18",  # Self
        group_id="ACME_CORP",
        coverage_start=date(2024, 1, 1),
        plan_code="HMO_STANDARD",
    )

    # Spouse
    spouse = Member(
        id="person-dep-001",
        name=PersonName(given_name="Jane", family_name="Doe"),
        birth_date=date(1987, 7, 15),
        gender=Gender.FEMALE,
        address=address,
        member_id="MEM001A",
        subscriber_id="SUB001",
        relationship_code="01",  # Spouse
        group_id="ACME_CORP",
        coverage_start=date(2024, 1, 1),
        plan_code="HMO_STANDARD",
    )

    # Child 1
    child1 = Member(
        id="person-dep-002",
        name=PersonName(given_name="Tommy", family_name="Doe"),
        birth_date=date(2015, 5, 10),
        gender=Gender.MALE,
        address=address,
        member_id="MEM001B",
        subscriber_id="SUB001",
        relationship_code="19",  # Child
        group_id="ACME_CORP",
        coverage_start=date(2024, 1, 1),
        plan_code="HMO_STANDARD",
    )

    # Child 2
    child2 = Member(
        id="person-dep-003",
        name=PersonName(given_name="Sally", family_name="Doe"),
        birth_date=date(2018, 11, 25),
        gender=Gender.FEMALE,
        address=address,
        member_id="MEM001C",
        subscriber_id="SUB001",
        relationship_code="19",  # Child
        group_id="ACME_CORP",
        coverage_start=date(2024, 1, 1),
        plan_code="HMO_STANDARD",
    )

    return subscriber, [spouse, child1, child2]


def main() -> None:
    """Generate family enrollment."""
    print("=== Family Enrollment Example ===\n")

    subscriber, dependents = create_family()

    print(f"Subscriber: {subscriber.name.full_name}")
    print(f"Plan: {subscriber.plan_code}")
    print(f"Group: {subscriber.group_id}")
    print("\nDependents:")
    for dep in dependents:
        rel = "Spouse" if dep.relationship_code == "01" else "Child"
        print(f"  - {dep.name.full_name} ({rel}, age {dep.age})")

    # Generate 834 for all members
    all_members = [subscriber, *dependents]

    print(f"\n834 Enrollment ({len(all_members)} members):")
    edi_834 = generate_834(all_members)

    # Count INS segments (one per member)
    ins_count = edi_834.count("INS*")
    print(f"  INS segments: {ins_count}")
    print(f"  Total size: {len(edi_834)} characters")

    # Save to file
    output_file = "family_834.edi"
    with open(output_file, "w") as f:
        f.write(edi_834)
    print(f"  Saved to: {output_file}")


if __name__ == "__main__":
    main()