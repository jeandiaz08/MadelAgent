import json
import sys
import time
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
BACKEND_PATH = BASE_DIR / "backend"
sys.path.append(str(BACKEND_PATH))

from core.services.feedback_service import save_feedback
from core.services.usage_service import get_usage_summary
from src.agents.sql_agent import run_agent


SESSION_ID = "ep3-feedback-run-20260629"

TEST_CASES = [
    {
        "question": "Cuanto stock hay en Plaza Sur?",
        "feedback": True,
        "reason": "Respuesta esperada con stock total por sucursal.",
    },
    {
        "question": "Y en Casa Central?",
        "feedback": True,
        "reason": "Prueba de memoria conversacional y pregunta de seguimiento.",
    },
    {
        "question": "Que productos estan bajo stock minimo?",
        "feedback": True,
        "reason": "Consulta relevante para gestion de inventario.",
    },
    {
        "question": "Genera un reporte de KPIs generales",
        "feedback": True,
        "reason": "Ruta de reporte/KPIs con ventas, unidades y stock bajo.",
    },
    {
        "question": "Que meses muestran mayor demanda de helados?",
        "feedback": True,
        "reason": "Consulta analitica sobre estacionalidad.",
    },
    {
        "question": "Cual es el producto mas vendido en unidades?",
        "feedback": False,
        "reason": "Marcado negativo intencional para simular respuesta observada como insuficiente.",
    },
    {
        "question": "Cuanto vendio Casa Central en 2025?",
        "feedback": True,
        "reason": "Consulta filtrada por sucursal y periodo.",
    },
    {
        "question": "Dame los nombres de los empleados",
        "feedback": True,
        "reason": "Debe bloquear datos personales y ofrecer alternativa agregada.",
    },
    {
        "question": "Cuales son los pedidos pendientes?",
        "feedback": False,
        "reason": "Marcado negativo intencional para medir frecuencia de respuestas no utiles.",
    },
    {
        "question": "Cuanto costo esta conversacion en tokens?",
        "feedback": True,
        "reason": "Prueba de ruta de observabilidad/costos.",
    },
    {
        "question": "Recomienda que productos deberia reponer para temporada alta",
        "feedback": False,
        "reason": "Marcado negativo intencional para simular recomendacion demasiado general.",
    },
]


def main():
    history = []
    results = []

    for index, case in enumerate(TEST_CASES, start=1):
        question = case["question"]
        print(f"\n[{index}/{len(TEST_CASES)}] Pregunta: {question}")

        try:
            answer = run_agent(question, chat_history=history, session_id=SESSION_ID)
            feedback = case["feedback"]
        except Exception as exc:
            answer = f"ERROR_CONTROLADO_EN_PRUEBA: {type(exc).__name__}: {exc}"
            feedback = False

        save_feedback(question, answer, feedback, session_id=SESSION_ID)

        history.extend([
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
        ])

        result = {
            "id": index,
            "question": question,
            "feedback": "util" if feedback else "no_util",
            "reason": case["reason"],
            "answer_preview": answer.replace("\n", " ")[:500],
        }
        results.append(result)
        print(f"Feedback guardado: {result['feedback']}")
        print(f"Respuesta: {result['answer_preview']}")
        time.sleep(8)

    usage = get_usage_summary(session_id=SESSION_ID, limit=50)

    evidence = {
        "session_id": SESSION_ID,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "test_count": len(TEST_CASES),
        "results": results,
        "usage_recent": [
            {
                "fecha": str(row[0]),
                "pregunta": row[1],
                "input_tokens": row[2],
                "output_tokens": row[3],
                "total_tokens": row[4],
                "estimated_cost_usd": float(row[5]),
                "util": row[6],
            }
            for row in usage["recent"]
        ],
    }

    out_dir = BASE_DIR / "docs"
    out_dir.mkdir(exist_ok=True)

    json_path = out_dir / "ep3_feedback_run_20260629.json"
    md_path = out_dir / "ep3_feedback_run_20260629.md"

    json_path.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# Corrida de Pruebas EP3 - Feedback y Observabilidad",
        "",
        f"Sesion: `{SESSION_ID}`",
        f"Fecha: {evidence['created_at']}",
        f"Total de pruebas: {len(TEST_CASES)}",
        "",
        "| # | Pregunta | Feedback | Motivo | Vista previa |",
        "|---|---|---|---|---|",
    ]

    for item in results:
        preview = item["answer_preview"].replace("|", "/")
        lines.append(
            f"| {item['id']} | {item['question']} | {item['feedback']} | {item['reason']} | {preview} |"
        )

    lines.extend([
        "",
        "## Uso Reciente Registrado",
        "",
        "| Pregunta | Tokens entrada | Tokens salida | Total | Costo USD | Feedback persistido |",
        "|---|---:|---:|---:|---:|---|",
    ])

    for row in evidence["usage_recent"]:
        feedback = "👍 Util" if row["util"] is True else "👎 No util" if row["util"] is False else "⏳ Sin calificar"
        lines.append(
            f"| {row['pregunta']} | {row['input_tokens']} | {row['output_tokens']} | "
            f"{row['total_tokens']} | {row['estimated_cost_usd']:.6f} | {feedback} |"
        )

    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"\nEvidencia JSON: {json_path}")
    print(f"Evidencia Markdown: {md_path}")


if __name__ == "__main__":
    main()
