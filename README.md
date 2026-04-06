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

## Instalación

```bash
git clone repo
cd project
python -m venv venv
pip install -r requirements.txt