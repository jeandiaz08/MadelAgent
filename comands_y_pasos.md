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