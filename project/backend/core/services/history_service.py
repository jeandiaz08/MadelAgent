from core.db.connection import get_connection


def get_history(limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT pregunta, respuesta, es_util, fecha
        FROM feedback
        ORDER BY fecha DESC
        LIMIT %s
    """, (limit,))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def get_feedback_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total,
            COUNT(*) FILTER (WHERE es_util IS TRUE) AS positivos,
            COUNT(*) FILTER (WHERE es_util IS FALSE) AS negativos
        FROM feedback
    """)

    data = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "total": int(data[0] or 0),
        "positivos": int(data[1] or 0),
        "negativos": int(data[2] or 0),
    }
