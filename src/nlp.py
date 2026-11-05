from dataclasses import dataclass


@dataclass(frozen=True)
class Analysis:
    topic: str
    intent: str
    sentiment: str


TOPIC_KEYWORDS = {
    "bullying_acoso": ("acoso", "hostig", "bullying", "maltrato", "amenaza"),
    "salud_mental": ("ansiedad", "depresion", "angustia", "suicidio", "salud mental"),
    "bienestar_docente": ("docente", "profesor", "clase", "reconocimiento", "estrés"),
    "convivencia": ("convivencia", "grupo", "respeto", "conflicto", "compañero"),
}


def analyze(text: str) -> Analysis:
    normalized = text.casefold()
    scores = {
        topic: sum(1 for keyword in keywords if keyword in normalized)
        for topic, keywords in TOPIC_KEYWORDS.items()
    }
    topic = max(scores, key=scores.get) if max(scores.values(), default=0) else "convivencia"
    intent = "pide_consejo" if any(word in normalized for word in ("qué hago", "ayuda", "cómo", "orient")) else "comparte_situacion"
    sentiment = "negativo" if any(word in normalized for word in ("no", "nunca", "nadie", "mal", "triste", "cansad", "miedo", "dolor")) else "neutro"
    return Analysis(topic=topic, intent=intent, sentiment=sentiment)
