# Quantum Random Number Extractor

> **Domain:** Post-Quantum Cryptography & Zero-Knowledge Architecture
> **Reference Guidelines & Standards:** `NIST FIPS 203/204/205, NIST SP 800-90B & ISO/IEC Standards`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**Quantum Random Number Extractor** is an advanced analytical and computational platform implementing NIST SP 800-90B physical quantum entropy source & min-entropy estimation. It provides a multi-agent evaluation pipeline that processes task payloads through specialized workers to generate consensus dossiers with cryptographic audit trails.

---

## ⚙️ Key Capabilities & Algorithmic Modules

- **Multi-Agent Evaluation Pipeline**: Three specialized workers (InvariantQC, SafetyEscalation, ProtocolConformance) analyze task payloads
- **Deterministic Calculation Engine**: Strict compliance with standard reference formulations and thresholds
- **Risk & Urgency Classification**: Multi-tier categorization (ROUTINE, ELEVATED, CRITICAL_STAT) with automated action recommendations
- **Validation & Guardrails**: Rigorous input bounds checking and anomaly detection
- **HMAC-SHA256 Audit Trail**: Cryptographically chained, tamper-evident logging
- **Zero-PHI Outbound Interceptor**: Active regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers

---

## 💻 Installation

```bash
# Core functionality
pip install .

# With web API support
pip install ".[web]"

# With development dependencies
pip install ".[dev]"
```

---

## 💻 CLI Quickstart & Usage

### 1. Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. Batch Processing
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 3. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 4. Chat Query
```bash
python cli.py chat "What is the system status?"
```

### 5. Start API Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Parameter Reference
| Parameter | Description | Default |
|:----------|:------------|:--------|
| `--task-id` | Unique task identifier | TASK-2026-001 |
| `--target` | Target identifier | KEY-TARGET-01 |
| `--primary` | Primary metric (float) | 28.5 |
| `--secondary` | Secondary metric (float) | 14.2 |
| `--critical` | Flag critical status | False |
| `--status` | Status descriptor | DISCORDANT |
| `-i, --input` | Input CSV file (batch) | required |
| `-o, --output` | Output CSV file (batch) | results.csv |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition. Set `AUDIT_SECRET_KEY` environment variable for persistent keys across restarts.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances (`llama3`, `mistral`), Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **Active Learning Bayesian Calibration:** Dynamic tracker updating worker reliability weights and monitoring Brier calibration drift.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 100
```

Run batch CLI with sample data:

```bash
python cli.py batch -i sample.csv -o results.csv
```

---

## 🐳 Container Deployment

```bash
docker build -t quantum-random-number-extractor .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY=your-secret-key quantum-random-number-extractor
```

Or using Docker Compose:

```bash
docker-compose up -d
```

---

## 📁 Project Structure

```
quantum-random-number-extractor/
├── agents/                  # Core agent modules (supervisor, workers, LLM, metrics)
│   ├── api.py              # FastAPI REST endpoints
│   ├── base.py             # Security guards, PHI protection, audit trail
│   ├── models.py           # Pydantic data models with validation
│   ├── supervisor.py       # Master orchestrator
│   ├── workers.py          # Specialized evaluation workers
│   └── ...
├── qrng_entropy/           # QRNG entropy estimation sub-package
│   ├── agents.py           # Entropy-specific agents (SP800-90B, Markov, HMAC-DRBG)
│   ├── engine.py           # Core algorithmic engine
│   ├── cli.py              # QRNG-specific CLI
│   └── server.py           # FastAPI server factory
├── tests/                  # Test suite
├── cli.py                  # Main CLI entry point
├── simulator.py            # Batch simulation tool
├── enrichment.py           # Enrichment feature engines
├── web/index.html          # Operations console UI
├── Dockerfile
└── docker-compose.yml
```

---

## 🔒 Security Notes

- **Audit Key**: Set `AUDIT_SECRET_KEY` environment variable in production. Without it, an ephemeral key is generated (with a warning) and audit integrity is not preserved across restarts.
- **Input Validation**: All metric values are validated to be finite (no NaN/Inf). Identifier fields must be non-empty.
- **PHI Protection**: All outbound data is inspected for PHI patterns (SSN, MRN, phone, email, patient names).
