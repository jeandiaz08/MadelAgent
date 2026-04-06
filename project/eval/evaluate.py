import json
import os
from groq import Groq
from dotenv import load_dotenv
from src.agents.sql_agent import run_agent

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def llm_judge(question, expected, response):
    """
    Usa a la IA como juez para evaluar si la respuesta es correcta por contexto,
    no por coincidencia exacta de texto.
    """
    prompt = f"""
    Eres un juez estricto pero justo evaluando a un asistente de base de datos.
    
    Pregunta del usuario: "{question}"
    Lo que se esperaba que respondiera (concepto o dato): "{expected}"
    Respuesta real del asistente: "{response}"

    Tu tarea: ¿La respuesta real del asistente responde a la pregunta y contiene la información o el concepto esperado?
    
    REGLA ESTRICTA: Responde ÚNICAMENTE con la palabra "CORRECTO" o "INCORRECTO". No des explicaciones.
    """
    
    eval_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=10
    )
    
    resultado_juez = eval_completion.choices[0].message.content.strip().upper()
    return "CORRECTO" in resultado_juez

def evaluate():
    print("Iniciando evaluación con LLM Juez...\n")
    
    with open("eval/dataset.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)

    results = []

    for item in dataset:
        question = item["question"]
        expected = item["expected_answer"]

        print(f"Pregunta: {question}")
        
        response = run_agent(question)
        
        is_correct = llm_judge(question, expected, response)
        
        if is_correct:
            print("✅ CORRECTO\n")
        else:
            print("❌ INCORRECTO")
            print(f"   Esperado: {expected}")
            print(f"   Recibido: {response}\n")

        results.append({
            "question": question,
            "response": response,
            "expected": expected,
            "correct": is_correct
        })

    score = sum(r["correct"] for r in results) / len(results)
    
    print("-" * 30)
    print(f"Puntaje final: {score * 100:.2f}%")
    print("-" * 30)
    
    return results, score

if __name__ == "__main__":
    evaluate()