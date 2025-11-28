# MemberSim Examples

Example scripts demonstrating MemberSim usage.

## Running Examples

Make sure MemberSim is installed:
```bash
cd MemberSim
pip install -e .
```

Then run any example:
```bash
python examples/basic_usage.py
python examples/family_enrollment.py
```

## Available Examples

### basic_usage.py
Demonstrates core functionality:
- Creating a member directly
- Exporting to JSON
- Generating X12 834 enrollment
- Creating and exporting claims (837P)
- Eligibility checking (270/271)
- Care gap generation
- Using MemberGenerator for batch creation

### family_enrollment.py
Demonstrates family enrollment:
- Creating subscriber and dependents
- Relationship codes (Self, Spouse, Child)
- Generating 834 for multiple members
- Exporting to EDI file