from core.db.connection import get_connection


def _deduplicate_columns(columns):
    seen = {}
    unique_columns = []

    for column in columns:
        count = seen.get(column, 0)
        if count == 0:
            unique_columns.append(column)
        else:
            unique_columns.append(f"{column}_{count + 1}")
        seen[column] = count + 1

    return unique_columns


def execute_query(query: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(query)
        
        columns = _deduplicate_columns([desc[0] for desc in cursor.description])
        
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        data = []
        for row in results:
            data.append(dict(zip(columns, row)))
        
        return data

    except Exception as e:
        return {"error": str(e)}
