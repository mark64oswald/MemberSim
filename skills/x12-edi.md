# X12 EDI Transactions

## Overview

X12 is the standard for electronic data interchange in US healthcare. Key transactions for payer operations:

## Transaction Types

### 834 - Benefit Enrollment
Communicates enrollment information from employer/sponsor to health plan.

**Key Segments:**
- ISA: Interchange control header
- GS: Functional group header
- ST: Transaction set header
- BGN: Beginning segment
- N1: Party identification (sponsor, payer)
- INS: Member level detail
- REF: Reference information
- DTP: Date/time periods
- NM1: Individual name
- DMG: Demographics
- HD: Health coverage
- SE/GE/IEA: Trailers

### 837P - Professional Claim
Healthcare claim from professional provider (physician, therapist, etc.).

**Key Segments:**
- BHT: Beginning of hierarchical transaction
- NM1: Names (billing provider, subscriber, patient)
- CLM: Claim information
- DTP: Service dates
- SV1: Professional service line
- DX: Diagnosis codes

### 837I - Institutional Claim
Healthcare claim from institutional provider (hospital, SNF, etc.).

**Key Segments:**
- Similar to 837P but with:
- SV2: Institutional service line
- CL1: Institutional claim code

### 835 - Remittance Advice
Payment information from payer to provider.

**Key Segments:**
- BPR: Financial information
- TRN: Trace number
- CLP: Claim payment information
- SVC: Service payment information
- CAS: Claim adjustment

### 278 - Prior Authorization
Request and response for service authorization.

**Key Segments:**
- BHT: Beginning segment
- UM: Health care services review
- HI: Health care information codes
- HSD: Health care services delivery

### 270/271 - Eligibility
Inquiry (270) and response (271) for member eligibility.

**Key Segments:**
- BHT: Beginning segment
- EB: Eligibility or benefit information
- DTP: Eligibility dates

## Control Numbers

- ISA13: Interchange control number (9 digits)
- GS06: Group control number (1-9 digits)
- ST02: Transaction set control number (4-9 digits)

## Delimiters

Standard delimiters:
- Element: * (asterisk)
- Segment: ~ (tilde)
- Sub-element: : (colon)
