from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class Evidence:
    title: str
    text: str
    source: str


class EvidenceStore:
    def __init__(self, source_dir: str = "data/sources") -> None:
        self.documents = self._load(Path(source_dir))

    @staticmethod
    def _load(source_dir: Path) -> list[Evidence]:
        if not source_dir.exists():
            return []
        documents = []
        for path in sorted(source_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            source = text.split("Fuente:", 1)[-1].strip() if "Fuente:" in text else path.name
            documents.append(Evidence(path.stem, text, source))
        return documents

    def search(self, query: str, limit: int = 2) -> list[Evidence]:
        terms = set(re.findall(r"\w+", query.casefold()))
        ranked = sorted(
            self.documents,
            key=lambda doc: len(terms & set(re.findall(r"\w+", doc.text.casefold()))),
            reverse=True,
        )
        return [doc for doc in ranked[:limit] if terms & set(re.findall(r"\w+", doc.text.casefold()))]
