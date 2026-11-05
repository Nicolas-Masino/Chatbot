import chainlit as cl
from src.agent import ConversationalAgent


@cl.on_chat_start
async def start() -> None:
    cl.user_session.set("agent", ConversationalAgent())
    model_mode = cl.Mode(
        id="model",
        name="Model",
        options=[
            cl.ModeOption(id="gpt-4o-mini", name="GPT-4 Mini", icon="brain", description="Mayor capacidad"),
            cl.ModeOption(id="mistral", name="Mistral", icon="bolt", default=True, description="Más rápido y local"),
        ]
    )
    await cl.Message(
        content=(
            "¡Hola! Soy **Voces que Importan**, un espacio de escucha y orientación "
            "sobre bienestar docente y convivencia universitaria.\n\n"
            "¿Cómo te sentís hoy o sobre qué situación te gustaría conversar?"
        )   
    ).send()
    await cl.context.emitter.set_modes([model_mode])



@cl.on_message
async def main(msg: cl.Message) -> None:
    agent = cl.user_session.get("agent")
    if not isinstance(agent, ConversationalAgent):
        raise RuntimeError("No se pudo inicializar la sesión del agente.")
    await cl.Message(content=agent.respond(msg.content, model=msg.modes.get("model"))).send()
