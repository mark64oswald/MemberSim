# Claims Processing

## Overview

Claims processing is the core operational function of health plans - receiving, adjudicating, and paying healthcare claims.

## Claim Types

### Professional (CMS-1500 / 837P)
- Physician services
- Outpatient therapy
- Diagnostic testing
- DME (Durable Medical Equipment)

### Institutional (UB-04 / 837I)
- Inpatient hospital stays
- Outpatient hospital services
- Skilled nursing facility
- Home health

### Dental (ADA / 837D)
- Preventive services
- Basic restorative
- Major restorative
- Orthodontia

### Pharmacy
- Retail pharmacy claims
- Mail order
- Specialty pharmacy

## Adjudication Process

### 1. Receipt and Validation
- EDI syntax validation
- Required field checks
- Provider enrollment verification

### 2. Eligibility Verification
- Member active on date of service
- Correct plan/group assignment
- COB (Coordination of Benefits) check

### 3. Benefit Application
- Service covered under plan
- Prior authorization check
- Medical necessity (if applicable)

### 4. Pricing
- Fee schedule lookup
- Allowed amount calculation
- Network status determination

### 5. Cost Sharing
- Apply deductible
- Calculate copay/coinsurance
- Check OOP maximum

### 6. Payment Determination
- Calculate plan payment
- Generate 835 remittance
- Update accumulators

## Claim Statuses

- **Received**: Claim in system
- **Pending**: Awaiting information or review
- **Approved**: Adjudicated for payment
- **Denied**: Not payable (with reason code)
- **Paid**: Payment issued

## Adjustment Reason Codes (CARC)

Common codes:
- 1: Deductible amount
- 2: Coinsurance amount
- 3: Copay amount
- 4: Procedure code inconsistent with modifier
- 16: Missing information
- 18: Duplicate claim
- 45: Exceeds fee schedule
- 50: Non-covered service
- 96: Non-covered charge
- 97: Payment adjusted (already paid)

## Remark Codes (RARC)

Provide additional explanation:
- N30: Missing diagnosis
- N362: Missing/invalid service facility
- M15: Separately billed services included
