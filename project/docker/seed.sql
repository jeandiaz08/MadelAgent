TRUNCATE TABLE turnos, empleados, movimientos_inventario, detalle_venta, ventas, detalle_pedido, pedidos, inventario, proveedores, productos, sucursales RESTART IDENTITY CASCADE;

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

INSERT INTO inventario (producto_id, sucursal_id, stock, stock_minimo, ultima_actualizacion) VALUES
(1, 1, 100, 40, NOW()),
(2, 1, 80, 35, NOW()),
(3, 2, 50, 45, NOW()),
(1, 3, 60, 35, NOW()),
(2, 4, 30, 35, NOW()),
(4, 1, 150, 80, NOW()),
(5, 2, 120, 70, NOW()),
(6, 3, 90, 40, NOW()),
(7, 4, 110, 40, NOW()),
(8, 1, 70, 35, NOW()),
(9, 2, 60, 30, NOW());

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

INSERT INTO ventas (sucursal_id, fecha, canal, total) VALUES
(1, '2024-01-15', 'tienda', 185000),
(2, '2024-01-18', 'tienda', 142000),
(3, '2024-02-12', 'delivery', 198000),
(4, '2024-03-09', 'tienda', 98000),
(1, '2024-07-21', 'tienda', 82000),
(2, '2024-09-12', 'delivery', 112000),
(1, '2024-12-18', 'tienda', 235000),
(3, '2024-12-23', 'delivery', 248000),
(1, '2025-01-10', 'tienda', 252000),
(2, '2025-01-17', 'delivery', 221000),
(3, '2025-02-08', 'tienda', 238000),
(4, '2025-02-16', 'delivery', 214000),
(1, '2025-03-11', 'tienda', 137000),
(2, '2025-04-15', 'tienda', 118000),
(3, '2025-05-20', 'delivery', 96000),
(4, '2025-06-14', 'tienda', 89000),
(1, '2025-09-05', 'delivery', 127000),
(2, '2025-10-19', 'tienda', 146000),
(3, '2025-11-28', 'delivery', 169000),
(4, '2025-12-20', 'tienda', 281000);

INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario) VALUES
(1, 1, 30, 2500), (1, 2, 25, 2600), (1, 4, 90, 500),
(2, 3, 20, 2400), (2, 5, 80, 700), (2, 9, 10, 3500),
(3, 6, 35, 2700), (3, 8, 20, 2900), (3, 4, 90, 500),
(4, 2, 18, 2600), (4, 3, 16, 2400), (4, 5, 18, 700),
(5, 1, 12, 2500), (5, 4, 40, 500), (5, 5, 30, 700),
(6, 8, 18, 2900), (6, 9, 12, 3500), (6, 4, 36, 500),
(7, 1, 42, 2500), (7, 2, 30, 2600), (7, 10, 15, 3400),
(8, 6, 45, 2700), (8, 7, 30, 2600), (8, 4, 96, 500),
(9, 1, 48, 2500), (9, 2, 38, 2600), (9, 8, 22, 2900),
(10, 3, 34, 2400), (10, 6, 36, 2700), (10, 4, 84, 500),
(11, 6, 42, 2700), (11, 8, 32, 2900), (11, 9, 15, 3500),
(12, 2, 36, 2600), (12, 7, 34, 2600), (12, 5, 62, 700),
(13, 1, 22, 2500), (13, 2, 18, 2600), (13, 4, 70, 500),
(14, 3, 20, 2400), (14, 5, 45, 700), (14, 10, 10, 3400),
(15, 8, 16, 2900), (15, 9, 8, 3500), (15, 4, 42, 500),
(16, 1, 14, 2500), (16, 5, 30, 700), (16, 7, 10, 2600),
(17, 8, 20, 2900), (17, 6, 18, 2700), (17, 4, 40, 500),
(18, 2, 24, 2600), (18, 9, 16, 3500), (18, 5, 40, 700),
(19, 6, 30, 2700), (19, 8, 22, 2900), (19, 10, 12, 3400),
(20, 1, 55, 2500), (20, 6, 46, 2700), (20, 7, 38, 2600);

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
