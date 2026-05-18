from src.utils.llm import ask_llm


def generate_answer(question, data, context="", return_usage=False):
    analyst_prompt = """
    Eres el Administrador Senior de Heladerias Madel.
    Tu trabajo es interpretar los datos de la base de datos y dar una respuesta estrategica.

    REGLAS:
    1. Si el dato es 0 o vacio, explica que no hay registros actuales, no digas simplemente "hay 0".
    2. Si los datos muestran stock bajo, actua como analista y recomienda hacer un pedido.
    3. Si hay datos historicos de ventas, entrega una recomendacion operativa concreta.
    4. Responde siempre en Espanol de forma profesional y amable.
    5. Si recibiste un error de la base de datos, traducelo a algo que el usuario entienda.
    6. No inventes datos. Si falta informacion, dilo claramente.
    7. Considera contexto chileno: diciembre, enero y febrero corresponden a verano/temporada alta para heladerias.
    """

    prompt_usuario = f"""
    Contexto recuperado:
    {context}

    Pregunta del usuario: {question}
    Datos obtenidos de la DB: {data}

    Por favor, analiza estos datos y responde a la pregunta.
    """

    return ask_llm(
        analyst_prompt,
        prompt_usuario,
        temperature=0.4,
        max_tokens=650,
        return_usage=return_usage,
    )
