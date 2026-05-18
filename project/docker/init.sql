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
    stock_minimo INT DEFAULT 20,
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

CREATE TABLE ventas (
    id SERIAL PRIMARY KEY,
    sucursal_id INT REFERENCES sucursales(id),
    fecha DATE,
    canal VARCHAR(50),
    total NUMERIC
);

CREATE TABLE detalle_venta (
    id SERIAL PRIMARY KEY,
    venta_id INT REFERENCES ventas(id),
    producto_id INT REFERENCES productos(id),
    cantidad INT,
    precio_unitario NUMERIC
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

CREATE TABLE conversation_memory (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100),
    role VARCHAR(30),
    content TEXT,
    topic TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE llm_usage (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100),
    question TEXT,
    model VARCHAR(100),
    input_tokens INT,
    output_tokens INT,
    total_tokens INT,
    estimated_cost_usd NUMERIC(12, 8),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ventas_fecha ON ventas(fecha);
CREATE INDEX idx_ventas_sucursal ON ventas(sucursal_id);
CREATE INDEX idx_detalle_venta_producto ON detalle_venta(producto_id);
CREATE INDEX idx_memory_session_topic ON conversation_memory(session_id, topic);
CREATE INDEX idx_usage_session_fecha ON llm_usage(session_id, fecha);
