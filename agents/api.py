"""
FastAPI REST API Server for Quantum Random Number Extractor.
"""
from typing import Dict, Any, List\nfrom pathlib import Path
from fastapi import FastAPI, HTTPException\nfrom fastapi.responses import FileResponse
from pydantic import BaseModel
from .base import AuditLogger, PHIGuard\nfrom qrng_entropy.extractor import extract_bits
from .models import SystemTaskPayload, ConsensusDossier
from .supervisor import SystemSupervisor

supervisor = SystemSupervisor(model_provider="mock")

app = FastAPI(
    title="Quantum Random Number Extractor API",
    description="Enterprise Distributed Component Platform (Post-Quantum Cryptography & Hardware Security)",
    version="3.0.0-ENTERPRISE",
)


class ExtractRequest(BaseModel):
    bits: str


WEB_DIR = Path(__file__).resolve().parent.parent / "web"


@app.get("/", include_in_schema=False)
def web_home():
    return FileResponse(WEB_DIR / "index.html")


@app.get("/extractor.js", include_in_schema=False)
def web_script():
    return FileResponse(WEB_DIR / "extractor.js")


@app.post("/api/extract")
def api_extract(payload: ExtractRequest):
    try:
        return extract_bits(payload.bits)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


class ChatRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "HEALTHY", "service": "quantum-random-number-extractor", "domain": "Post-Quantum Cryptography & Hardware Security", "standard": "NIST FIPS 203/204/205 / ISO/IEC 17825 Standards", "version": "3.0.0-ENTERPRISE"}


@app.get("/metrics")
def metrics():
    return {
        "dossiers_processed_total": len(supervisor.dossier_registry),
        "audit_blocks_total": len(AuditLogger.get_trail()),
        "system_status": "NOMINAL_OPTIMAL"
    }


@app.post("/api/audit")
def api_audit(payload: SystemTaskPayload):
    dossier = supervisor.process_task(payload)
    return dossier.to_dict()


@app.post("/api/chat")
def api_chat(req: ChatRequest):
    try:
        ans = supervisor.query_supervisory_chat(req.query)
        return {"response": ans}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/audit/logs")
def api_audit_logs():
    return {"audit_trail": AuditLogger.get_trail(), "verified": AuditLogger.verify_integrity()}
