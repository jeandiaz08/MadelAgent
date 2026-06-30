# V1.3 (EP3) ACTUAL

## Cambios principales

- Observabilidad externa con LangSmith: trazas, latencia P50/P99, tasa de errores, tokens y uso de herramientas.
- Dashboard local en Streamlit con costos estimados, uso reciente y feedback historico.
- Feedback persistente en PostgreSQL para registrar respuestas utiles y no utiles.
- Columna `util` en `llm_usage` para relacionar uso de tokens con calidad percibida.
- Validacion de SQL de solo lectura con `execute_readonly_sql`.
- Controles basicos para limitar consultas sobre datos sensibles.

## Levantar todo

Ubicarse en:

```bash
cd project/docker
```

Levantar aplicacion y base de datos:

```bash
docker-compose up --build
```

Abrir:

```text
http://localhost:8501
```

## Reiniciar limpio si cambio el modelo de datos

Usar esto solo si se necesita recrear tablas y datos iniciales:

```bash
cd project/docker
docker-compose down -v
docker-compose up --build
```

## Reiniciar solo la app sin tocar la base de datos

Util para cambios de codigo o cambio de API key en `.env`:

```bash
docker restart madel_app
```

Si no toma los cambios:

```bash
docker compose -f project/docker/docker-compose.yml up -d --no-deps app
```

Si ademas se necesita reconstruir la imagen:

```bash
docker compose -f project/docker/docker-compose.yml up -d --no-deps --build app
```

## Revisar logs de la app

```bash
docker logs --tail 80 madel_app
```

## Entrar a PostgreSQL

```bash
docker exec -it madel_postgres psql -U admin -d madel_db
```

Comandos utiles dentro de PostgreSQL:

```sql
\dt
SELECT COUNT(*) FROM feedback;
SELECT util, COUNT(*) FROM llm_usage GROUP BY util;
```

## Variables recomendadas en `.env`

```bash
GROQ_API_KEY=tu_api_key
GROQ_MODEL=llama-3.3-70b-versatile
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=tu_langsmith_api_key
LANGSMITH_PROJECT=MadelAgent
```

# V1.2 (EP2) Anterior al (29/6/2026)

## Cambios principales

- Agente con herramientas declaradas mediante LangChain.
- Memoria corta en Streamlit y memoria persistente en PostgreSQL.
- Recuperacion de contexto para preguntas de seguimiento.
- Estimacion de tokens y costo teorico por consulta.
- Tablas historicas de ventas para KPIs y analisis de demanda.
- Pestana de observabilidad en la aplicacion.

## Importante si ya se ejecuto antes

Como se agregaron nuevas tablas (`ventas`, `detalle_venta`, `conversation_memory`, `llm_usage`) y una columna nueva en `inventario`, se recomienda reiniciar volumen:

```bash
cd project/docker
docker-compose down -v
docker-compose up --build
```

# V1.1 (26/4/2026)

## Ejecución del proyecto

Este proyecto está dockerizado, por lo que **NO es necesario crear entorno virtual ni instalar librerías manualmente**.

---

## levantar el contenedor

**Asegurarse de estar situado en la carpeta:**

project/docker

---

**Levantar todo (base de datos + aplicación + librerías):**

docker-compose up --build

---

## si ya se ejecutó antes (reiniciar limpio)

docker-compose down -v
docker-compose up --build

---

## acceder al sistema

Abrir en el navegador:

http://localhost:8501

---

## comprobar que funciona la base de datos

docker ps (Ver contenedores activos)

---

**Entrar a PostgreSQL:**

docker exec -it madel_postgres psql -U admin -d madel_db

---

**Ver tablas:**

\dt

---

## probar backend (opcional)

Solo para test interno:

python -m core.main

---

## extras

- Ctrl + D → salir de PostgreSQL
- Asegurarse de que Docker esté encendido
- No es necesario usar venv






# V1.0 (1/4/2026)
## Ejecución del proyecto
Antes de ejecutar asegurarse de crear un entrono virtual (python -m venv venv) ademas de activarlo (venv\Scripts\activate), luego descargar las librerias que estan en requirements.txt (pip install -r requirements.txt)
y listo sigue los demas pasos.

## Antes de levantar
**crear archivo .env en capeta /project y copiar credenciales adjuntas, si no funciona la api de groq se recomienda cambiar la api key por por una nueva devido al limite de uso de token**

## levantar el contenedor
**Asegurarse de estar situado en la carpeta de project/docker**
docker-compose up -d **Levantar todo -imagen e entorno -containe**

**si ya exiten volumenes de datos o se ejecto anteriormente, ejecutar esto**

docker-compose down -v
docker-compose up -d

## probar que funciona le backend
python -m core.main (opcional para test solo de backend)

## probar que funciona el fron-end(Ejecutar)
**Asegurarse de estar situado en la carpeta de project**
streamlit run app.py

**Luego abrir en el navegador**
http://localhost:8501

## Comandos de BD PostgreSQL
**entrar hacia la base de datos**
docker exec -it madel_postgres psql -U admin -d madel_db
**Comprobar que funcionen las tablas**
docker ps (Verificar que funciona y los contenedores activos)
docker exec -it madel_postgres psql -U admin -d madel_db #conectarse a las tablas, luego \dt (para ver las tablas)

## extras
ctl + d para salir del terminal

