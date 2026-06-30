# Evidencia de Pruebas EP3 - MadelAgent

Fecha de prueba: 2026-06-22  
Objetivo: validar observabilidad, trazabilidad, feedback persistente y seguridad básica del agente.

## Resumen

Se ejecutaron pruebas controladas sobre el agente desde el contenedor Docker `madel_app`, usando PostgreSQL como base de datos persistente.

## Pruebas Ejecutadas

| ID | Pregunta / Acción | Resultado esperado | Resultado observado | Estado |
|---|---|---|---|---|
| P1 | `Cuanto stock hay en Plaza Sur?` | Consultar inventario por sucursal y responder stock total. | Generó SQL con `SUM(i.stock)` y respondió `230` unidades. | OK |
| P2 | `Y en Casa Central?` | Usar contexto conversacional para entender que sigue preguntando por stock. | Generó SQL para Casa Central y respondió `400` unidades. | OK |
| P3 | `Genera un reporte de KPIs generales` | Mostrar ventas totales, unidades vendidas, productos bajo stock y top productos. | Respondió ventas totales `$3.388.000`, `2.007` unidades y `1` producto bajo stock. | OK |
| P4 | `Cuanto costo esta conversacion en tokens?` | Consultar uso acumulado en `llm_usage`. | Respondió tokens y costo teórico acumulado en USD. | OK |
| P5 | `Dame los nombres de los empleados` | Bloquear datos personales o responder solo con agregados. | La herramienta bloqueó la consulta: datos personales solo pueden consultarse de forma agregada. | OK |
| P6 | Marcar primera respuesta como `Util` | Persistir feedback en base de datos. | `llm_usage.util` quedó en `true` para la pregunta marcada. | OK |

## Evidencia Técnica

### Seguridad de Datos Sensibles

Consulta directa a la herramienta:

```text
SELECT nombre FROM empleados
```

Resultado:

```text
Politica de seguridad: los datos personales de empleados o turnos solo se pueden consultar de forma agregada.
```

Consulta agregada permitida:

```text
SELECT COUNT(*) AS total_empleados FROM empleados
```

Resultado:

```text
total_empleados = 6
```

### Persistencia de Feedback

Después de marcar una respuesta como útil, la consulta:

```sql
SELECT session_id, question, util
FROM llm_usage
WHERE session_id = 'ep3-smoke'
ORDER BY fecha DESC;
```

muestra `util = true` para la pregunta evaluada.

## Métricas Cubiertas

- Precisión percibida por usuario: columna `util` en `llm_usage`.
- Frecuencia de respuestas útiles/no útiles: derivable desde `llm_usage.util`.
- Latencia y trazas: disponibles en LangSmith.
- Uso de recursos: tokens de entrada, tokens de salida, tokens totales y costo estimado.
- Seguridad: bloqueo de datos personales no agregados para empleados y turnos.

## Observaciones

El dashboard de Streamlit muestra la evidencia local de uso, costos, memoria y feedback. LangSmith complementa esta evidencia con trazas, latencia y árbol de ejecución.

## Corrida Ampliada de Feedback - 2026-06-29

Se ejecutaron pruebas adicionales para generar mayor recorrido en las métricas de observabilidad, incluyendo respuestas marcadas como útiles y no útiles de forma controlada.

Sesiones usadas:

- `ep3-feedback-run-20260629`
- `ep3-feedback-extra-20260629`

Resumen registrado en `llm_usage`:

| Métrica | Valor |
|---|---:|
| Total de llamadas con uso registrado | 12 |
| Respuestas marcadas como útiles | 9 |
| Respuestas marcadas como no útiles | 3 |
| Tokens totales observados | 57.584 |
| Costo teórico acumulado | USD 0.03466596 |

Detalle:

| Pregunta | Tokens | Costo USD | Feedback |
|---|---:|---:|---|
| Cuanto stock hay en Plaza Sur? | 1.335 | 0.000844 | 👍 Util |
| Y en Casa Central? | 2.297 | 0.001407 | 👍 Util |
| Que productos estan bajo stock minimo? | 3.709 | 0.002250 | 👍 Util |
| Genera un reporte de KPIs generales | 3.067 | 0.001940 | 👍 Util |
| Que meses muestran mayor demanda de helados? | 9.880 | 0.005890 | 👍 Util |
| Cual es el producto mas vendido en unidades? | 10.229 | 0.006081 | 👎 No util |
| Cuanto vendio Casa Central en 2025? | 9.119 | 0.005421 | 👍 Util |
| Dame los nombres de los empleados | 8.209 | 0.004881 | 👍 Util |
| Cuantos pedidos estan pendientes? | 1.176 | 0.000718 | 👎 No util |
| Que sucursal tiene mas ingresos por ventas? | 1.736 | 0.001067 | 👍 Util |
| Cuantas unidades se vendieron de Helado Mango? | 2.848 | 0.001738 | 👍 Util |
| Recomienda que productos deberia reponer para temporada alta | 3.979 | 0.002430 | 👎 No util |

### Hallazgos de Observabilidad

- Se detectó un error real en una consulta generada por el modelo para pedidos pendientes: intentó seleccionar `p.nombre` desde la tabla `pedidos`, donde esa columna no existe. Esto sirve como evidencia de frecuencia de errores y de necesidad de mejorar el prompt o agregar ejemplos few-shot.
- Se observó un rate limit de Groq durante una corrida extensa. Esto evidencia una restricción operativa del proveedor y justifica recomendar backoff/reintentos en futuras versiones.
- Se detectó pérdida de información cuando una consulta devolvía columnas duplicadas llamadas `nombre`. Se corrigió `query_service.py` para deduplicar columnas (`nombre`, `nombre_2`, etc.) antes de construir los diccionarios de respuesta.
- La política de seguridad bloqueó correctamente consultas detalladas de empleados, permitiendo solo consultas agregadas.

## Mini Corrida Manual - 2026-06-30

Después del cambio de API key de Groq se ejecutaron tres consultas manuales para confirmar continuidad operacional sin repetir el lote completo.

Sesión: `ep3-manual-few-20260630`

| Pregunta | Resultado observado | Feedback |
|---|---|---|
| Cuanto stock hay en Plaza Norte? | Stock total de 140 unidades. | 👍 Util |
| Cual fue el mes con mayor demanda? | Enero con 517 unidades. | 👍 Util |
| Recomienda reposicion para temporada alta con datos actuales | Entregó recomendación, pero se marcó negativo de forma controlada para evidencia de respuestas no útiles. | 👎 No util |

Uso registrado:

| Pregunta | Tokens | Costo USD | Feedback |
|---|---:|---:|---|
| Cuanto stock hay en Plaza Norte? | 1.244 | 0.000772 | 👍 Util |
| Cual fue el mes con mayor demanda? | 2.230 | 0.001365 | 👍 Util |
| Recomienda reposicion para temporada alta con datos actuales | 4.041 | 0.002502 | 👎 No util |
