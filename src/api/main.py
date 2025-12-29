"""
AUTOHELIX: Interface Layer (FastAPI)
Exposes the Quantum Optimizer and Streaming Data via REST.
"""

from contextlib import asynccontextmanager
from typing import Dict

from fastapi import FastAPI

from src.quantum.qaoa_circuits import AutoHelixQAOA
from src.streaming.telemetry_producer import TelemetryGenerator

# Global state for the demo
telemetry_log = []
generator = TelemetryGenerator()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Quantum Kernel
    print("✓ AUTOHELIX API: Connected to Quantum Kernel")
    yield
    # Shutdown
    print("✓ AUTOHELIX API: Shutting down")


app = FastAPI(title="AutoHelix Interface", lifespan=lifespan)


@app.get("/")
def health_check():
    return {"status": "operational", "system": "AutoHelix", "node": "grandview-node-01"}


@app.get("/stream/live")
async def get_live_telemetry():
    """Fetch the latest generated events."""
    events = [generator.generate_event() for _ in range(5)]
    telemetry_log.extend(events)
    # Keep log small for memory
    if len(telemetry_log) > 100:
        telemetry_log.pop(0)
    return {"count": 5, "events": events}


@app.post("/optimize/recovery")
async def trigger_optimization(incident: Dict):
    """
    Trigger a Quantum Optimization for a specific incident.
    """
    # Extract graph from incident or use mock defaults
    services = incident.get("services", {"db": 5.0, "api": 2.0, "web": 1.0})
    dependencies = incident.get("dependencies", {"api": ["db"], "web": ["api"]})

    # Instantiate the Quantum Kernel
    qaoa = AutoHelixQAOA(n_qubits=len(services), steps=3, backend="local")

    # Run the optimization
    optimal_sequence = qaoa.run_optimization(dependencies, services)

    return {
        "incident_id": incident.get("id", "unknown"),
        "strategy": "QAOA_HYBRID",
        "optimal_sequence": optimal_sequence,
        "estimated_recovery_time": sum(services.values()),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
