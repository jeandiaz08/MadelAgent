from core.db.connection import get_connection

def execute_query(query: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(query)
        
        columns = [desc[0] for desc in cursor.description]
        
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        data = []
        for row in results:
            data.append(dict(zip(columns, row)))
        
        return data

    except Exception as e:
        return {"error": str(e)}