# MemberSim Demos

Interactive demonstrations of MemberSim capabilities for payer system testing.

## Available Demos

### [Claims Processing Demo](claims-processing/README.md)

Comprehensive guide to generating and testing healthcare claims.

**What you'll learn:**
- Generate realistic professional and institutional claims
- X12 837P/837I transaction generation and structure
- Claims adjudication and payment testing
- Denial scenarios with CARC/RARC codes
- Coordination of benefits (COB) testing
- Batch generation for load testing

**Key scenarios covered:**
- Professional claims (office visits, labs, specialists)
- Institutional claims (hospital stays, procedures)
- Denial management workflows
- Primary/secondary payer coordination

---

### Enrollment Demo (Coming Soon)

Member enrollment workflows and X12 834 transaction generation.

**Planned content:**
- New member enrollment processing
- Open enrollment and qualifying life events
- Dependent adds and removes
- X12 834 transaction structure
- COBRA enrollment scenarios
- Plan change and transfer workflows

---

### Quality Measures Demo (Coming Soon)

HEDIS care gap generation and quality measure testing.

**Planned content:**
- HEDIS measure definitions and logic
- Care gap generation with configurable rates
- Gap closure evidence tracking
- Measure status reporting
- Population health analytics
- Star ratings integration

---

### Eligibility Demo (Coming Soon)

Real-time eligibility verification with X12 270/271.

**Planned content:**
- X12 270 eligibility inquiry generation
- X12 271 eligibility response handling
- Coverage verification scenarios
- Benefit detail responses
- Network status verification

---

### Prior Authorization Demo (Coming Soon)

Authorization request and response workflows.

**Planned content:**
- X12 278 request/response generation
- Authorization decision scenarios
- Utilization management testing
- Service type authorization
- Medical necessity documentation

---

## Demo Categories

| Category | Description | Status |
|----------|-------------|--------|
| **Claims** | Claims processing, adjudication, denials | Available |
| **Enrollment** | Member enrollment and X12 834 | Coming Soon |
| **Quality** | HEDIS measures and care gaps | Coming Soon |
| **Eligibility** | Real-time verification (270/271) | Coming Soon |
| **Authorization** | Prior auth workflows (278) | Coming Soon |
| **Integration** | System integration examples | Coming Soon |

## Running Demos

Each demo is self-contained with setup instructions:

```bash
# Navigate to demo directory
cd demos/<demo-name>

# Read the README for detailed instructions
cat README.md

# Run example scripts (if provided)
python example.py
```

## Prerequisites

All demos require MemberSim to be installed:

```bash
# Clone and install
git clone https://github.com/mark64oswald/MemberSim.git
cd MemberSim
pip install -e ".[dev]"
```

## Quick Links

- **[Main README](../README.md)** - Project overview and quick start
- **[API Reference](../docs/api.md)** - Complete Python API documentation
- **[Examples](../examples/)** - Code examples and scripts
- **[Skills](../skills/)** - Claude project knowledge files

## Contributing

Want to add a demo? We welcome contributions:

1. Create a new directory under `demos/`
2. Add a comprehensive `README.md` following the claims-processing pattern
3. Include working code examples
4. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## Support

- **Issues:** [GitHub Issues](https://github.com/mark64oswald/MemberSim/issues)
- **Discussions:** [GitHub Discussions](https://github.com/mark64oswald/MemberSim/discussions)
- **Documentation:** [docs/](../docs/)
