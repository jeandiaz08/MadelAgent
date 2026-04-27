# MadelAgent
Implementacion de agente para base de datos relacional de empresa MADEL, con este se besca responder con un lenguaje natural preguntas de usuarios sobre analisis de datos de Stocks, historial, colaboradores etc..

# Madel AI - Agente Text-to-SQL

Proyecto desarrollado para la asignatura **Ingeniería de Soluciones con Inteligencia Artificial**.

## Descripción

Madel AI es un agente basado en modelos de lenguaje (LLM) que permite consultar una base de datos empresarial mediante lenguaje natural.

El sistema traduce preguntas del usuario a consultas SQL (Text-to-SQL), ejecuta dichas consultas en una base de datos PostgreSQL y retorna respuestas interpretadas en lenguaje natural.

Este enfoque permite realizar análisis de datos operacionales como stock, pedidos, empleados y movimientos de inventario sin necesidad de conocimientos técnicos en SQL.

## Arquitectura

Usuario
↓
Frontend (Streamlit)
↓
Agente IA (Groq - LLM)
↓
Generación SQL (Text-to-SQL)
↓
Base de Datos PostgreSQL (Docker)
↓
Resultado
↓
Respuesta en lenguaje natural

## Tecnologías

- Python
- Streamlit
- PostgreSQL
- Docker
- Groq (LLM)

# Instalación

**Pasos para ejecutar e instalar el proyecto**
git clone repo
cd project/docker


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
