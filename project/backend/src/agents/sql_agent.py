from src.utils.prompts import RAG_SYSTEM_PROMPT
from src.utils.llm import ask_llm
from src.retrieval.retrieval import run_sql
from src.generate.generate import generate_answer

def run_agent(question: str):
    sql_query = ask_llm(RAG_SYSTEM_PROMPT, question)

    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    print(f"\nSQL generado: {sql_query}")

    if not sql_query.upper().startswith("SELECT"):
        return generate_answer(question, f"Error: El sistema no pudo generar una consulta válida. Respuesta del modelo: {sql_query}")

    try:
        result = run_sql(sql_query)
        print(f"Resultado DB: {result}")
        
    except Exception as e:

        print(f"Error de ejecución SQL: {e}")
        result = f"Error de base de datos: {str(e)}"

    final_answer = generate_answer(question, result)

    return final_answer