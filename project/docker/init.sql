CREATE TABLE sucursales (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    direccion TEXT
);

CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    categoria VARCHAR(50),
    precio NUMERIC
);

CREATE TABLE inventario (
    id SERIAL PRIMARY KEY,
    producto_id INT REFERENCES productos(id),
    sucursal_id INT REFERENCES sucursales(id),
    stock INT,
    ultima_actualizacion TIMESTAMP
);

CREATE TABLE proveedores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    proveedor_id INT REFERENCES proveedores(id),
    sucursal_id INT REFERENCES sucursales(id),
    fecha DATE,
    estado VARCHAR(50)
);

CREATE TABLE detalle_pedido (
    id SERIAL PRIMARY KEY,
    pedido_id INT REFERENCES pedidos(id),
    producto_id INT REFERENCES productos(id),
    cantidad INT
);

CREATE TABLE movimientos_inventario (
    id SERIAL PRIMARY KEY,
    producto_id INT REFERENCES productos(id),
    sucursal_origen_id INT,
    sucursal_destino_id INT,
    cantidad INT,
    tipo VARCHAR(50),
    fecha TIMESTAMP
);

CREATE TABLE empleados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    sucursal_id INT REFERENCES sucursales(id),
    cargo VARCHAR(50)
);

CREATE TABLE turnos (
    id SERIAL PRIMARY KEY,
    empleado_id INT REFERENCES empleados(id),
    fecha DATE,
    tipo_turno VARCHAR(50)
);

CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    pregunta TEXT,
    respuesta TEXT,
    es_util BOOLEAN,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);