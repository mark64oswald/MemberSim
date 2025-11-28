# MemberSim API Reference

## Core Models

### Member
```python
from membersim.core.member import Member
from healthsim.person import Address, Gender, PersonName

Member(
    id: str,                    # Unique person identifier
    name: PersonName,           # Name components (given_name, family_name)
    birth_date: date,           # Date of birth
    gender: Gender,             # Gender.MALE, Gender.FEMALE, etc.
    address: Address = None,    # Physical address (optional)
    member_id: str,             # Unique member identifier
    subscriber_id: str = None,  # Reference to subscriber (for dependents)
    relationship_code: str = "18",  # X12 relationship (18=Self, 01=Spouse, 19=Child)
    group_id: str,              # Employer/group identifier
    coverage_start: date,       # Coverage effective date
    coverage_end: date = None,  # Coverage termination date (None if active)
    plan_code: str,             # Benefit plan identifier
    pcp_npi: str = None,        # Assigned PCP NPI (for HMO plans)
)

# Properties
member.is_active -> bool        # Coverage currently active
member.is_subscriber -> bool    # Is the primary subscriber (relationship_code="18")
member.age -> int               # Current age in years
member.full_name -> str         # Full formatted name
```

### MemberGenerator
```python
from membersim.core.member import MemberGenerator

generator = MemberGenerator(seed=42)

# Generate single member
member = generator.generate_one(
    gender="F",          # Optional: "M" or "F"
    plan_type="PPO",     # Optional: "HMO", "PPO", "HDHP"
    min_age=18,          # Optional: minimum age
    max_age=65,          # Optional: maximum age
)

# Generate multiple members
members = generator.generate_many(count=100)
```

### Plan
```python
from membersim.core.plan import Plan, SAMPLE_PLANS

Plan(
    plan_code: str,
    plan_name: str,
    plan_type: str,               # PPO, HMO, EPO, HDHP
    deductible_individual: Decimal,
    deductible_family: Decimal,
    oop_max_individual: Decimal,
    oop_max_family: Decimal,
    coinsurance: Decimal,         # e.g., 0.20 for 20%
    copay_pcp: Decimal,
    copay_specialist: Decimal,
    copay_er: Decimal,
)

# Pre-defined plans
SAMPLE_PLANS["PPO_GOLD"]
SAMPLE_PLANS["PPO_SILVER"]
SAMPLE_PLANS["HMO_STANDARD"]
SAMPLE_PLANS["HDHP_HSA"]
```

### Claim
```python
from membersim.claims.claim import Claim, ClaimLine

ClaimLine(
    line_number: int,
    procedure_code: str,          # CPT/HCPCS
    charge_amount: Decimal,
    units: Decimal,
    service_date: date,
    diagnosis_pointers: list[int],
    procedure_modifiers: list[str] = [],
    revenue_code: str = None,     # For institutional claims
)

Claim(
    claim_id: str,
    member_id: str,
    subscriber_id: str,
    provider_npi: str,
    service_date: date,
    claim_type: str,              # "PROFESSIONAL" or "INSTITUTIONAL"
    principal_diagnosis: str,
    claim_lines: list[ClaimLine],
    place_of_service: str = "11",
    other_diagnoses: list[str] = [],
)

# Properties
claim.total_charge -> Decimal
claim.total_units -> Decimal
claim.all_diagnoses -> list[str]
```

## Format Generators

### X12 Transactions
```python
from membersim.formats import (
    generate_834,           # Enrollment
    generate_837p,          # Professional claims
    generate_837i,          # Institutional claims
    generate_835,           # Remittance
    generate_270,           # Eligibility inquiry
    generate_271,           # Eligibility response
    generate_278_request,   # Auth request
    generate_278_response,  # Auth response
)

# Usage
edi_string = generate_834(members: list[Member])
edi_string = generate_837p(claims: list[Claim])
edi_string = generate_270(member: Member, service_date: date = None)
edi_string = generate_271(member: Member, plan: Plan, is_eligible: bool = True)
```

### Export Functions
```python
from membersim.formats.export import (
    JSONEncoder,       # Custom JSON encoder for dates, Decimals
    to_json,           # Any model to JSON string
    to_csv,            # List of models to CSV string
    members_to_csv,    # Members with flattened demographics
    claims_to_csv,     # Claims summary
)

# JSON export
json_str = to_json(member, pretty=True)
json_str = to_json(members)  # List

# CSV export
csv_str = members_to_csv(members)
csv_str = claims_to_csv(claims)
```

### FHIR Resources
```python
from membersim.formats.fhir import (
    member_to_fhir_coverage,
    member_to_fhir_patient,
    create_fhir_bundle,
)

# Generate FHIR resources
coverage = member_to_fhir_coverage(member, plan=None)
patient = member_to_fhir_patient(member)
bundle = create_fhir_bundle([coverage, patient], bundle_type="collection")
```

## Quality Measures

```python
from membersim.quality import (
    HEDIS_MEASURES,           # Dict of measure definitions
    get_measure,              # Get single measure by ID
    get_measures_for_member,  # Get applicable measures for a member
    generate_care_gaps,       # Generate gap data for population
    generate_measure_status,  # Single member/measure status
)

# Access measures
measure = get_measure("BCS")  # Breast Cancer Screening
measures = get_measures_for_member(member)

# Generate gaps
gaps = generate_care_gaps(
    members: list[Member],
    measures: list[str] = None,  # None = all applicable
    gap_rate: float = 0.3,       # Target open gap rate
    measure_year: int = 2024,
    seed: int = None,            # For reproducibility
)

# MemberMeasureStatus fields
gap.member_id: str
gap.measure_id: str
gap.measure_year: int
gap.in_denominator: bool
gap.in_numerator: bool
gap.gap_status: str  # "OPEN", "CLOSED", "NOT_APPLICABLE"
```

## Value-Based Care

```python
from membersim.vbc import (
    Attribution,
    AttributionMethod,
    AttributionPanel,
    CapitationRate,
    CapitationPayment,
    calculate_capitation_payment,
    HCC_CATEGORIES,
)

# Attribution
attribution = Attribution(
    attribution_id: str,
    member_id: str,
    provider_npi: str,
    provider_tin: str = None,
    attribution_method: str = AttributionMethod.PROSPECTIVE,
    attribution_reason: str = "PCP_SELECTION",
    effective_date: date,
    termination_date: date = None,
    performance_year: int,
    risk_score: Decimal = None,
    hcc_codes: list[str] = [],
)

# Attribution methods
AttributionMethod.PROSPECTIVE   # Assigned at start of period
AttributionMethod.RETROSPECTIVE # Assigned after claims analysis
AttributionMethod.HYBRID        # Combination

# Capitation
rate = CapitationRate(
    rate_id: str,
    contract_id: str,
    rate_category: str,       # "PEDIATRIC", "ADULT", "SENIOR"
    base_pmpm: Decimal,
    risk_adjusted: bool = True,
)

payment = calculate_capitation_payment(
    provider_npi: str,
    contract_id: str,
    payment_period: str,      # "YYYY-MM" format
    members: list[dict],      # {"member_id", "age", "risk_score"}
    rates: dict[str, CapitationRate],
)
```

## Scenarios

```python
from membersim.scenarios import (
    ScenarioEngine,
    ScenarioDefinition,
    ScenarioEvent,
    SCENARIO_LIBRARY,
    EventType,
    EventCategory,
)

# Get predefined scenario
scenario = SCENARIO_LIBRARY.get("diabetic_member")
scenario = SCENARIO_LIBRARY.get("new_employee")
scenario = SCENARIO_LIBRARY.get("preventive_care")

# Create timeline
engine = ScenarioEngine()
timeline = engine.create_timeline(member, scenario, start_date)

# Get and execute events
events = timeline.get_pending_events(as_of_date)
for event in events:
    result = engine.execute_event(event)

# Event types
EventType.ENROLLMENT
EventType.OFFICE_VISIT
EventType.LAB_TEST
EventType.PRESCRIPTION
EventType.HOSPITALIZATION
```

## Authorization

```python
from membersim.authorization import Authorization, AuthorizationStatus
from membersim.formats import generate_278_request, generate_278_response

auth = Authorization(
    auth_id: str,
    member_id: str,
    provider_npi: str,
    service_type: str,
    procedure_codes: list[str],
    diagnosis_codes: list[str],
    request_date: date,
    service_start: date,
    service_end: date = None,
    status: str = AuthorizationStatus.PENDING,
)

# Generate 278 transactions
edi_278_req = generate_278_request(auth)
edi_278_resp = generate_278_response(auth)
```

## Network

```python
from membersim.network import (
    Provider,
    ProviderContract,
    FeeSchedule,
    create_default_fee_schedule,
    MEDICARE_BASE_RATES,
)

# Provider contract
contract = ProviderContract(
    contract_id: str,
    provider_npi: str,
    payer_id: str,
    contract_type: str,       # "FFS", "CAPITATION", "VBC"
    effective_date: date,
    termination_date: date = None,
    fee_schedule_id: str = None,
)

# Fee schedule
fee_schedule = create_default_fee_schedule(
    pct_of_medicare: Decimal = Decimal("1.10"),  # 110% of Medicare
)
allowed = fee_schedule.get_allowed_amount("99213", units=1)
```