import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR / "backend"))

from core.services.feedback_service import save_feedback
from core.services.usage_service import get_usage_summary
from src.agents.sql_agent import run_agent


SESSION_ID = "ep3-feedback-extra-20260629"

CASES = [
    ("Cuantos pedidos estan pendientes?", False),
    ("Que sucursal tiene mas ingresos por ventas?", True),
    ("Cuantas unidades se vendieron de Helado Mango?", True),
    ("Recomienda que productos deberia reponer para temporada alta", False),
]


def main():
    history = []
    for question, feedback in CASES:
        print(f"\nPregunta: {question}")
        try:
            answer = run_agent(question, chat_history=history, session_id=SESSION_ID)
        except Exception as exc:
            answer = f"ERROR_CONTROLADO_EN_PRUEBA: {type(exc).__name__}: {exc}"
            feedback = False

        save_feedback(question, answer, feedback, session_id=SESSION_ID)
        history.extend([
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
        ])
        print(f"Feedback: {'util' if feedback else 'no_util'}")
        print(answer.replace("\n", " ")[:700])
        time.sleep(10)

    print("\nUso reciente:")
    for row in get_usage_summary(session_id=SESSION_ID, limit=10)["recent"]:
        print(row)


if __name__ == "__main__":
    main()
