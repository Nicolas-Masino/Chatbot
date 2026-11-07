from dataclasses import asdict
from .config import Settings
from .rag import EvidenceStore
from .nlp import analyze
from .resources import verified_resources


async def analizar_situacion(text: str) -> dict:
    return await analyze(text)


def consultar_evidencia(text: str, store: EvidenceStore | None = None) -> list[dict]:
    evidence = (store or EvidenceStore()).search(text)
    return [{"title": item.title, "text": item.text, "source": item.source} for item in evidence]


def orientar_recursos(settings: Settings | None = None) -> list[dict]:
    return [asdict(resource) for resource in verified_resources(settings or Settings.from_env())]
