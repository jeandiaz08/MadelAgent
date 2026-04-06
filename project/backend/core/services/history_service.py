from core.db.connection import get_connection

def get_history(limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT pregunta, respuesta, fecha
        FROM feedback
        ORDER BY fecha DESC
        LIMIT %s
    """, (limit,))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data