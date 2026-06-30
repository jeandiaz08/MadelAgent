from core.db.connection import get_connection


def _ensure_usage_feedback_column(cursor):
    cursor.execute(
        """
        ALTER TABLE llm_usage
        ADD COLUMN IF NOT EXISTS util BOOLEAN DEFAULT NULL
        """
    )


def save_feedback(pregunta, respuesta, es_util, session_id=None):
    conn = get_connection()
    cursor = conn.cursor()

    _ensure_usage_feedback_column(cursor)

    cursor.execute("""
        INSERT INTO feedback (pregunta, respuesta, es_util)
        VALUES (%s, %s, %s)
    """, (pregunta, respuesta, es_util))

    if session_id:
        cursor.execute(
            """
            WITH latest AS (
                SELECT id
                FROM llm_usage
                WHERE session_id = %s
                  AND question = %s
                ORDER BY fecha DESC
                LIMIT 1
            )
            UPDATE llm_usage
            SET util = %s
            WHERE id IN (SELECT id FROM latest)
            """,
            (session_id, pregunta, es_util),
        )
    else:
        cursor.execute(
            """
            WITH latest AS (
                SELECT id
                FROM llm_usage
                WHERE question = %s
                ORDER BY fecha DESC
                LIMIT 1
            )
            UPDATE llm_usage
            SET util = %s
            WHERE id IN (SELECT id FROM latest)
            """,
            (pregunta, es_util),
        )

    conn.commit()
    cursor.close()
    conn.close()
