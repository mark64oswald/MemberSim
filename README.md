# MemberSim

Synthetic health plan member data generation for safe testing of payer systems.

## Overview

MemberSim generates realistic but fictional health plan data including:
- Member enrollment records (X12 834)
- Healthcare claims (X12 837P/I)
- Payment/remittance advice (X12 835)
- Prior authorization (X12 278)
- Eligibility verification (X12 270/271)
- HEDIS quality measures and care gaps
- Provider networks and fee schedules

## Installation

```bash
pip install membersim
```

## Quick Start

```python
from membersim import MemberGenerator

# Generate members with claims
generator = MemberGenerator(seed=42)
members = generator.generate_members(count=100, plan_type="PPO")
claims = generator.generate_claims(members, per_member=5)

# Export to X12
from membersim.formats.x12 import EDI834Generator
edi = EDI834Generator()
edi.export(members, "enrollment.834")
```

## Part of HealthSim Family

- **healthsim-core**: Shared foundation library
- **PatientSim**: Clinical/EMR synthetic data
- **MemberSim**: Payer/claims synthetic data (this project)

## License

MIT License
