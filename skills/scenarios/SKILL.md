# MemberSim Scenarios

Detailed scenario guidance for common payer testing workflows.

## Enrollment Scenarios

### New Member Enrollment
"Create a new family enrollment: subscriber John Doe (35/M), spouse Jane (33/F), and two children (8/M, 5/F). All on HMO Standard starting March 2024."

**Generates:**
- Subscriber with relationship_code "18" (Self)
- Dependents with relationship_codes "01" (Spouse), "19" (Child)
- 834 with maintenance_type "021" (Addition)

### Member Termination
"Terminate member MEM12345 effective end of month due to voluntary disenrollment."

**Generates:**
- 834 with maintenance_type "024" (Termination)
- Coverage end date set

### Plan Change
"Change member MEM12345 from PPO Gold to HDHP HSA effective next month."

**Generates:**
- 834 with maintenance_type "001" (Change)
- Updated plan_code

## Claims Scenarios

### Office Visit
"Create a routine office visit: 99213 with hypertension diagnosis I10."

**Typical structure:**
- CPT: 99213 (Office visit level 3)
- ICD-10: I10 (Essential hypertension)
- POS: 11 (Office)
- Charge: $150-200

### Preventive Care
"Create a wellness visit for a 50-year-old with mammogram screening."

**Typical structure:**
- CPT: 99396 (Preventive 40-64) + 77067 (Mammogram)
- ICD-10: Z00.00 (Encounter for exam)
- Often $0 member cost for preventive

### Emergency Room
"Create an ER visit for chest pain with ECG and X-ray."

**Typical structure:**
- CPT: 99284 (ER level 4) + 93000 (ECG) + 71046 (Chest X-ray)
- ICD-10: R07.9 (Chest pain)
- POS: 23 (Emergency Room)
- Higher coinsurance typically applies

### Inpatient Admission
"Create a 3-day inpatient stay for pneumonia."

**Typical structure:**
- Revenue codes: 0120 (Room & Board)
- ICD-10: J18.9 (Pneumonia)
- DRG-based pricing for institutional claims

## Eligibility Scenarios

### Standard Eligibility Check
"Check if member MEM12345 is eligible for services on March 15, 2024."

**Generates:**
- 270 inquiry with service date
- 271 response showing:
  - Active/Inactive status
  - Deductible amounts (individual/family)
  - OOP remaining
  - Copay amounts by service type

### Accumulator Status
"Show how much deductible member MEM12345 has met year-to-date."

**Returns:**
- Individual deductible: $500 of $1,500 met
- Family deductible: $1,200 of $3,000 met
- OOP max status

## Quality Measure Scenarios

### Population Care Gaps
"Generate care gaps for my diabetic population with 30% compliance rate."

**Generates:**
- Members with diabetes diagnoses
- CDC-A1C (HbA1c testing) gaps
- CDC-EYE (Eye exam) gaps
- Configurable gap rate

### Individual Member Gaps
"What care gaps does member MEM12345 have?"

**Returns:**
- All applicable measures based on age/gender
- Open vs. closed status
- Last service date if compliant

### Outreach List
"Give me a list of women 50-74 who need mammograms."

**Generates:**
- BCS measure filtering
- Members with OPEN gap status
- Contact information for outreach

## Value-Based Care Scenarios

### Provider Attribution
"Attribute 100 members to provider NPI 1234567890 for 2024."

**Generates:**
- Attribution records with effective dates
- Risk scores (if specified)
- Panel summary

### Capitation Payment
"Calculate January 2024 capitation for provider NPI 1234567890."

**Generates:**
- Member count by category (pediatric/adult/senior)
- Base PMPM x member months
- Risk adjustment amount
- Total payment

## Prior Authorization Scenarios

### Outpatient Imaging
"Create a prior auth request for an MRI of the lumbar spine."

**Generates:**
- 278 request with:
  - CPT: 72148 (MRI lumbar)
  - Diagnosis: M54.5 (Low back pain)
  - Review type: PROSPECTIVE

### Approval Response
"Approve the MRI auth for 1 unit valid for 30 days."

**Generates:**
- 278 response with:
  - Status: APPROVED
  - Approved units: 1
  - Effective dates