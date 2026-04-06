from core.db.connection import get_connection

def save_feedback(pregunta, respuesta, es_util):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO feedback (pregunta, respuesta, es_util)
        VALUES (%s, %s, %s)
    """, (pregunta, respuesta, es_util))

    conn.commit()
    cursor.close()
    conn.close()