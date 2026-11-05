from dataclasses import dataclass
from .config import Settings


@dataclass(frozen=True)
class Resource:
    name: str
    description: str
    url: str
    scope: str


def verified_resources(settings: Settings) -> list[Resource]:
    resources = [
        Resource("Línea 135", "Asistencia en crisis de la Ciudad de Buenos Aires y Gran Buenos Aires.", "https://www.asistenciaalsuicida.org.ar/", "Argentina"),
        Resource("Línea 0800-345-1435", "Centro de Asistencia al Suicida para otras localidades.", "https://www.asistenciaalsuicida.org.ar/", "Argentina"),
    ]
    if settings.convivencia_url:
        resources.append(Resource("Canal de convivencia institucional", settings.university_name, settings.convivencia_url, "Universidad"))
    if settings.wellbeing_url:
        resources.append(Resource("Bienestar y acompañamiento institucional", settings.university_name, settings.wellbeing_url, "Universidad"))
    return resources
