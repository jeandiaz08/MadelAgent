from src.agents.tools import AGENT_TOOLS, execute_readonly_sql, is_readonly_query
from src.generate.generate import generate_answer
from src.utils.llm import ask_llm
from src.utils.prompts import RAG_SYSTEM_PROMPT
from core.services.memory_service import get_recent_memory, save_interaction, search_memory
from core.services.usage_service import get_usage_summary, save_usage


def _format_messages(rows):
    if not rows:
        return "Sin contexto previo."
    return "\n".join([f"{role}: {content}" for role, content, _ in rows])


def _merge_usage(*items):
    usage = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
    model = None
    for item in items:
        if not item:
            continue
        model = item.get("model", model)
        usage["input_tokens"] += item.get("input_tokens", 0)
        usage["output_tokens"] += item.get("output_tokens", 0)
        usage["total_tokens"] += item.get("total_tokens", 0)
    if model:
        usage["model"] = model
    return usage


def _plan_route(question):
    text = question.lower()
    if any(word in text for word in ["costo", "coste", "token", "tokens", "precio"]):
        return "cost"
    if any(word in text for word in ["kpi", "reporte", "resumen ejecutivo", "dashboard"]):
        return "report"
    return "sql"


def _cost_response(session_id):
    summary = get_usage_summary(session_id=session_id, limit=5)
    if not summary["totals"]:
        return (
            "Todavia no hay uso registrado para esta conversacion. "
            "Cuando hagas una consulta, registrare tokens de entrada, tokens de salida "
            "y costo teorico usando la tarifa publica de Groq para llama-3.3-70b-versatile."
        )

    lines = ["Resumen de uso estimado de esta conversacion:"]
    for model, input_tokens, output_tokens, total_tokens, cost in summary["totals"]:
        lines.append(
            f"- Modelo {model}: {total_tokens} tokens "
            f"({input_tokens} entrada, {output_tokens} salida), costo teorico USD {float(cost):.6f}."
        )
    lines.append(
        "Esta cifra es estimada: si la cuenta usa capa gratuita, el cobro real puede ser USD 0, "
        "pero la metrica permite proyectar costos de produccion."
    )
    return "\n".join(lines)


def _run_kpi_report(question, context, session_id):
    report_sql = """
    SELECT 'ventas_totales' AS kpi, COALESCE(SUM(total), 0)::numeric AS valor
    FROM ventas
    UNION ALL
    SELECT 'unidades_vendidas' AS kpi, COALESCE(SUM(cantidad), 0)::numeric AS valor
    FROM detalle_venta
    UNION ALL
    SELECT 'productos_bajo_stock' AS kpi, COUNT(*)::numeric AS valor
    FROM inventario
    WHERE stock <= stock_minimo
    """

    top_products_sql = """
    SELECT p.nombre, SUM(dv.cantidad) AS unidades, SUM(dv.cantidad * dv.precio_unitario) AS ingresos
    FROM detalle_venta dv
    JOIN productos p ON p.id = dv.producto_id
    GROUP BY p.nombre
    ORDER BY unidades DESC
    LIMIT 5
    """

    monthly_sql = """
    SELECT DATE_TRUNC('month', v.fecha)::date AS mes, SUM(v.total) AS total
    FROM ventas v
    GROUP BY mes
    ORDER BY mes
    """

    data = {
        "kpis": execute_readonly_sql.invoke({"query": report_sql}),
        "top_productos": execute_readonly_sql.invoke({"query": top_products_sql}),
        "ventas_mensuales": execute_readonly_sql.invoke({"query": monthly_sql}),
    }

    answer, answer_usage = generate_answer(
        question,
        data,
        context=context,
        return_usage=True,
    )
    save_usage(session_id, question, answer_usage)
    return answer


def run_agent(question: str, chat_history=None, session_id="default"):
    route = _plan_route(question)
    recent_context = _format_messages(get_recent_memory(session_id, limit=8))
    relevant_context = _format_messages(search_memory(session_id, question, limit=6))
    chat_context = _format_messages([
        (message.get("role", "user"), message.get("content", ""), None)
        for message in (chat_history or [])[-8:]
    ])

    full_context = f"""
    Memoria reciente:
    {recent_context}

    Memoria recuperada semanticamente:
    {relevant_context}

    Historial de la sesion actual:
    {chat_context}
    """

    if route == "cost":
        answer = _cost_response(session_id)
        save_interaction(session_id, question, answer)
        return answer

    if route == "report":
        answer = _run_kpi_report(question, full_context, session_id)
        save_interaction(session_id, question, answer)
        return answer

    user_payload = f"""
    Contexto conversacional para resolver referencias:
    {full_context}

    Pregunta actual:
    {question}
    """

    sql_query, sql_usage = ask_llm(
        RAG_SYSTEM_PROMPT,
        user_payload,
        temperature=0,
        max_tokens=350,
        return_usage=True,
    )

    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    print(f"\nSQL generado: {sql_query}")

    if not is_readonly_query(sql_query):
        answer, answer_usage = generate_answer(
            question,
            f"Error: El sistema no pudo generar una consulta valida. Respuesta del modelo: {sql_query}",
            context=full_context,
            return_usage=True,
        )
        save_usage(session_id, question, _merge_usage(sql_usage, answer_usage))
        save_interaction(session_id, question, answer)
        return answer

    result = execute_readonly_sql.invoke({"query": sql_query})
    print(f"Resultado DB: {result}")

    final_answer, answer_usage = generate_answer(
        question,
        result,
        context=full_context,
        return_usage=True,
    )

    save_usage(session_id, question, _merge_usage(sql_usage, answer_usage))
    save_interaction(session_id, question, final_answer)

    return final_answer


def get_agent_tool_names():
    return [tool.name for tool in AGENT_TOOLS]
