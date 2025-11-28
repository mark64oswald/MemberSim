# MemberSim

**Generate realistic synthetic health plan members and claims through natural conversation with Claude.**

MemberSim creates not just member data, but complete **payer scenarios** with realistic event timelines — from enrollment through claims processing, care gap identification, and value-based care attribution.

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](CHANGELOG.md)

> **v0.2.0**: MemberSim now uses [healthsim-core](https://github.com/mark64oswald/healthsim-core) as its foundation, providing improved seed reproducibility, standardized validation, and a shared architecture with PatientSim.

---

## What You Can Do

Instead of wrestling with complex X12 EDI specifications or building enrollment files from scratch, simply tell Claude what you need:

> **You:** "Generate 50 members enrolled in our PPO Gold plan with a mix of ages and include some with diabetes care gaps"
>
> **Claude:** "I'll create 50 PPO Gold members with realistic demographics. I'll include 15 members with open diabetes care gaps (HbA1c testing, eye exams, nephropathy screening) distributed across ages 40-75..."

> **You:** "I need to test our claims adjudication — create a member with a series of professional claims for an office visit, labs, and a specialist referral"
>
> **Claude:** "I'll generate a member with a claim timeline: Day 1 office visit ($150), Day 1 lab panel ($85), Day 7 specialist consultation ($275). Each claim will have proper CPT/HCPCS codes, place of service, and realistic allowed amounts..."

> **You:** "Create an 834 enrollment file for 100 new members joining effective January 1st"
>
> **Claude:** "I'll generate a HIPAA-compliant X12 834 file with 100 member enrollments, including subscriber and dependent loops, coverage start dates, and proper segment terminators..."

> **You:** "Generate test data for our HEDIS reporting — I need members with both open and closed gaps for BCS and COL measures"
>
> **Claude:** "I'll create members targeting breast cancer screening (BCS) and colorectal cancer screening (COL) measures. 60% will have open gaps, 40% closed with evidence dates within the measurement year..."

**No code. No X12 expertise required. Just describe the payer data you need.**

---

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/mark64oswald/MemberSim.git
cd MemberSim

# Install dependencies
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### 2. Set Up Claude Project

MemberSim works through **Claude Projects** — give Claude the domain knowledge to generate accurate payer data.

**Quick Setup:**

1. **Open Claude** (claude.ai or Claude Desktop)

2. **Create a New Project**:
   - Click "Projects" → "Create Project"
   - Name: "MemberSim"
   - Description: "Synthetic payer data generation"

3. **Add Project Knowledge**:
   - Add `.claude/project-instructions.md` to the project
   - Optionally add scenario skills:
     - `skills/scenarios/enrollment-lifecycle.md`
     - `skills/scenarios/claims-processing.md`
     - `skills/scenarios/hedis-gaps.md`

4. **Start a Conversation**:
   ```
   Generate 10 members enrolled in PPO plans with January 2024 effective dates
   ```

### 3. Your First Member

Start with these example requests:

**Single Member**:
```
Generate a 45-year-old female member enrolled in HMO Premier with 2 dependents
```

**Member Cohorts**:
```
Create 100 members with a realistic age distribution, 60% PPO and 40% HMO
```

**With Claims**:
```
Generate a member with 6 months of claims history including PCP visits, labs, and a hospital stay
```

**X12 Export**:
```
Export these members as an 834 enrollment transaction
```

---

## What MemberSim Generates

### Realistic Member Demographics

- **Names & Identifiers**: Member IDs, group IDs, SSNs, addresses (using Faker for HIPAA-safe synthetic data)
- **Coverage Details**: Plan codes, coverage tiers (employee, employee+spouse, family)
- **Relationships**: Subscribers with dependents, proper relationship codes
- **Diverse Populations**: Configurable age, gender, and geographic distributions

### Plan & Coverage Data

- **Plan Types**: HMO, PPO, EPO, POS, HDHP configurations
- **Benefits**: Deductibles, copays, coinsurance, out-of-pocket maximums
- **Coverage Periods**: Effective dates, termination handling, COBRA
- **Accumulators**: Year-to-date tracking of deductibles and OOP

### Claims & Payments

- **Professional Claims (837P)**: Office visits, specialist consultations, labs
- **Institutional Claims (837I)**: Hospital stays, outpatient procedures
- **Claim Lines**: CPT/HCPCS codes, modifiers, place of service
- **Adjudication**: Allowed amounts, member responsibility, EOB details
- **Remittance (835)**: Payment information, adjustment reason codes

### Quality Measures

- **HEDIS Measures**: Preventive care, chronic condition management
- **Care Gaps**: Open gaps with due dates, closed gaps with evidence
- **Star Ratings**: Quality scores and performance metrics
- **Population Health**: Risk scores, chronic condition flags

### Prior Authorization

- **Auth Requests**: Service type, requesting provider
- **Auth Decisions**: Approved, denied, pended with reasons
- **Auth Tracking**: Validity periods, units authorized

### Value-Based Care

- **Provider Attribution**: Member-PCP relationships
- **Capitation**: PMPM calculations, risk-adjusted payments
- **Performance**: Quality bonuses, shared savings

---

## Output Formats

MemberSim exports to all major payer data formats:

### X12 834 — Benefit Enrollment
**For:** Eligibility systems, enrollment processing

```
Generate an 834 enrollment file for new hires effective March 1st
```

**Loops Generated:**
- 1000A/B: Sponsor and payer identification
- 2000: Member level data
- 2100A-C: Member name, address, demographics
- 2300: Coverage information
- 2310: Provider information (if applicable)

### X12 837P/I — Healthcare Claims
**For:** Claims processing systems, clearinghouses

```
Export professional claims as 837P transactions
```

**Content:**
- Billing and rendering providers
- Subscriber and patient information
- Claim and service line details
- Diagnosis codes (ICD-10)
- Procedure codes (CPT/HCPCS)

### X12 835 — Remittance Advice
**For:** Payment reconciliation, ERA processing

**Content:**
- Payment information
- Claim-level adjustments
- Service line details
- Reason codes

### X12 270/271 — Eligibility
**For:** Real-time eligibility verification

```
Generate 270 eligibility inquiry and 271 response pair
```

### X12 278 — Prior Authorization
**For:** Utilization management systems

### FHIR R4
**For:** Modern healthcare APIs, interoperability

**Resources Generated:**
- Patient (member demographics)
- Coverage (plan enrollment)
- Claim (claims data)
- ExplanationOfBenefit (adjudication)

### JSON/CSV
**For:** Analytics, reporting, data warehouses

---

## Use Cases

### Claims System Testing

Generate realistic test data for claims processing systems.

**What you can test:**
- Claims adjudication rules
- Benefit configuration
- COB (coordination of benefits)
- Duplicate claim detection
- Timely filing limits

**Example:**
```python
from membersim.claims import generate_claim_batch

# Generate claims with various scenarios
claims = generate_claim_batch(
    members=members,
    claim_types=["professional", "institutional"],
    date_range=(date(2024, 1, 1), date(2024, 6, 30)),
    include_adjustments=True,
    seed=42
)
```

### Enrollment System Testing

Test enrollment processing with X12 834 transactions.

**What you can test:**
- New enrollment processing
- Termination handling
- Plan changes and transfers
- Dependent adds/removes
- COBRA enrollment

### Quality Measure Development

Validate HEDIS calculations and care gap identification.

**What you can test:**
- Measure specification logic
- Gap closure algorithms
- Evidence collection
- Exclusion handling
- Supplemental data integration

### Analytics & Reporting

Generate synthetic populations for analytics development.

**Applications:**
- Population health dashboards
- Risk stratification models
- Utilization analytics
- Cost trending
- Provider performance

---

## For Developers

**Looking to automate MemberSim or extend it with custom scenarios?**

MemberSim provides a Python API for programmatic access:

```python
from datetime import date
from membersim.core.member import Member, MemberGenerator
from membersim.generation import MemberCohortGenerator, MemberCohortConstraints
from membersim.scenarios import ScenarioEngine, MemberTimeline
from membersim.formats import generate_834, generate_837p
from membersim.quality import generate_care_gaps
from healthsim.person import Address, Gender, PersonName

# Create generator with reproducible seed
gen = MemberGenerator(seed=42)

# Generate single member
member = gen.generate_one(
    plan_type="PPO",
    min_age=30,
    max_age=50
)
print(f"{member.name.given_name} {member.name.family_name}, Plan: {member.plan_code}")

# Generate cohort with constraints
cohort_gen = MemberCohortGenerator(seed=42)
constraints = MemberCohortConstraints(
    count=100,
    gender_distribution={"M": 0.48, "F": 0.52},
    age_distribution={
        "0-17": 0.15,
        "18-34": 0.25,
        "35-54": 0.35,
        "55-64": 0.15,
        "65+": 0.10
    },
    plan_distribution={"PPO": 0.6, "HMO": 0.4}
)
members = cohort_gen.generate(constraints)

# Export to X12 834
edi_834 = generate_834(members)
print(edi_834[:500])

# Generate care gaps
gaps = generate_care_gaps(members, gap_rate=0.3, seed=42)
for gap in gaps[:5]:
    print(f"{gap.member_id}: {gap.measure_id} - {gap.status}")
```

### Scenario Engine

Create realistic member journeys with timeline-based scenarios:

```python
from membersim.scenarios import ScenarioEngine, ScenarioLibrary, BUILTIN_SCENARIOS

# Get a predefined scenario
library = ScenarioLibrary(BUILTIN_SCENARIOS)
diabetic_scenario = library.get("diabetic_member")

# Create and execute timeline
engine = ScenarioEngine(seed=42)
timeline = engine.create_timeline(
    member=member,
    scenario=diabetic_scenario,
    start_date=date(2024, 1, 1)
)

# Process events
for event in timeline.get_pending_events():
    result = engine.execute_event(
        timeline=timeline,
        event=event,
        member=member,
        context={}
    )
    print(f"Executed: {event.event_name}")
```

### Value-Based Care

Model provider attribution and capitation:

```python
from membersim.vbc import Attribution, CapitationRate, calculate_capitation_payment
from decimal import Decimal

# Create attribution
attribution = Attribution(
    attribution_id="ATT001",
    member_id=member.member_id,
    provider_npi="1234567890",
    effective_date=date(2024, 1, 1),
    performance_year=2024,
)

# Calculate capitation payment
rate = CapitationRate(
    rate_id="RATE001",
    contract_id="CTR001",
    effective_date=date(2024, 1, 1),
    base_pmpm=Decimal("45.00"),
    age_band="ADULT",
    risk_adjustment=True
)

payment = calculate_capitation_payment(
    members=[member],
    rate=rate,
    payment_period="2024-03"
)
print(f"Payment: ${payment.total_amount}")
```

**Developer Resources:**
- **[API Reference](docs/developer-guide/api-reference.md)** — Complete Python API
- **[Extending MemberSim](docs/developer-guide/extending.md)** — Add custom scenarios
- **[X12 Deep Dive](docs/reference/x12-formats.md)** — EDI format details

---

## Available Scenarios

MemberSim includes pre-built scenario templates:

### Enrollment Lifecycle
- **New Enrollment**: Member joins plan
- **Open Enrollment**: Annual plan changes
- **Qualifying Life Event**: Mid-year changes
- **Termination**: Coverage ending
- **COBRA**: Continuation coverage

### Claims Processing
- **Routine Care**: PCP visits, preventive services
- **Specialty Care**: Referrals, specialist visits
- **Hospital Stay**: Inpatient admission
- **Emergency**: ED visits
- **Pharmacy**: Prescription claims

### Quality Measures
- **Diabetes Care**: HbA1c, eye exam, nephropathy
- **Preventive Screening**: BCS, COL, cervical cancer
- **Medication Adherence**: Statin, diabetes, RAS antagonist
- **Behavioral Health**: Depression screening, follow-up

---

## Project Structure

```
membersim/
├── .claude/                    # Claude Project configuration
│   ├── project-instructions.md # Claude's role definition
│   └── mcp-config.json         # MCP server configuration
├── src/membersim/              # Main package
│   ├── core/                   # Member, Subscriber, Plan models
│   ├── claims/                 # Claim, ClaimLine, Payment
│   ├── quality/                # HEDIS measures, care gaps
│   ├── authorization/          # Prior auth models
│   ├── network/                # Provider contracts
│   ├── vbc/                    # Value-based care
│   ├── formats/                # X12, FHIR exporters
│   ├── generation/             # Member generation (extends healthsim-core)
│   ├── scenarios/              # Timeline-based scenarios
│   ├── validation/             # Data validation (extends healthsim-core)
│   └── mcp/                    # MCP server
├── skills/                     # Claude skill files
│   ├── scenarios/              # Enrollment, claims, quality
│   ├── payer/                  # Domain knowledge
│   └── x12/                    # X12 EDI knowledge
├── examples/                   # Usage examples
│   ├── conversations/          # Natural language examples
│   └── developer/              # Python API examples
├── tests/                      # Test suite (150+ tests)
└── docs/                       # Documentation
```

---

## Advanced: MCP Integration

For advanced workflows, MemberSim provides **MCP (Model Context Protocol) servers**.

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

**MCP Tools:**
- `generate_member` — Create single member
- `generate_cohort` — Create member population
- `generate_claims` — Create claims for member
- `export_834` — Export enrollment file
- `export_837` — Export claims file
- `list_plans` — List available plan configurations
- `list_hedis_measures` — List HEDIS measure definitions

---

## Development

MemberSim follows modern Python development practices.

### Running Tests

```bash
pytest tests/ -v                          # Run all tests
pytest tests/ --cov=membersim             # With coverage
pytest tests/test_generation.py -v        # Specific module
```

### Code Quality

```bash
black src/ tests/              # Format code
ruff check src/ tests/ --fix   # Lint and auto-fix
mypy src/                      # Type checking
```

### Requirements

- Python 3.11+
- healthsim-core >= 0.2.0
- pydantic >= 2.0
- faker >= 20.0

### Contributing

Contributions welcome! We're especially interested in:

- **New X12 transaction types** (276/277, 820)
- **Additional HEDIS measures**
- **Provider network scenarios**
- **Documentation improvements**

---

## License

MIT License — see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for seamless integration with [Claude](https://claude.ai)
- X12 standards from [X12.org](https://x12.org)
- HEDIS specifications from [NCQA](https://www.ncqa.org)
- Built on [healthsim-core](https://github.com/mark64oswald/healthsim-core)

## Related Projects

- **[healthsim-core](https://github.com/mark64oswald/healthsim-core)** — Shared foundation library
- **[PatientSim](https://github.com/mark64oswald/PatientSim)** — Clinical/EMR data generation

## Support

- **Issues**: [Report bugs or request features](https://github.com/mark64oswald/MemberSim/issues)
- **Discussions**: [Ask questions or share ideas](https://github.com/mark64oswald/MemberSim/discussions)
- **Documentation**: [Read the docs](docs/)

---

## Important Note

**This software generates synthetic data for testing and development purposes only.**

MemberSim is designed for:
- ✅ Development and testing environments
- ✅ Educational purposes
- ✅ Analytics development with synthetic data
- ✅ System integration testing

MemberSim is **NOT** designed for:
- ❌ Production payer systems
- ❌ Real member data
- ❌ Actual claims processing
- ❌ HIPAA-regulated environments (without proper review)

All generated data is synthetic and should not be confused with real member information.

---

## Ready to Get Started?

1. **[Install MemberSim](#1-installation)**
2. **[Set Up Claude Project](#2-set-up-claude-project)**
3. **[Generate Your First Members](#3-your-first-member)**
4. **[Explore Use Cases](#use-cases)**

**Questions?** Check out our [examples](examples/) or open an issue!