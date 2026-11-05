from dataclasses import dataclass
from time import perf_counter


@dataclass
class Metrics:
    messages: int = 0
    urgent_messages: int = 0
    evidence_hits: int = 0
    total_latency_ms: float = 0.0

    def observe(self, started_at: float, *, urgent: bool, evidence_hits: int) -> None:
        self.messages += 1
        self.urgent_messages += int(urgent)
        self.evidence_hits += evidence_hits
        self.total_latency_ms += (perf_counter() - started_at) * 1000

    @property
    def average_latency_ms(self) -> float:
        return self.total_latency_ms / self.messages if self.messages else 0.0
