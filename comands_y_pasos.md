# V1.2 (EP2) ACTUAL

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

