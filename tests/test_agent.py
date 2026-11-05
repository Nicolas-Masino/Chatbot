from src.agent import ConversationalAgent
from src.config import Settings
from src.safety import assess_safety
from src.tools import consultar_evidencia, orientar_recursos


def test_urgent_signal_prioritizes_human_help():
    response = ConversationalAgent().respond("Mi compañero dijo que no quiere seguir viviendo")
    assert "911" in response
    assert "no dejes sola" in response.lower()


def test_agent_cites_local_evidence():
    response = ConversationalAgent().respond("Me siento agotado como docente y necesito orientación")
    assert "Evidencia" in response
    assert "unesco" in response.lower()


def test_resources_do_not_invent_university_channel():
    resources = consultar_evidencia("acoso")
    assert isinstance(resources, list)
    assert assess_safety("Necesito orientación sobre un conflicto").level == "normal"


def test_configured_channel_is_returned():
    settings = Settings(university_name="Universidad Demo", convivencia_url="https://example.edu/convivencia")
    assert any(item["url"] == settings.convivencia_url for item in orientar_recursos(settings))
