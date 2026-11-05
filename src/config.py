from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    provider: str = "demo"
    model: str = ""
    api_key: str = ""
    university_name: str = "Tu universidad"
    convivencia_url: str = ""
    wellbeing_url: str = ""
    emergency_phone: str = ""

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            provider=os.getenv("LLM_PROVIDER", "demo").lower(),
            model=os.getenv("LLM_MODEL", ""),
            api_key=os.getenv("LLM_API_KEY", ""),
            university_name=os.getenv("UNIVERSITY_NAME", "Tu universidad"),
            convivencia_url=os.getenv("UNIVERSITY_CONVIVENCIA_URL", ""),
            wellbeing_url=os.getenv("UNIVERSITY_WELLBEING_URL", ""),
            emergency_phone=os.getenv("UNIVERSITY_EMERGENCY_PHONE", ""),
        )
