from langchain_core.tools import tool

from core.services.memory_service import save_memory, search_memory
from core.services.query_service import execute_query
from core.services.usage_service import estimate_cost


SCHEMA_DESCRIPTION = """
Tablas principales:
- sucursales(id, nombre, direccion)
- productos(id, nombre, categoria, precio)
- inventario(id, producto_id, sucursal_id, stock, stock_minimo, ultima_actualizacion)
- proveedores(id, nombre)
- pedidos(id, proveedor_id, sucursal_id, fecha, estado)
- detalle_pedido(id, pedido_id, producto_id, cantidad)
- movimientos_inventario(id, producto_id, sucursal_origen_id, sucursal_destino_id, cantidad, tipo, fecha)
- ventas(id, sucursal_id, fecha, canal, total)
- detalle_venta(id, venta_id, producto_id, cantidad, precio_unitario)
- empleados(id, nombre, sucursal_id, cargo)
- turnos(id, empleado_id, fecha, tipo_turno)
""".strip()


def is_readonly_query(query):
    cleaned = query.strip().rstrip(";").upper()
    forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE"]
    return cleaned.startswith("SELECT") and not any(word in cleaned for word in forbidden)


@tool
def get_schema() -> str:
    """Devuelve el esquema disponible para generar consultas SQL sobre MADEL."""
    return SCHEMA_DESCRIPTION


@tool
def execute_readonly_sql(query: str):
    """Ejecuta una consulta SELECT segura sobre PostgreSQL y devuelve filas en formato dict."""
    if not is_readonly_query(query):
        return {"error": "Solo se permiten consultas SELECT de lectura."}
    return execute_query(query)


@tool
def estimate_query_cost(input_tokens: int, output_tokens: int, model: str = "llama-3.3-70b-versatile") -> str:
    """Estima el costo teorico de una llamada LLM segun tokens de entrada y salida."""
    cost = estimate_cost(input_tokens, output_tokens, model)
    return f"USD {cost:.6f}"


@tool
def save_conversation_memory(session_id: str, role: str, content: str) -> str:
    """Guarda un mensaje importante como memoria persistente de la conversacion."""
    save_memory(session_id, role, content)
    return "Memoria guardada."


@tool
def search_conversation_memory(session_id: str, query: str) -> str:
    """Recupera memoria relevante de conversaciones anteriores por tema o palabra clave."""
    rows = search_memory(session_id, query)
    if not rows:
        return "No hay memoria relevante."
    return "\n".join([f"{role}: {content}" for role, content, _ in rows])


AGENT_TOOLS = [
    get_schema,
    execute_readonly_sql,
    estimate_query_cost,
    save_conversation_memory,
    search_conversation_memory,
]
