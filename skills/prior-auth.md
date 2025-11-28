# Prior Authorization

## Overview

Prior authorization (PA) is a utilization management process requiring approval before certain services are rendered.

## Services Requiring PA

### Common Categories
- Inpatient admissions (elective)
- Advanced imaging (MRI, CT, PET)
- Specialty medications
- DME (motorized wheelchairs, CPAP)
- Home health services
- Skilled nursing facility stays
- Behavioral health (residential, PHP)
- Surgical procedures (certain)
- Genetic testing

### Clinical Criteria
Authorization decisions based on:
- Medical necessity
- Appropriate level of care
- Evidence-based guidelines (MCG, InterQual)
- Plan-specific policies

## Authorization Workflow

### 1. Request Submission
- X12 278 transaction
- Portal submission
- Phone/fax (legacy)

**Required Information:**
- Member demographics
- Provider information
- Diagnosis codes
- Procedure/service codes
- Clinical documentation

### 2. Clinical Review
- Nurse reviewer initial assessment
- Medical director review (if not meeting criteria)
- Peer-to-peer available

### 3. Decision
- **Approved**: Service authorized
- **Denied**: Not medically necessary (with reason)
- **Pended**: Need additional information
- **Partial**: Some units/days approved

### 4. Communication
- X12 278 response
- Portal notification
- Letter to member/provider

## Timelines

### Urgent/Expedited
- Decision within 24-72 hours
- Used when delay could harm member

### Standard (Non-urgent)
- Decision within 14 calendar days
- Extension possible with notification

### Retrospective
- Review after service rendered
- Limited timeframe for submission (varies by plan)

## Authorization Elements

- Authorization number
- Effective dates
- Approved units/visits/days
- Approved facility/provider
- Diagnosis and procedure codes
- Expiration date

## Concurrent Review

Ongoing review during treatment:
- Inpatient stays
- Home health episodes
- Behavioral health treatment
- Additional days/units requested

## Appeals

Member/provider right to appeal denial:
- Level 1: Internal review
- Level 2: External review (IRO)
- Expedited appeal for urgent situations
