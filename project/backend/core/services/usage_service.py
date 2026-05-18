from core.db.connection import get_connection
from src.utils.llm import DEFAULT_MODEL


MODEL_PRICING_USD_PER_MILLION = {
    "llama-3.3-70b-versatile": {
        "input": 0.59,
        "output": 0.79,
    }
}


def estimate_cost(input_tokens=0, output_tokens=0, model=DEFAULT_MODEL):
    pricing = MODEL_PRICING_USD_PER_MILLION.get(
        model,
        MODEL_PRICING_USD_PER_MILLION["llama-3.3-70b-versatile"],
    )
    return (
        (input_tokens / 1_000_000) * pricing["input"]
        + (output_tokens / 1_000_000) * pricing["output"]
    )


def save_usage(session_id, question, usage):
    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)
    total_tokens = usage.get("total_tokens", input_tokens + output_tokens)
    model = usage.get("model", DEFAULT_MODEL)
    estimated_cost = estimate_cost(input_tokens, output_tokens, model)

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO llm_usage (
                session_id, question, model, input_tokens, output_tokens,
                total_tokens, estimated_cost_usd
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                session_id,
                question,
                model,
                input_tokens,
                output_tokens,
                total_tokens,
                estimated_cost,
            ),
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception:
        return


def get_usage_summary(session_id=None, limit=20):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if session_id:
            cursor.execute(
                """
                SELECT model,
                       COALESCE(SUM(input_tokens), 0),
                       COALESCE(SUM(output_tokens), 0),
                       COALESCE(SUM(total_tokens), 0),
                       COALESCE(SUM(estimated_cost_usd), 0)
                FROM llm_usage
                WHERE session_id = %s
                GROUP BY model
                """,
                (session_id,),
            )
        else:
            cursor.execute(
                """
                SELECT model,
                       COALESCE(SUM(input_tokens), 0),
                       COALESCE(SUM(output_tokens), 0),
                       COALESCE(SUM(total_tokens), 0),
                       COALESCE(SUM(estimated_cost_usd), 0)
                FROM llm_usage
                GROUP BY model
                """
            )

        totals = cursor.fetchall()

        cursor.execute(
            """
            SELECT fecha, question, input_tokens, output_tokens, total_tokens, estimated_cost_usd
            FROM llm_usage
            WHERE (%s IS NULL OR session_id = %s)
            ORDER BY fecha DESC
            LIMIT %s
            """,
            (session_id, session_id, limit),
        )
        recent = cursor.fetchall()

        cursor.close()
        conn.close()

        return {
            "totals": totals,
            "recent": recent,
        }
    except Exception:
        return {"totals": [], "recent": []}
