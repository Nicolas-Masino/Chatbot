# Voces que Importan

Prototipo Chainlit de orientación para estudiantes y docentes sobre convivencia
universitaria, bienestar docente, bullying/acoso y salud mental/prevención.

## Alcance y seguridad

El agente informa, acompaña y deriva; no diagnostica, no determina culpabilidad y
no reemplaza atención clínica, institucional ni de emergencias. Ante señales de
peligro inmediato interrumpe el flujo normal y recomienda ayuda humana. Los canales
de la universidad se configuran con variables de entorno y no se inventan.

## Ejecutar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
chainlit run app.py
```

El comando anterior inicia la aplicación sin recarga automática, que evita
errores de compatibilidad del watcher con Python 3.14. Si necesitas recarga
automática durante el desarrollo, puedes probar `chainlit run app.py -w`.

El modo `LLM_PROVIDER=demo` funciona sin credenciales y permite probar el flujo,
el RAG local y los guardrails. El adaptador de modelo está desacoplado para agregar
un proveedor posteriormente sin modificar la interfaz Chainlit.

## Evaluación

```bash
pytest -q
```

La carpeta `data/sources/` contiene fuentes resumidas con URL para que cada respuesta
pueda citar evidencia. Antes de una demostración real deben verificarse vigencia,
jurisdicción y canales oficiales. La prueba urgente incluida usa un caso ficticio.

Para la defensa, conservar capturas o un video de una ejecución demo como plan B si
falla la conexión.


# Requerimientos 
Las ultimas versiones de Python pueden generar comportamientos inesperados en Chainlit. El proyecto actual corre con Python 3.12