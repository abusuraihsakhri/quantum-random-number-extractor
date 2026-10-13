# Quantum Random Number Extractor

### [Open the Live Application →](https://abusuraihsakhri.github.io/quantum-random-number-extractor/)

A local-first workbench for **binary measurement streams**. It demonstrates the classical **von Neumann extractor** and reports elementary input/output bias statistics. It also retains the repository's earlier generic threshold-audit and batch-processing features.

## Browser workbench

Paste a string of binary outcomes, or import a plain-text file containing 0 and 1 symbols separated by whitespace, commas, semicolons, or vertical bars. Select **Extract bits** to see the output, input/output bit frequencies, discarded pairs, and descriptive empirical min-entropy values. Export the extracted bits as a text file.

You can generate a **synthetic biased Bernoulli stream** to explore the extractor. This is not a physical or quantum entropy source. Uploads, calculation and exports run **entirely inside the browser tab**; the GitHub Pages application does not send observations to a server. A modern JavaScript-enabled browser is sufficient; the optional simulation additionally needs Web Crypto.

### Extraction rule

| Input pair | Output |
| --- | --- |
| `01` | `0` |
| `10` | `1` |
| `00`, `11` | Discard |

Nonoverlapping pairs are processed left-to-right. An odd final input bit is unused. For example, `01 10 00 11 01` produces `010`.

**Scientific limitation:** This rule removes fixed bias for independent, identically distributed Bernoulli trials. It does not remove arbitrary correlations, verify source provenance, certify cryptographic unpredictability or implement a full **NIST SP 800-90B** entropy-source assessment. The displayed min-entropy statistic `-log2(max(p(0), p(1)))` is a *plug-in descriptive estimate*, not a statistically conservative entropy lower bound. **Do not use experimental output for production key generation.**

## Python installation and CLI

Python 3.9 or newer is required. From a clone of this repository:

```bash
python -m pip install .
# Extract from a UTF-8 text file; saves plain 0/1 output
quantum-random-number-extractor extract -i observations.txt -o extracted-bits.txt
# Output to the terminal instead:
python -m qrng_entropy.cli extract -i observations.txt
```

Inputs must contain at least two observations, with a maximum of 1,000,000 bits (4 MiB text-file limit). Invalid symbols are rejected rather than silently removed. The core extractor requires only Python's standard library.

The **legacy task-audit CLI** remains available:

```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2
python cli.py batch -i sample.csv -o results.csv
python cli.py verify-audit
python cli.py chat "What is the system status?"
```

The legacy `audit` and `batch` commands classify generic metrics using fixed heuristic thresholds; they **do not calculate quantum entropy or demonstrate NIST conformance**. The `enrichment.py` features are similarly illustrative threshold checks.

## Optional local API

```bash
python -m pip install ".[web]"
python cli.py serve --host 127.0.0.1 --port 8000
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to use the same browser workbench. The API also exposes:

- `POST /api/extract` — JSON payload `{"bits":"0110001101"}`; returns extraction results
- `POST /api/audit`, `POST /api/chat`, `GET /api/audit/logs`, `GET /metrics`, `GET /health` — preserved legacy task-audit operations
- `/docs` — interactive FastAPI API reference

Use the API only on a trusted network unless you add authentication and deployment-specific access controls. Submitting to an API does transmit that data to its host; the standalone GitHub Pages workbench **does not use the API**.

## Audit trail and security scope

The legacy task supervisor signs in-memory log entries with HMAC-SHA256 and verifies both record signatures and chain continuity. Configure a unique `AUDIT_SECRET_KEY` through the deployment environment; without it, a random ephemeral key is generated. Logs are **not persisted or externally anchored** and cannot detect removal of a final log suffix across process restarts. The repository includes regex-based identifier screening, but this is **not a complete PHI de-identification or compliance system**. Do not submit sensitive records to the public application or unauthenticated API endpoints.

## Development and checks

```bash
python -m pip install ".[web,dev]"
python -m pytest -q
node --test tests/web.test.cjs
python -m compileall -q agents qrng_entropy
```

The static site is served from `web/` by GitHub Pages Actions, with no backend and no Pyodide dependency. The Python service is optional. CI runs Python tests on several Python versions and JavaScript extractor tests with Node.js.

## License

[MIT](LICENSE).
