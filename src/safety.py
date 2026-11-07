from dataclasses import dataclass
import re

@dataclass(frozen=True)
class SafetyResult:
    level: str
    reason: str
    response: str | None = None


_URGENT_PATTERNS = (
    r"\bno (?:quiero|quiere) seguir viviendo\b",
    r"\bme quiero suicidar\b",
    r"\bse quiere suicidar\b",
    r"\bse quiere matar\b",
    r"\bme quiero matar\b",
    r"\bpeligro inmediato\b",
)

def safety_from_llm(analysis: dict) -> SafetyResult:
    if analysis["intent"] == "emergencia":
        return SafetyResult(
            level="urgent",
            reason="llm_detected_emergency",
            response=(
                "Lo que contás puede implicar un riesgo inmediato. Si hay peligro, "
                "llamá ahora al 911 (Argentina) o a emergencias de tu localidad. "
                "No dejes sola a la persona: buscá a alguien de confianza o a un "
                "profesional y no prometas guardar el secreto. Decime en qué "
                "localidad estás para buscar un recurso oficial."
            ),
        )
    return SafetyResult(level="normal", reason="llm_no_emergency_detected")

def safety_from_re(text: str) -> SafetyResult:
    normalized = text.casefold()
    if any(re.search(pattern, normalized) for pattern in _URGENT_PATTERNS):
        return SafetyResult(
            level="urgent",
            reason="possible_immediate_danger",
            response=(
                "Lo que contás puede implicar un riesgo inmediato. Si hay peligro, "
                "llamá ahora al 911 (Argentina) o a emergencias de tu localidad. "
                "No dejes sola a la persona: buscá a alguien de confianza o a un "
                "profesional y no prometas guardar el secreto. Decime en qué "
                "localidad estás para buscar un recurso oficial."
            ),
        )
    return SafetyResult(level="normal", reason="no_urgent_signal")

def assess_safety(from_re, from_llm) -> SafetyResult:
    if from_re.level == "urgent":
        return from_re
    if from_llm.level == "urgent":
        return from_llm
    return SafetyResult(level="normal", reason="no_urgent_signal")
