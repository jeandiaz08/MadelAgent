from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(question, data):
    analyst_prompt = """
    Eres el Administrador Senior de Heladerías Madel. 
    Tu trabajo es interpretar los datos de la base de datos y dar una respuesta estratégica.
    
    REGLAS:
    1. Si el dato es 0 o vacío, explica que no hay registros actuales, no digas simplemente "hay 0".
    2. Si los datos muestran stock bajo, actúa como analista y recomienda hacer un pedido.
    3. Responde siempre en Español de forma profesional y amable.
    4. Si recibiste un error de la base de datos, tradúcelo a algo que el usuario entienda.
    """

    prompt_usuario = f"""
    Pregunta del usuario: {question}
    Datos obtenidos de la DB: {data}
    
    Por favor, analiza estos datos y responde a la pregunta.
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": analyst_prompt},
            {"role": "user", "content": prompt_usuario}
        ],
        temperature=0.4 
    )

    return completion.choices[0].message.content