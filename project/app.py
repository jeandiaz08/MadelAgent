import sys
import os

BASE_DIR = os.path.dirname(__file__)
BACKEND_PATH = os.path.join(BASE_DIR, "backend")
sys.path.append(BACKEND_PATH)

import streamlit as st
from src.agents.sql_agent import run_agent
from eval.evaluate import evaluate
from core.services.feedback_service import save_feedback
from core.services.history_service import get_history

st.set_page_config(page_title="Madel AI", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ebacb5; }
    .title { color: #ff4b4b; font-size: 40px; font-weight: bold; }
    .stButton>button { background-color: #ff4b4b; color: white; border: none; padding: 10px 20px; border-radius: 5px; }
    .stButton>button:hover { background-color: #ff1a1a; }
    /* Estilo para la tarjeta del chat */
    .chat-card { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

st.sidebar.image('img/logocolor.png', width=100)
st.sidebar.title("Historial")

if st.sidebar.button("Ver historial"):
    history = get_history()
    for h in history:
        pregunta, respuesta, fecha = h
        st.sidebar.write(f"🕒 {fecha}")
        st.sidebar.write(f"❔ {pregunta}")
        st.sidebar.write(f"💬 {respuesta}")
        st.sidebar.divider()

if st.sidebar.button("Nueva conversación"):
    st.session_state.history = []
    st.rerun()

st.sidebar.title("Panel de Control")

if st.sidebar.button("Evaluar sistema"):
    with st.spinner("Ejecutando pruebas..."):
        results, score = evaluate()
        st.session_state["eval_results"] = results
        st.session_state["eval_score"] = score
    st.sidebar.success("Evaluación completada")

st.title("Madel Asistente AI")
tab1, tab2 = st.tabs(["Chat de Gestión", "Reporte de Calidad"])

with tab1:
    st.write("Consulta información de la empresa en lenguaje natural")
    
    if "history" not in st.session_state:
        st.session_state.history = []

    chat_container = st.container(height=450)

    with chat_container:
        for message in st.session_state.history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Haz tu pregunta..."):
        st.session_state.history.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Pensando..."):
                    response = run_agent(prompt)
                st.markdown(response)
        
        st.session_state.history.append({"role": "assistant", "content": response})
        st.session_state["last_question"] = prompt
        st.session_state["last_response"] = response

    if "last_response" in st.session_state:
        st.divider()
        st.caption("¿Fue útil la última respuesta?")
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("👍"):
                save_feedback(st.session_state.last_question, st.session_state.last_response, True)
                st.toast("¡Gracias!")
        with col2:
            if st.button("👎"):
                save_feedback(st.session_state.last_question, st.session_state.last_response, False)
                st.toast("Tomamos nota")

with tab2:
    st.header("Resultados de la Evaluación")
    if "eval_results" in st.session_state:
        st.metric("Precisión General (Score)", f"{st.session_state.eval_score * 100:.2f}%")
        st.divider()

        for r in st.session_state.eval_results:
            with st.expander(f"{'✅' if r['correct'] else '❌'} Pregunta: {r['question']}"):
                st.write(f"**Respuesta del Agente:** {r['response']}")
                st.write(f"**Resultado Esperado:** {r['expected']}")
                if not r['correct']:
                    st.warning("El Juez determinó que la información no coincide.")
    else:
        st.info("Presiona el botón 'Evaluar sistema' en el panel lateral para generar el reporte.")