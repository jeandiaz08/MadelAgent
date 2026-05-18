import os
import sys
import uuid

import streamlit as st

BASE_DIR = os.path.dirname(__file__)
BACKEND_PATH = os.path.join(BASE_DIR, "backend")
sys.path.append(BACKEND_PATH)

from core.services.feedback_service import save_feedback
from core.services.history_service import get_history
from core.services.memory_service import clear_memory, get_recent_memory
from core.services.usage_service import get_usage_summary
from eval.evaluate import evaluate
from src.agents.sql_agent import get_agent_tool_names, run_agent


st.set_page_config(page_title="Madel AI", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background-color: #f7eef1; color: #2d2025; }
    [data-testid="stAppViewContainer"] { background-color: #f7eef1; }
    [data-testid="stMain"] p,
    [data-testid="stMain"] label,
    [data-testid="stMain"] span,
    [data-testid="stMain"] div {
        color: #2d2025;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] li {
        color: #ffffff;
    }
    .main-title { color: #c81e3a; font-size: 2.2rem; font-weight: 700; margin-bottom: .2rem; }
    .subtle { color: #57464b; font-size: .95rem; }
    .stTabs [data-baseweb="tab"] p { color: #57464b; }
    .stTabs [aria-selected="true"] p { color: #c81e3a; }
    .stButton>button { background-color: #c81e3a; color: white; border: none; border-radius: 6px; }
    .stButton>button:hover { background-color: #9f1730; color: white; }
    </style>
    """,
    unsafe_allow_html=True,
)


if "history" not in st.session_state:
    st.session_state.history = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())


st.sidebar.image("img/logocolor.png", width=100)
st.sidebar.title("Madel Agent")
st.sidebar.caption(f"Sesion: {st.session_state.session_id[:8]}")

if st.sidebar.button("Nueva conversacion"):
    clear_memory(st.session_state.session_id)
    st.session_state.history = []
    st.session_state.session_id = str(uuid.uuid4())
    st.rerun()

st.sidebar.divider()
st.sidebar.subheader("Herramientas del agente")
for tool_name in get_agent_tool_names():
    st.sidebar.write(f"- {tool_name}")

st.sidebar.divider()
st.sidebar.subheader("Panel de control")

if st.sidebar.button("Evaluar sistema"):
    with st.spinner("Ejecutando benchmark con juez LLM..."):
        results, score = evaluate()
        st.session_state["eval_results"] = results
        st.session_state["eval_score"] = score
    st.sidebar.success("Evaluacion completada")

if st.sidebar.button("Ver feedback historico"):
    st.session_state["show_feedback"] = not st.session_state.get("show_feedback", False)

if st.session_state.get("show_feedback", False):
    history = get_history()
    for pregunta, respuesta, fecha in history:
        st.sidebar.write(f"{fecha}")
        st.sidebar.write(f"Pregunta: {pregunta}")
        st.sidebar.write(f"Respuesta: {respuesta}")
        st.sidebar.divider()


st.markdown('<div class="main-title">Madel Asistente AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtle">Agente Text-to-SQL con memoria, herramientas, costos estimados y analitica historica.</div>',
    unsafe_allow_html=True,
)

tab_chat, tab_quality, tab_observability = st.tabs(
    ["Chat de gestion", "Reporte de calidad", "Observabilidad"]
)


with tab_chat:
    st.write("Consulta informacion de la empresa en lenguaje natural.")

    chat_container = st.container(height=470)

    with chat_container:
        for message in st.session_state.history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Haz tu pregunta..."):
        previous_history = list(st.session_state.history)
        st.session_state.history.append({"role": "user", "content": prompt})

        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Pensando con memoria y herramientas..."):
                    response = run_agent(
                        prompt,
                        chat_history=previous_history,
                        session_id=st.session_state.session_id,
                    )
                st.markdown(response)

        st.session_state.history.append({"role": "assistant", "content": response})
        st.session_state["last_question"] = prompt
        st.session_state["last_response"] = response

    if "last_response" in st.session_state:
        st.divider()
        st.caption("Fue util la ultima respuesta?")
        col1, col2 = st.columns([1, 6])
        with col1:
            if st.button("Util"):
                save_feedback(st.session_state.last_question, st.session_state.last_response, True)
                st.toast("Gracias por el feedback.")
        with col2:
            if st.button("No util"):
                save_feedback(st.session_state.last_question, st.session_state.last_response, False)
                st.toast("Tomamos nota para mejorar.")


with tab_quality:
    st.header("Resultados de evaluacion")
    if "eval_results" in st.session_state:
        st.metric("Precision general", f"{st.session_state.eval_score * 100:.2f}%")
        st.divider()

        for result in st.session_state.eval_results:
            icon = "OK" if result["correct"] else "ERROR"
            with st.expander(f"{icon} Pregunta: {result['question']}"):
                st.write(f"**Respuesta del agente:** {result['response']}")
                st.write(f"**Resultado esperado:** {result['expected']}")
                if not result["correct"]:
                    st.warning("El juez determino que la informacion no coincide.")
    else:
        st.info("Presiona 'Evaluar sistema' en el panel lateral para generar el reporte.")


with tab_observability:
    st.header("Memoria y costos")

    usage = get_usage_summary(session_id=st.session_state.session_id, limit=10)
    total_tokens = sum(int(row[3]) for row in usage["totals"]) if usage["totals"] else 0
    total_cost = sum(float(row[4]) for row in usage["totals"]) if usage["totals"] else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Tokens estimados", total_tokens)
    col2.metric("Costo teorico", f"USD {total_cost:.6f}")
    col3.metric("Mensajes en memoria", len(get_recent_memory(st.session_state.session_id, limit=50)))

    st.subheader("Uso reciente")
    if usage["recent"]:
        st.dataframe(
            [
                {
                    "fecha": row[0],
                    "pregunta": row[1],
                    "entrada": row[2],
                    "salida": row[3],
                    "total": row[4],
                    "costo_usd": float(row[5]),
                }
                for row in usage["recent"]
            ],
            width="stretch",
        )
    else:
        st.info("Aun no hay llamadas registradas en esta sesion.")

    st.subheader("Memoria reciente")
    memory_rows = get_recent_memory(st.session_state.session_id, limit=10)
    if memory_rows:
        for role, content, fecha in memory_rows:
            st.write(f"**{role}** | {fecha}")
            st.write(content)
            st.divider()
    else:
        st.info("La memoria de esta sesion esta vacia.")
