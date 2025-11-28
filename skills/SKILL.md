# MemberSim Skills

MemberSim generates synthetic health plan member data, claims, eligibility, and value-based care scenarios for payer/TPA testing.

## Quick Start

**Create a member:**
"Create a 45-year-old female member enrolled in a PPO Gold plan starting January 2024."

**Generate claims:**
"Create an office visit claim for member MEM12345 with diagnosis J06.9 and procedure 99213."

**Check eligibility:**
"Check eligibility for member MEM12345 and show the 270/271 transaction."

**Generate care gaps:**
"Generate HEDIS care gaps for all female members over 50 with a 40% open gap rate."

## Available Tools

| Tool | Purpose |
|------|---------|
| `create_member` | Create member with demographics and coverage |
| `create_claim` | Create professional or institutional claim |
| `check_eligibility` | Generate 270/271 eligibility transactions |
| `generate_care_gaps` | Generate HEDIS quality measure gaps |
| `export_members` | Export to JSON, CSV, FHIR, or 834 |
| `export_claims` | Export to JSON, CSV, or 837 |
| `list_plans` | Show available plan configurations |
| `list_hedis_measures` | Show HEDIS measure definitions |

## Domain Knowledge

### Plan Types
- **PPO_GOLD**: High premium, low deductible ($500), 20% coinsurance
- **PPO_SILVER**: Mid-tier, $1500 deductible, 25% coinsurance
- **HMO_STANDARD**: Low premium, PCP required, $30 copays
- **HDHP_HSA**: High deductible ($3000), HSA eligible

### X12 Transactions
- **834**: Enrollment/eligibility maintenance
- **837P/I**: Professional and institutional claims
- **835**: Remittance/payment advice
- **270/271**: Eligibility inquiry/response
- **278**: Prior authorization request/response

### HEDIS Measures
- **BCS**: Breast Cancer Screening (women 50-74)
- **CCS**: Cervical Cancer Screening (women 21-64)
- **COL**: Colorectal Cancer Screening (adults 50-75)
- **CDC-A1C**: Diabetes HbA1c Testing
- **CDC-EYE**: Diabetes Eye Exam
- **CBP**: Controlling Blood Pressure

## Example Conversations

### Enrollment Testing
```
User: I need to test 834 enrollment files. Create 5 members with different demographics.

Claude: I'll create diverse members for enrollment testing...
[Creates members with varying ages, genders, plan types]
[Exports as 834 format]
```

### Claims Processing
```
User: Generate a claim for a diabetic patient seeing an endocrinologist.

Claude: I'll create a specialist visit claim with diabetes diagnosis...
[Creates claim with E11.9 diagnosis, 99214 procedure]
[Can export as 837P or JSON]
```

### Quality Reporting
```
User: Show me which members have open care gaps for diabetes measures.

Claude: I'll generate CDC measure status for diabetic members...
[Generates CDC-A1C and CDC-EYE gaps]
[Shows which members need A1c tests or eye exams]
```

## Output Formats

### JSON
```json
{
  "member_id": "MEM12345",
  "name": {
    "given_name": "Jane",
    "family_name": "Smith"
  },
  "birth_date": "1975-06-15",
  "gender": "female",
  "plan_code": "PPO_GOLD",
  "coverage_start": "2024-01-01"
}
```

### FHIR Coverage
```json
{
  "resourceType": "Coverage",
  "status": "active",
  "beneficiary": {"reference": "Patient/MEM12345"},
  "period": {"start": "2024-01-01"}
}
```

### X12 834
```
ISA*00*          *00*          *ZZ*MEMBERSIM...
GS*BE*MEMBERSIM*RECEIVER*20240101*1200*1*X*005010X220A1~
ST*834*0001~
BGN*00*REF20240101*20240101~
...
```

## Integration Notes

MemberSim uses healthsim-core for shared demographics and address models. All members have consistent data structures across PatientSim and MemberSim products.

For batch generation or programmatic use, see the MemberSim Python API documentation.