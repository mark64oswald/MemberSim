# MemberSim Reference Data

Quick reference for codes and terminology.

## Relationship Codes (X12)
| Code | Description |
|------|-------------|
| 18 | Self (Subscriber) |
| 01 | Spouse |
| 19 | Child |
| 20 | Employee |
| 21 | Unknown |
| 53 | Life Partner |
| G8 | Other |

## Place of Service Codes
| Code | Description |
|------|-------------|
| 11 | Office |
| 12 | Home |
| 21 | Inpatient Hospital |
| 22 | Outpatient Hospital |
| 23 | Emergency Room |
| 31 | Skilled Nursing Facility |
| 81 | Independent Lab |

## Common CPT Codes
### Office Visits (E&M)
- 99211-99215: Established patient (levels 1-5)
- 99201-99205: New patient (levels 1-5)
- 99381-99397: Preventive visits by age

### Diagnostic
- 85025: CBC with differential
- 80053: Comprehensive metabolic panel
- 83036: HbA1c
- 80061: Lipid panel

### Imaging
- 71046: Chest X-ray (2 views)
- 72148: MRI lumbar spine
- 70553: MRI brain with contrast
- 77067: Screening mammogram

## Common ICD-10 Codes
### Chronic Conditions
- E11.9: Type 2 diabetes without complications
- I10: Essential hypertension
- J44.9: COPD
- N18.3: CKD Stage 3

### Acute Conditions
- J06.9: Acute upper respiratory infection
- R07.9: Chest pain, unspecified
- M54.5: Low back pain
- K21.0: GERD

### Preventive
- Z00.00: General adult exam
- Z12.31: Screening mammogram
- Z12.11: Screening colonoscopy

## Claim Adjustment Reason Codes (CARC)
| Code | Description |
|------|-------------|
| 1 | Deductible |
| 2 | Coinsurance |
| 3 | Copay |
| 45 | Charge exceeds fee schedule |
| 96 | Non-covered charge |
| 97 | Payment adjusted - prior payer |

## Authorization Status
| Status | Description |
|--------|-------------|
| PENDING | Under review |
| APPROVED | Authorized as requested |
| MODIFIED | Approved with changes |
| DENIED | Not authorized |
| CANCELLED | Request withdrawn |

## Denial Reason Codes
| Code | Description |
|------|-------------|
| MNC | Medical necessity criteria not met |
| INFO | Insufficient information |
| DUP | Duplicate request |
| EXCL | Service not covered |
| NETW | Out-of-network provider |