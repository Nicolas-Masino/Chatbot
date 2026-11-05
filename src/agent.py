import os
from openai import OpenAI
from .config import Settings
from .metrics import Metrics
from .rag import EvidenceStore
from .safety import assess_safety
from .tools import analizar_situacion, consultar_evidencia
from time import perf_counter


class ConversationalAgent:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings.from_env()
        self.store = EvidenceStore()
        self.history: list[dict] = []  # Historial en formato de mensajes de OpenAI
        self.metrics = Metrics()
        
        # Inicializar el cliente de OpenAI (toma OPENAI_API_KEY del entorno)
        #self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.client = OpenAI(
            base_url="https://ollama.com/v1",
            api_key=self.settings.api_key,
        )

    def respond(self, message: str, model: str) -> str:
        started_at = perf_counter()
        self.model = model 
        print(f"Usando modelo: {self.model}")
        
        # 1. Validación de seguridad (Guardrail prioritario ante riesgo urgente)
        safety = assess_safety(message)
        if safety.level == "urgent":
            response = safety.response or "Buscá ayuda humana inmediata y comunicate con emergencias."
            # Guardar en historial
            self.history.append({"role": "user", "content": message})
            self.history.append({"role": "assistant", "content": response})
            self.metrics.observe(started_at, urgent=True, evidence_hits=0)
            return response

        # 2. Ejecutar herramientas y análisis NLP local
        analysis = analizar_situacion(message)
        evidence = consultar_evidencia(message, self.store)

        # 3. Preparar el contexto de la evidencia para el LLM
        evidence_text = ""
        if evidence:
            evidence_text = "Evidencia institucional disponible para incluir y citar:\n" + "\n".join(
                f"- Título: {item['title']} | Fuente: {item['source']}" for item in evidence
            )
        else:
            evidence_text = "No se encontró evidencia local específica para este mensaje. No inventes cifras ni fuentes oficiales."

        # 4. Construir el System Prompt ético y guía para el modelo
        system_prompt = f"""
        Eres "Voces que Importan", un agente conversacional de apoyo y orientación para estudiantes y docentes universitarios.
        El análisis preliminar detectó el eje temático: **{analysis['topic']}** con intención de **{analysis['intent']}**.

        REGLAS DE ORO ESTRICTAS QUE DEBES CUMPLIR:
        1. NUNCA diagnostiques condiciones médicas, psicológicas o psiquiátricas.
        2. Valida la emoción del usuario con absoluta empatía y tono humano.
        3. Si utilizas información de la evidencia provista a continuación, DEBES citar la fuente explícitamente (ej. [UNESCO-IESALC]). No inventes datos ni estadísticas.
        4. Orienta de forma constructiva hacia canales institucionales o pasos seguros.

        {evidence_text}
        """

        # 5. Armar la estructura de mensajes para la API (Sistema + Historial + Mensaje actual)
        messages = [{"role": "system", "content": system_prompt}]
        
        # Agregar los últimos turnos del historial para mantener memoria corta conversacional
        messages.extend(self.history[-6:])  # Mantiene los últimos 3 pares de mensajes
        
        # Agregar el mensaje actual del usuario
        messages.append({"role": "user", "content": message})

        try:
            # 6. Llamada oficial a la API de OpenAI
            completion = self.client.chat.completions.create(
                model=self.settings.model,  
                messages=messages,
                temperature=0.3      # Temperatura baja para mantener respuestas controladas y basadas en hechos
            )
            response = completion.choices[0].message.content

        except Exception as e:
            response = f"Disculpáme, ocurrió un error al comunicarme con el servicio de IA. Por favor, intentá nuevamente en unos instantes."

        # 7. Actualizar historial de la sesión y métricas
        self.history.append({"role": "user", "content": message})
        self.history.append({"role": "assistant", "content": response})
        self.metrics.observe(started_at, urgent=False, evidence_hits=len(evidence))

        return response