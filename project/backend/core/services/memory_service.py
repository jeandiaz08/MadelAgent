import re
from core.db.connection import get_connection


def _extract_topic(text):
    words = re.findall(r"[A-Za-z0-9_]+", text.lower())
    stopwords = {
        "como", "cuanto", "cuantos", "cual", "cuales", "dime", "hay",
        "por", "para", "con", "los", "las", "del", "una", "unos",
        "unas", "que", "mas", "menos", "stock", "total",
    }
    keywords = [word for word in words if len(word) > 3 and word not in stopwords]
    return " ".join(keywords[:8])


def save_memory(session_id, role, content, topic=None):
    topic = topic or _extract_topic(content)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO conversation_memory (session_id, role, content, topic)
            VALUES (%s, %s, %s, %s)
            """,
            (session_id, role, content, topic),
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception:
        return


def save_interaction(session_id, question, answer):
    save_memory(session_id, "user", question)
    save_memory(session_id, "assistant", answer, topic=_extract_topic(question))


def get_recent_memory(session_id, limit=8):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT role, content, fecha
            FROM conversation_memory
            WHERE session_id = %s
            ORDER BY fecha DESC
            LIMIT %s
            """,
            (session_id, limit),
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return list(reversed(rows))
    except Exception:
        return []


def search_memory(session_id, query, limit=6):
    topic = _extract_topic(query)
    terms = [term for term in topic.split() if len(term) > 3]

    if not terms:
        return get_recent_memory(session_id, limit=limit)

    where = " OR ".join(["content ILIKE %s OR topic ILIKE %s" for _ in terms])
    params = []
    for term in terms:
        params.extend([f"%{term}%", f"%{term}%"])

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT role, content, fecha
            FROM conversation_memory
            WHERE session_id = %s AND ({where})
            ORDER BY fecha DESC
            LIMIT %s
            """,
            [session_id, *params, limit],
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return list(reversed(rows))
    except Exception:
        return []


def clear_memory(session_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM conversation_memory WHERE session_id = %s",
            (session_id,),
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception:
        return
