"""
AUTOHELIX: Telemetry Stream Generator
Generates synthetic infrastructure events for the MMH (Monitored Monetization Hub).
"""

import random
import time
import uuid
from datetime import datetime


class TelemetryGenerator:
    def __init__(self):
        self.services = [
            "payment-gateway",
            "order-processor",
            "inventory-db",
            "auth-service",
            "recommendation-engine",
        ]
        self.regions = ["us-east-1", "eu-central-1", "ap-northeast-1"]

    def generate_event(self):
        """Emit a single structured log event following NWU schema."""
        service = random.choice(self.services)
        event_type = random.choice(
            ["HEALTH_CHECK", "LATENCY_SPIKE", "SERVICE_FAILURE", "LIQUIDITY_TRANSFER"]
        )

        # Base schema
        event = {
            "log_id": str(uuid.uuid4()),
            "event_time": datetime.utcnow().isoformat() + "Z",
            "source_system": service,
            "region": random.choice(self.regions),
            "type": event_type,
            "schema_version": "1.0",
        }

        # Context-specific fields
        if event_type == "SERVICE_FAILURE":
            event["severity"] = "CRITICAL"
            event["dependencies"] = self._get_dependencies(service)
            event["estimated_downtime_cost"] = random.uniform(1000.0, 50000.0)

        elif event_type == "LIQUIDITY_TRANSFER":
            event["liquidity_score"] = round(random.uniform(0.1, 1.0), 2)
            event["asset_value_usd"] = round(random.uniform(10.0, 500.0), 2)
            event["reuse_count"] = random.randint(1, 100)

        return event

    def _get_dependencies(self, service):
        """Mock dependency graph."""
        graph = {
            "payment-gateway": ["auth-service"],
            "order-processor": ["payment-gateway", "inventory-db"],
            "recommendation-engine": ["inventory-db"],
            "inventory-db": [],
            "auth-service": [],
        }
        return graph.get(service, [])

    def stream(self, interval=0.5):
        """Infinite generator for streaming."""
        while True:
            yield self.generate_event()
            time.sleep(interval)
