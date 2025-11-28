# Payer Domain Knowledge

## Overview

Health plan (payer) operations involve managing member enrollment, processing claims, coordinating benefits, and ensuring quality care delivery.

## Key Concepts

### Members and Subscribers
- **Subscriber**: Primary policy holder who establishes coverage
- **Member**: Any person covered under a policy (subscriber + dependents)
- **Dependent**: Family member covered under subscriber's policy

### Coverage Types
- **Commercial**: Employer-sponsored or individual market plans
- **Medicare Advantage**: Private plans contracted with CMS for Medicare beneficiaries
- **Medicaid Managed Care**: State-contracted plans for Medicaid population
- **Dual Eligible**: Members with both Medicare and Medicaid

### Plan Types
- **HMO**: Health Maintenance Organization - requires PCP, referrals for specialists
- **PPO**: Preferred Provider Organization - flexible network, no referrals needed
- **EPO**: Exclusive Provider Organization - no out-of-network coverage except emergencies
- **POS**: Point of Service - HMO/PPO hybrid

## Cost Sharing

### Deductible
Amount member pays before plan begins paying. Can be individual or family level.

### Copay
Fixed dollar amount for specific services (e.g., $25 PCP visit).

### Coinsurance
Percentage of allowed amount member pays after deductible (e.g., 20% for specialist).

### Out-of-Pocket Maximum
Annual limit on member cost sharing. Once reached, plan pays 100%.

## Accumulators

Track member progress toward deductibles and OOP maximums:
- Individual deductible accumulator
- Family deductible accumulator
- Individual OOP accumulator
- Family OOP accumulator
