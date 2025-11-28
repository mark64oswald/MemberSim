# MemberSim

Synthetic health plan member data generator for payer/TPA testing and development.

## Overview

MemberSim generates realistic synthetic data for:
- **Member enrollment** (demographics, coverage, dependents)
- **Claims processing** (professional, institutional, payments)
- **Eligibility verification** (real-time and batch)
- **Quality measures** (HEDIS care gaps)
- **Value-based care** (attribution, capitation)

Built on [healthsim-core](https://github.com/mark64oswald/healthsim-core) for consistent demographics across the HealthSim platform.

## Installation

```bash
pip install membersim
```

Or from source:
```bash
git clone https://github.com/mark64oswald/MemberSim.git
cd MemberSim
pip install -e .
```

## Quick Start

### Python API

```python
from datetime import date
from membersim.core.member import Member, MemberGenerator
from membersim.core.plan import SAMPLE_PLANS
from membersim.formats import generate_834, generate_837p
from membersim.quality import generate_care_gaps
from healthsim.person import Address, Gender, PersonName

# Generate members with the MemberGenerator
generator = MemberGenerator(seed=42)
members = generator.generate_many(count=10)

# Or create a member directly
member = Member(
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
    group_id="GRP001",
    coverage_start=date(2024, 1, 1),
    plan_code="PPO_GOLD",
)

# Generate X12 834 enrollment
edi_834 = generate_834([member])

# Generate care gaps
gaps = generate_care_gaps([member], gap_rate=0.3)
```

### MCP Server (Claude.ai)

MemberSim includes an MCP server for conversational data generation:

```json
{
  "mcpServers": {
    "membersim": {
      "command": "python",
      "args": ["-m", "membersim.mcp.server"]
    }
  }
}
```

Then in Claude:
> "Create a 45-year-old female member enrolled in PPO Gold starting January 2024"

## Output Formats

| Format | Use Case |
|--------|----------|
| X12 834 | Enrollment files |
| X12 837P/I | Professional/institutional claims |
| X12 835 | Remittance advice |
| X12 270/271 | Eligibility inquiry/response |
| X12 278 | Prior authorization |
| FHIR R4 | Coverage, Patient resources |
| JSON | API integration |
| CSV | Reporting, analytics |

## Package Structure

```
membersim/
├── core/           # Member, Subscriber, Plan, Provider, Accumulator
├── claims/         # Claim, ClaimLine, Payment
├── quality/        # HEDIS measures, care gap generation
├── authorization/  # Prior auth models
├── network/        # Provider contracts, fee schedules
├── vbc/            # Attribution, capitation
├── formats/        # X12, FHIR, JSON, CSV exporters
├── generation/     # Reproducible generation framework
├── scenarios/      # Timeline-based scenario engine
├── mcp/            # MCP server for Claude.ai
└── skills/         # Claude.ai Skills files
```

## Key Features

### X12 EDI Transactions
Generate compliant HIPAA X12 transactions:
```python
from membersim.formats import generate_834, generate_837p, generate_270, generate_271

# Enrollment
edi_834 = generate_834(members)

# Claims
edi_837 = generate_837p(claims)

# Eligibility
edi_270 = generate_270(member)
edi_271 = generate_271(member, plan)
```

### HEDIS Quality Measures
Generate care gaps for population health:
```python
from membersim.quality import generate_care_gaps, HEDIS_MEASURES

# Generate care gaps with 30% open rate
gaps = generate_care_gaps(members, gap_rate=0.3, seed=42)

# Access measure definitions
for measure_id, measure in HEDIS_MEASURES.items():
    print(f"{measure_id}: {measure.name}")
```

### Value-Based Care
Model provider attribution and capitation:
```python
from membersim.vbc import Attribution, calculate_capitation_payment
from decimal import Decimal

# Attribution
attribution = Attribution(
    attribution_id="ATT001",
    member_id="MEM001",
    provider_npi="1234567890",
    effective_date=date(2024, 1, 1),
    performance_year=2024,
)

# Capitation calculation
payment = calculate_capitation_payment(
    provider_npi="1234567890",
    contract_id="CTR001",
    payment_period="2024-03",
    members=[{"member_id": "MEM001", "age": 45, "risk_score": Decimal("1.0")}],
    rates={"ADULT": adult_rate},
)
```

### Scenario Engine
Create realistic member journeys:
```python
from membersim.scenarios import ScenarioEngine, SCENARIO_LIBRARY

# Get a predefined scenario
diabetic_scenario = SCENARIO_LIBRARY.get("diabetic_member")

# Create timeline
engine = ScenarioEngine()
timeline = engine.create_timeline(member, diabetic_scenario, start_date)

# Execute events
for event in timeline.get_pending_events(end_date):
    result = engine.execute_event(event)
```

## Requirements

- Python 3.11+
- healthsim-core >= 0.1.0
- pydantic >= 2.0
- faker >= 20.0

## License

MIT License - see LICENSE file.

## Related Projects

- [healthsim-core](https://github.com/mark64oswald/healthsim-core) - Shared foundation library
- [PatientSim](https://github.com/mark64oswald/PatientSim) - Clinical/EMR data generation