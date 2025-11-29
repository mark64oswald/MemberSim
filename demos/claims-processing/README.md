# Claims Processing Testing with MemberSim

This guide demonstrates how to use MemberSim for comprehensive claims processing system testing.

## Overview

MemberSim generates realistic synthetic claims data in industry-standard X12 formats, making it ideal for:

- **Claims Adjudication Testing** - Validate pricing, benefits, and payment logic
- **837P/837I Transaction Testing** - Professional and institutional claim workflows
- **835 Remittance Testing** - Payment reconciliation and ERA processing
- **Denial Management Testing** - CARC/RARC reason code handling
- **COB Testing** - Coordination of benefits scenarios
- **Load Testing** - Batch generation of thousands of claims

## Quick Start

### 1. Installation

```bash
cd /path/to/membersim
pip install -e ".[dev]"
```

### 2. Generate Your First Claim

```python
from datetime import date
from decimal import Decimal
from membersim.core.member import MemberGenerator
from membersim.claims.claim import Claim, ClaimLine

# Create member generator with reproducible seed
gen = MemberGenerator(seed=42)
member = gen.generate_one(plan_type="PPO")

print(f"Generated: {member.full_name}, Member ID: {member.member_id}")

# Create a professional claim
claim = Claim(
    claim_id="CLM001",
    member_id=member.member_id,
    subscriber_id=member.subscriber_id or member.member_id,
    provider_npi="1234567890",
    service_date=date(2024, 3, 15),
    claim_type="PROFESSIONAL",
    principal_diagnosis="J06.9",  # Acute upper respiratory infection
    place_of_service="11",        # Office
    claim_lines=[
        ClaimLine(
            line_number=1,
            procedure_code="99213",      # Office visit, established patient
            charge_amount=Decimal("150.00"),
            units=Decimal("1"),
            service_date=date(2024, 3, 15),
            diagnosis_pointers=[1],
        ),
    ],
)

print(f"Claim Total: ${claim.total_charge}")
```

### 3. Export to X12 Format

Choose your export format based on your testing needs:

| Format | Use Case | Function |
|--------|----------|----------|
| **X12 837P** | Professional claims processing | `generate_837p()` |
| **X12 837I** | Institutional claims processing | `generate_837i()` |
| **X12 835** | Remittance advice / ERA | `generate_835()` |
| **JSON** | Analytics, custom applications | `to_json()` |
| **CSV** | Reporting, data warehouses | `claims_to_csv()` |

```python
from membersim.formats import generate_837p

# Export to X12 837P
edi_837p = generate_837p([claim])
print(edi_837p[:500])
```

## Common Testing Scenarios

### Scenario 1: Professional Claims (837P) Testing

Test professional claim processing with office visits, labs, and specialist referrals:

```python
from datetime import date, timedelta
from decimal import Decimal
from membersim.core.member import MemberGenerator
from membersim.claims.claim import Claim, ClaimLine
from membersim.formats import generate_837p

# Generate member
gen = MemberGenerator(seed=42)
member = gen.generate_one(plan_type="PPO", min_age=30, max_age=60)

# Create a series of related claims
claims = []

# Day 1: Office visit with labs
office_visit = Claim(
    claim_id="CLM001",
    member_id=member.member_id,
    subscriber_id=member.subscriber_id or member.member_id,
    provider_npi="1234567890",
    service_date=date(2024, 3, 15),
    claim_type="PROFESSIONAL",
    principal_diagnosis="E11.9",  # Type 2 diabetes
    place_of_service="11",
    claim_lines=[
        ClaimLine(
            line_number=1,
            procedure_code="99214",      # Office visit, moderate complexity
            charge_amount=Decimal("200.00"),
            units=Decimal("1"),
            service_date=date(2024, 3, 15),
            diagnosis_pointers=[1],
        ),
        ClaimLine(
            line_number=2,
            procedure_code="83036",      # HbA1c test
            charge_amount=Decimal("45.00"),
            units=Decimal("1"),
            service_date=date(2024, 3, 15),
            diagnosis_pointers=[1],
        ),
        ClaimLine(
            line_number=3,
            procedure_code="80053",      # Comprehensive metabolic panel
            charge_amount=Decimal("85.00"),
            units=Decimal("1"),
            service_date=date(2024, 3, 15),
            diagnosis_pointers=[1],
        ),
    ],
)
claims.append(office_visit)

# Day 7: Specialist consultation
specialist_visit = Claim(
    claim_id="CLM002",
    member_id=member.member_id,
    subscriber_id=member.subscriber_id or member.member_id,
    provider_npi="9876543210",
    service_date=date(2024, 3, 22),
    claim_type="PROFESSIONAL",
    principal_diagnosis="E11.9",
    other_diagnoses=["E11.65"],  # Type 2 diabetes with hyperglycemia
    place_of_service="11",
    claim_lines=[
        ClaimLine(
            line_number=1,
            procedure_code="99243",      # Office consultation
            charge_amount=Decimal("275.00"),
            units=Decimal("1"),
            service_date=date(2024, 3, 22),
            diagnosis_pointers=[1, 2],
        ),
    ],
)
claims.append(specialist_visit)

# Export to 837P
edi_837p = generate_837p(claims)
print(f"Generated 837P with {len(claims)} claims")
print(f"Total charges: ${sum(c.total_charge for c in claims)}")
```

**Use Cases:**
- Testing claims adjudication pricing rules
- Validating CPT code edits and bundling
- Testing modifier handling
- Verifying diagnosis pointer logic

### Scenario 2: Batch Claims Generation

Generate large datasets for load testing and performance benchmarking:

```python
from datetime import date, timedelta
from decimal import Decimal
import random
from membersim.core.member import MemberGenerator
from membersim.claims.claim import Claim, ClaimLine
from membersim.formats import generate_837p, claims_to_csv

# Common procedure codes for professional claims
PROCEDURE_CODES = [
    ("99213", Decimal("150.00")),   # Office visit, low complexity
    ("99214", Decimal("200.00")),   # Office visit, moderate
    ("99215", Decimal("275.00")),   # Office visit, high complexity
    ("80053", Decimal("85.00")),    # Comprehensive metabolic panel
    ("83036", Decimal("45.00")),    # HbA1c
    ("85025", Decimal("25.00")),    # CBC with differential
    ("81001", Decimal("15.00")),    # Urinalysis
]

# Generate member population
gen = MemberGenerator(seed=42)
members = gen.generate_many(count=100)

# Generate claims for each member
all_claims = []
random.seed(42)

for i, member in enumerate(members):
    # Each member gets 1-5 claims
    num_claims = random.randint(1, 5)
    
    for j in range(num_claims):
        # Random service date in 2024
        service_date = date(2024, 1, 1) + timedelta(days=random.randint(0, 180))
        
        # Random procedures (1-3 per claim)
        num_lines = random.randint(1, 3)
        selected_procs = random.sample(PROCEDURE_CODES, num_lines)
        
        claim_lines = [
            ClaimLine(
                line_number=k + 1,
                procedure_code=proc[0],
                charge_amount=proc[1],
                units=Decimal("1"),
                service_date=service_date,
                diagnosis_pointers=[1],
            )
            for k, proc in enumerate(selected_procs)
        ]
        
        claim = Claim(
            claim_id=f"CLM{i:04d}{j:02d}",
            member_id=member.member_id,
            subscriber_id=member.subscriber_id or member.member_id,
            provider_npi=f"123456789{random.randint(0, 9)}",
            service_date=service_date,
            claim_type="PROFESSIONAL",
            principal_diagnosis="Z00.00",  # General exam
            place_of_service="11",
            claim_lines=claim_lines,
        )
        all_claims.append(claim)

print(f"Generated {len(all_claims)} claims for {len(members)} members")
print(f"Total charges: ${sum(c.total_charge for c in all_claims):,.2f}")

# Export formats
edi_837p = generate_837p(all_claims)
csv_data = claims_to_csv(all_claims)
```

**Output:**
- X12 837P transaction set with 200+ claims
- CSV export for analytics
- Performance metrics

**Use Cases:**
- Load testing claims processing systems
- Database population
- Performance benchmarking
- Stress testing clearinghouse interfaces

### Scenario 3: Institutional Claims (837I) Testing

Test institutional claims for hospital stays and outpatient procedures:

```python
from datetime import date, timedelta
from decimal import Decimal
from membersim.core.member import MemberGenerator
from membersim.claims.claim import Claim, ClaimLine
from membersim.formats import generate_837i

# Generate member
gen = MemberGenerator(seed=42)
member = gen.generate_one(plan_type="PPO", min_age=50, max_age=70)

# Create inpatient hospital claim
inpatient_claim = Claim(
    claim_id="INST001",
    member_id=member.member_id,
    subscriber_id=member.subscriber_id or member.member_id,
    provider_npi="1122334455",
    service_date=date(2024, 4, 1),
    claim_type="INSTITUTIONAL",
    principal_diagnosis="I21.09",  # STEMI of unspecified site
    other_diagnoses=["I25.10", "E11.9", "I10"],  # CAD, DM, HTN
    place_of_service="21",  # Inpatient hospital
    claim_lines=[
        # Room and board
        ClaimLine(
            line_number=1,
            procedure_code="",
            revenue_code="0120",          # Room & board - semi-private
            charge_amount=Decimal("2500.00"),
            units=Decimal("3"),           # 3 days
            service_date=date(2024, 4, 1),
            diagnosis_pointers=[1],
        ),
        # ICU
        ClaimLine(
            line_number=2,
            procedure_code="",
            revenue_code="0200",          # ICU
            charge_amount=Decimal("4500.00"),
            units=Decimal("1"),
            service_date=date(2024, 4, 1),
            diagnosis_pointers=[1],
        ),
        # Cardiac catheterization
        ClaimLine(
            line_number=3,
            procedure_code="93458",       # Left heart cath
            revenue_code="0481",          # Cardiology
            charge_amount=Decimal("8500.00"),
            units=Decimal("1"),
            service_date=date(2024, 4, 2),
            diagnosis_pointers=[1, 2],
        ),
        # Pharmacy
        ClaimLine(
            line_number=4,
            procedure_code="",
            revenue_code="0250",          # Pharmacy
            charge_amount=Decimal("1200.00"),
            units=Decimal("1"),
            service_date=date(2024, 4, 1),
            diagnosis_pointers=[1],
        ),
        # Laboratory
        ClaimLine(
            line_number=5,
            procedure_code="",
            revenue_code="0300",          # Laboratory
            charge_amount=Decimal("850.00"),
            units=Decimal("1"),
            service_date=date(2024, 4, 1),
            diagnosis_pointers=[1],
        ),
    ],
)

# Export to 837I
edi_837i = generate_837i([inpatient_claim])
print(f"Hospital claim total: ${inpatient_claim.total_charge:,.2f}")
```

**Use Cases:**
- Testing DRG assignment and pricing
- Validating revenue code processing
- Testing inpatient benefit accumulators
- Hospital contract rate testing

### Scenario 4: Denial Scenarios Testing

Test claims denial workflows with various denial reason codes:

```python
from datetime import date
from decimal import Decimal
from membersim.core.member import MemberGenerator
from membersim.claims.claim import Claim, ClaimLine
from membersim.claims.adjudication import (
    AdjudicatedClaim,
    AdjudicatedLine,
    AdjustmentReason,
)

# Generate member
gen = MemberGenerator(seed=42)
member = gen.generate_one(plan_type="HMO")

# Claim that will be denied - no authorization
unauthorized_claim = Claim(
    claim_id="DEN001",
    member_id=member.member_id,
    subscriber_id=member.subscriber_id or member.member_id,
    provider_npi="5555555555",
    service_date=date(2024, 3, 15),
    claim_type="PROFESSIONAL",
    principal_diagnosis="M54.5",  # Low back pain
    place_of_service="11",
    claim_lines=[
        ClaimLine(
            line_number=1,
            procedure_code="72148",      # MRI lumbar spine
            charge_amount=Decimal("1500.00"),
            units=Decimal("1"),
            service_date=date(2024, 3, 15),
            diagnosis_pointers=[1],
        ),
    ],
)

# Adjudicate with denial
adjudicated = AdjudicatedClaim(
    claim=unauthorized_claim,
    adjudication_date=date(2024, 3, 20),
    status="DENIED",
    lines=[
        AdjudicatedLine(
            line_number=1,
            charge_amount=Decimal("1500.00"),
            allowed_amount=Decimal("0.00"),
            paid_amount=Decimal("0.00"),
            patient_responsibility=Decimal("0.00"),
            adjustments=[
                AdjustmentReason(
                    group_code="CO",           # Contractual obligation
                    reason_code="4",           # Service not covered
                    amount=Decimal("1500.00"),
                ),
            ],
            remark_codes=["N56"],  # Procedure requires prior authorization
        ),
    ],
)

# Common denial scenarios
DENIAL_SCENARIOS = [
    {
        "name": "Prior Authorization Required",
        "carc": "4",
        "rarc": "N56",
        "description": "Procedure requires prior authorization",
    },
    {
        "name": "Not Medically Necessary",
        "carc": "50",
        "rarc": "M59",
        "description": "Non-covered because not medically necessary",
    },
    {
        "name": "Duplicate Claim",
        "carc": "18",
        "rarc": "MA130",
        "description": "Duplicate claim/service",
    },
    {
        "name": "Timely Filing",
        "carc": "29",
        "rarc": "N362",
        "description": "Claim submitted past timely filing limit",
    },
    {
        "name": "Out of Network",
        "carc": "B7",
        "rarc": "N519",
        "description": "Provider not in network",
    },
    {
        "name": "Member Not Eligible",
        "carc": "27",
        "rarc": "N535",
        "description": "Member not eligible on date of service",
    },
]

print("Common Denial Scenarios for Testing:")
for scenario in DENIAL_SCENARIOS:
    print(f"  - {scenario['name']}: CARC {scenario['carc']}, RARC {scenario['rarc']}")
```

**Use Cases:**
- Testing denial reason code mapping
- Validating denial workflow triggers
- Testing appeals processing
- Denial management reporting

### Scenario 5: Coordination of Benefits (COB)

Test claims with primary and secondary payer scenarios:

```python
from datetime import date
from decimal import Decimal
from membersim.core.member import MemberGenerator
from membersim.claims.claim import Claim, ClaimLine
from membersim.claims.adjudication import (
    AdjudicatedClaim,
    AdjudicatedLine,
    AdjustmentReason,
    COBInfo,
)

# Generate member with dual coverage
gen = MemberGenerator(seed=42)
member = gen.generate_one(plan_type="PPO")

# Create claim
claim = Claim(
    claim_id="COB001",
    member_id=member.member_id,
    subscriber_id=member.subscriber_id or member.member_id,
    provider_npi="1234567890",
    service_date=date(2024, 3, 15),
    claim_type="PROFESSIONAL",
    principal_diagnosis="J06.9",
    place_of_service="11",
    claim_lines=[
        ClaimLine(
            line_number=1,
            procedure_code="99214",
            charge_amount=Decimal("200.00"),
            units=Decimal("1"),
            service_date=date(2024, 3, 15),
            diagnosis_pointers=[1],
        ),
    ],
)

# Primary payer adjudication
primary_adjudication = AdjudicatedClaim(
    claim=claim,
    adjudication_date=date(2024, 3, 20),
    status="PAID",
    payer_type="PRIMARY",
    lines=[
        AdjudicatedLine(
            line_number=1,
            charge_amount=Decimal("200.00"),
            allowed_amount=Decimal("150.00"),
            paid_amount=Decimal("120.00"),          # 80% after deductible met
            patient_responsibility=Decimal("30.00"),
            adjustments=[
                AdjustmentReason(
                    group_code="CO",
                    reason_code="45",               # Charge exceeds allowed
                    amount=Decimal("50.00"),
                ),
                AdjustmentReason(
                    group_code="PR",
                    reason_code="3",                # Coinsurance
                    amount=Decimal("30.00"),
                ),
            ],
        ),
    ],
)

# Secondary payer receives claim with primary EOB info
cob_info = COBInfo(
    other_payer_id="PRIMARY001",
    other_payer_paid=Decimal("120.00"),
    other_payer_allowed=Decimal("150.00"),
    patient_responsibility_primary=Decimal("30.00"),
    coordination_order="SECONDARY",
)

# Secondary payer adjudication (picks up patient responsibility)
secondary_adjudication = AdjudicatedClaim(
    claim=claim,
    adjudication_date=date(2024, 3, 25),
    status="PAID",
    payer_type="SECONDARY",
    cob_info=cob_info,
    lines=[
        AdjudicatedLine(
            line_number=1,
            charge_amount=Decimal("200.00"),
            allowed_amount=Decimal("160.00"),       # Secondary's allowed
            paid_amount=Decimal("30.00"),           # Picks up patient resp
            patient_responsibility=Decimal("0.00"), # Member owes nothing
            adjustments=[
                AdjustmentReason(
                    group_code="OA",
                    reason_code="23",               # Primary payer amount
                    amount=Decimal("120.00"),
                ),
                AdjustmentReason(
                    group_code="CO",
                    reason_code="45",
                    amount=Decimal("50.00"),
                ),
            ],
        ),
    ],
)

print("COB Scenario Summary:")
print(f"  Billed: ${claim.total_charge}")
print(f"  Primary Paid: ${primary_adjudication.total_paid}")
print(f"  Secondary Paid: ${secondary_adjudication.total_paid}")
print(f"  Member Owes: ${secondary_adjudication.total_patient_responsibility}")
```

**Use Cases:**
- Testing COB rules (birthday rule, gender rule)
- Validating secondary claim submission
- Testing Medicare secondary payer scenarios
- Worker's comp and auto liability testing

## X12 Format Details

### X12 837P Segment Structure

The 837P (Professional) transaction contains these key segments:

| Segment | Description | Key Fields |
|---------|-------------|------------|
| **ISA** | Interchange Control Header | Sender/receiver IDs, date/time |
| **GS** | Functional Group Header | Application sender/receiver |
| **ST** | Transaction Set Header | Transaction set ID (837) |
| **BHT** | Beginning of Hierarchical Transaction | Purpose, reference ID |
| **2000A** | Billing Provider HL | Provider info loop |
| **2010AA** | Billing Provider Name | NPI, tax ID, address |
| **2000B** | Subscriber HL | Subscriber info loop |
| **2010BA** | Subscriber Name | Member demographics |
| **2300** | Claim Information | Claim ID, dates, diagnosis |
| **2400** | Service Line | CPT, charges, units |
| **SE** | Transaction Set Trailer | Segment count |
| **GE** | Functional Group Trailer | Transaction count |
| **IEA** | Interchange Control Trailer | Group count |

**Example 837P Output:**
```
ISA*00*          *00*          *ZZ*MEMBERSIM      *ZZ*RECEIVER       *240315*1030*^*00501*000000001*0*P*:~
GS*HC*MEMBERSIM*RECEIVER*20240315*1030*1*X*005010X222A1~
ST*837*0001*005010X222A1~
BHT*0019*00*CLM001*20240315*1030*CH~
NM1*41*2*BILLING PROVIDER*****XX*1234567890~
PER*IC*CONTACT*TE*5555551234~
NM1*40*2*RECEIVER NAME*****46*12345~
HL*1**20*1~
NM1*85*2*RENDERING PROVIDER*****XX*1234567890~
HL*2*1*22*0~
NM1*IL*1*SMITH*JOHN****MI*MEM123456~
DMG*D8*19800315*M~
CLM*CLM001*150***11:B:1*Y*A*Y*Y~
HI*ABK:J069~
LX*1~
SV1*HC:99213*150*UN*1***1~
DTP*472*D8*20240315~
SE*18*0001~
GE*1*1~
IEA*1*000000001~
```

### X12 837I Segment Structure

The 837I (Institutional) transaction includes additional segments:

| Segment | Description | Key Fields |
|---------|-------------|------------|
| **2300** | Claim Information | Statement dates, DRG, admission type |
| **2400** | Service Line | Revenue code, HCPCS, units |
| **CL1** | Institutional Claim Code | Admission type, source, status |
| **2310A** | Attending Provider | Attending physician NPI |
| **2310E** | Referring Provider | Referring physician info |

**Key Institutional Fields:**
- Revenue codes (0100-0999)
- Admission type (1=Emergency, 2=Urgent, 3=Elective)
- Discharge status (01=Home, 02=SNF, 20=Expired)
- Bill type (111=Inpatient, 131=Outpatient)

### X12 835 Remittance Structure

The 835 (Remittance Advice) reports payment information:

| Segment | Description | Key Fields |
|---------|-------------|------------|
| **BPR** | Financial Information | Payment amount, method, date |
| **TRN** | Reassociation Trace | Check/EFT number |
| **1000A** | Payer Identification | Payer name and ID |
| **1000B** | Payee Identification | Provider name and ID |
| **2100** | Claim Payment Information | Claim ID, status, paid amount |
| **2110** | Service Payment Information | Line-level payments |
| **CAS** | Claim Adjustment Segment | CARC/RARC codes |
| **PLB** | Provider Level Adjustment | Withholdings, recoupments |

**Common Adjustment Group Codes:**
- **CO** - Contractual Obligations
- **PR** - Patient Responsibility
- **OA** - Other Adjustments
- **PI** - Payer Initiated Reductions
- **CR** - Correction and Reversal

## MCP Integration (Claude Code)

MemberSim provides an MCP server for seamless integration with Claude Code.

### Setup

1. Install MemberSim:
```bash
pip install -e ".[dev]"
```

2. Configure Claude Code (add to `.claude/mcp_settings.json`):
```json
{
  "mcpServers": {
    "membersim": {
      "command": "python",
      "args": ["-m", "membersim.mcp.server"],
      "env": {
        "PYTHONPATH": "${workspaceFolder}/src"
      }
    }
  }
}
```

3. Restart Claude Code

### Usage Examples

**Generate test claims:**
```
Generate 10 professional claims for diabetes patients with HbA1c tests
```

**Create denial scenarios:**
```
Create 5 claims that should be denied for prior authorization failure
```

**Export for testing:**
```
Generate an 837P file with 50 claims for load testing our clearinghouse
```

**COB testing:**
```
Create a claim scenario with Medicare as primary and our plan as secondary
```

## Testing Workflows

### 1. Claims Adjudication Testing

**Goal:** Validate pricing and benefit application

**Steps:**
1. Generate claims with known charge amounts
2. Submit to adjudication engine
3. Verify allowed amounts match fee schedule
4. Confirm member responsibility calculation
5. Check accumulator updates

**Example:**
```python
# Generate claim with known values
claim = create_test_claim(
    procedure="99214",
    charge=Decimal("200.00"),
    expected_allowed=Decimal("150.00"),  # Per fee schedule
    expected_paid=Decimal("120.00"),     # After 20% coinsurance
)

# Submit and verify
result = adjudication_engine.process(claim)
assert result.allowed_amount == Decimal("150.00")
assert result.paid_amount == Decimal("120.00")
assert result.patient_responsibility == Decimal("30.00")
```

### 2. Payment Accuracy Testing

**Goal:** Ensure correct payment calculations

**Steps:**
1. Generate claims with various benefit scenarios
2. Test deductible application
3. Test coinsurance calculation
4. Verify out-of-pocket maximum
5. Validate COB calculations

**Test Cases:**
```python
# Deductible not met
test_deductible_applies(
    ytd_deductible=Decimal("0.00"),
    claim_allowed=Decimal("150.00"),
    individual_deductible=Decimal("500.00"),
    expected_patient_resp=Decimal("150.00"),
)

# Deductible met, coinsurance applies
test_coinsurance_applies(
    ytd_deductible=Decimal("500.00"),
    claim_allowed=Decimal("150.00"),
    coinsurance=Decimal("0.20"),
    expected_patient_resp=Decimal("30.00"),
)

# OOP max reached
test_oop_max_reached(
    ytd_oop=Decimal("4900.00"),
    oop_max=Decimal("5000.00"),
    claim_allowed=Decimal("500.00"),
    expected_patient_resp=Decimal("100.00"),  # Caps at OOP max
)
```

### 3. Denial Management Testing

**Goal:** Validate denial workflows and reason codes

**Steps:**
1. Generate claims designed to deny
2. Verify correct denial reason codes
3. Test appeals workflow
4. Validate denial notifications

**Example:**
```bash
# Generate denial test set
python -c "
from membersim.testing import generate_denial_test_set

denials = generate_denial_test_set(
    scenarios=['auth_required', 'timely_filing', 'duplicate', 'not_covered'],
    seed=42
)
for d in denials:
    print(f'{d.claim_id}: Expected CARC {d.expected_carc}')
"
```

### 4. Clearinghouse Integration Testing

**Goal:** Test X12 transaction exchange

**Steps:**
1. Generate 837P/837I transactions
2. Submit to clearinghouse
3. Receive 999 acknowledgment
4. Process 835 remittance
5. Reconcile payments

**Example:**
```bash
# Generate and submit
python generate_837p_batch.py --count 100 --output batch_001.edi

# Simulate submission
curl -X POST https://clearinghouse.example/submit \
  -H "Content-Type: application/edi-x12" \
  -d @batch_001.edi

# Process response
python process_835_response.py --input era_001.edi
```

## Reproducibility

MemberSim supports deterministic generation for reproducible tests:

```python
from membersim.core.member import MemberGenerator

# Always generates the same member and claims
gen1 = MemberGenerator(seed=42)
member1 = gen1.generate_one()

gen2 = MemberGenerator(seed=42)
member2 = gen2.generate_one()

assert member1.member_id == member2.member_id
assert member1.full_name == member2.full_name
```

**Use Cases:**
- Regression testing
- Test case documentation
- Bug reproduction
- Continuous integration

## Troubleshooting

### Common Issues

**Issue:** Import errors when running examples
```
ModuleNotFoundError: No module named 'membersim'
```
**Solution:** Install in development mode: `pip install -e ".[dev]"`

---

**Issue:** X12 validation errors
```
Invalid segment terminator
```
**Solution:** Ensure using `~` as segment terminator, not `\n`. Check your EDI viewer settings.

---

**Issue:** Claims missing required fields
```
KeyError: 'subscriber_id'
```
**Solution:** For self-pay members, set `subscriber_id = member_id`:
```python
claim.subscriber_id = member.subscriber_id or member.member_id
```

---

**Issue:** Decimal precision errors
```
InvalidOperation: quantize result has too many digits
```
**Solution:** Use `Decimal` from the start, don't convert from float:
```python
# Good
charge = Decimal("150.00")

# Bad - can cause precision issues
charge = Decimal(150.00)
```

---

**Issue:** Date format errors in X12
```
Invalid date format in DTP segment
```
**Solution:** Dates must be `CCYYMMDD` format (e.g., `20240315`). MemberSim handles this automatically when using `date` objects.

## Performance Benchmarks

Generation performance on MacBook Pro (M1):

| Operation | Count | Time | Rate |
|-----------|-------|------|------|
| Generate Members | 1,000 | 1.8s | 556/sec |
| Generate Claims | 1,000 | 2.4s | 417/sec |
| Generate 837P | 1,000 claims | 3.1s | 323/sec |
| Generate 835 | 1,000 claims | 2.8s | 357/sec |
| Full adjudication | 1,000 claims | 4.5s | 222/sec |

**Tips for Performance:**
- Reuse generator instance for batches
- Set seed for reproducibility
- Generate in batches of 100-1000
- Use parallel processing for 10k+ claims

## Next Steps

- **Read the docs:** [API Reference](../../docs/api.md)
- **Try examples:** Run scripts in [examples/](../../examples/)
- **Explore scenarios:** See [scenarios/](../../skills/scenarios/)
- **X12 deep dive:** See [X12 Formats Reference](../../docs/reference/x12-formats.md)

## Support

- **Documentation:** [README.md](../../README.md)
- **Examples:** [examples/](../../examples/)
- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions

## License

Apache License 2.0 - See [LICENSE](../../LICENSE) for details
