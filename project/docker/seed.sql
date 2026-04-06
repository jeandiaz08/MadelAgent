TRUNCATE TABLE turnos, empleados, movimientos_inventario, detalle_pedido, pedidos, inventario, proveedores, productos, sucursales RESTART IDENTITY CASCADE;

INSERT INTO sucursales (nombre, direccion) VALUES
('Casa Central', 'Santiago Centro'),
('Plaza Sur', 'San Bernardo'),
('Tobalaba', 'Providencia'),
('Plaza Norte', 'Huechuraba');

INSERT INTO productos (nombre, categoria, precio) VALUES
('Helado Vainilla', 'Helados', 2500),
('Helado Chocolate', 'Helados', 2600),
('Helado Frutilla', 'Helados', 2400),
('Cono Simple', 'Complementos', 500),
('Barquillo', 'Complementos', 700),
('Helado Mango', 'Helados', 2700),
('Helado Piña', 'Helados', 2600),
('Helado Cookies', 'Helados', 2900),
('Sundae Chocolate', 'Postres', 3500),
('Sundae Frutilla', 'Postres', 3400);

INSERT INTO proveedores (nombre) VALUES
('Proveedor Uno'),
('Proveedor Dos');

INSERT INTO inventario (producto_id, sucursal_id, stock, ultima_actualizacion) VALUES
(1, 1, 100, NOW()),
(2, 1, 80, NOW()),
(3, 2, 50, NOW()),
(1, 3, 60, NOW()),
(2, 4, 30, NOW()),
(4, 1, 150, NOW()),
(5, 2, 120, NOW()),
(6, 3, 90, NOW()),
(7, 4, 110, NOW()),
(8, 1, 70, NOW()),
(9, 2, 60, NOW());

INSERT INTO pedidos (proveedor_id, sucursal_id, fecha, estado) VALUES
(1, 1, CURRENT_DATE, 'pendiente'),
(2, 2, CURRENT_DATE, 'recibido'),
(1, 3, CURRENT_DATE - INTERVAL '1 day', 'recibido'),
(2, 4, CURRENT_DATE - INTERVAL '2 days', 'pendiente');

INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad) VALUES
(1, 1, 50),
(1, 2, 30),
(2, 3, 40),
(3, 4, 60),
(3, 5, 40),
(4, 6, 30);

INSERT INTO movimientos_inventario (producto_id, sucursal_origen_id, sucursal_destino_id, cantidad, tipo, fecha) VALUES
(1, 1, 2, 20, 'traslado', NOW()),
(2, NULL, 1, 50, 'ingreso', NOW()),
(3, 2, NULL, 10, 'salida', NOW()),
(4, 1, 3, 25, 'traslado', NOW()),
(5, NULL, 2, 60, 'ingreso', NOW()),
(6, 3, NULL, 15, 'salida', NOW());

INSERT INTO empleados (nombre, sucursal_id, cargo) VALUES
('Juan Perez', 1, 'Vendedor'),
('Maria Lopez', 2, 'Cajera'),
('Carlos Soto', 3, 'Supervisor'),
('Ana Torres', 1, 'Cajera'),
('Luis Rojas', 2, 'Vendedor'),
('Pedro Díaz', 4, 'Supervisor');

INSERT INTO turnos (empleado_id, fecha, tipo_turno) VALUES
(1, CURRENT_DATE, 'mañana'),
(2, CURRENT_DATE, 'tarde'),
(3, CURRENT_DATE, 'noche'),
(4, CURRENT_DATE, 'mañana'),
(5, CURRENT_DATE, 'tarde'),
(6, CURRENT_DATE, 'noche'),
(1, CURRENT_DATE - INTERVAL '1 day', 'tarde'),
(2, CURRENT_DATE - INTERVAL '1 day', 'mañana');