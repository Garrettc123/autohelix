from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AUTOHELIX",
    description="Quantum-Hybrid AI Infrastructure for Self-Healing Systems & Real-Time Data Liquidity Markets",
    version="1.0.0",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/")
def root():
    return {
        "system": "AUTOHELIX",
        "version": "1.0.0",
        "status": "operational",
        "author": "Garrett Carrol",
        "organization": "Garcar Enterprise",
        "capabilities": [
            "quantum-hybrid-compute",
            "self-healing-infrastructure",
            "real-time-data-liquidity",
            "formal-verification",
            "autonomous-repair",
        ],
    }


@app.get("/health")
def health():
    return {"status": "healthy", "system": "AUTOHELIX"}
