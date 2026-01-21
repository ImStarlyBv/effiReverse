# EFFI Dropshipping API

RESTful API para gestionar clientes y órdenes en el sistema Effi.

## Setup

### Local
```bash
pip install -r requirements.txt
playwright install chromium
python app.py
```

### Docker
```bash
docker-compose up -d
```

## Endpoints

### Session
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/newcookie` | Forzar refresh del session cookie |
| GET | `/session/status` | Ver estado de la sesión |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products` | Listar todos los productos |
| GET | `/products/search?q=X` | Buscar productos por nombre |
| GET | `/products/<id>` | Obtener producto por ID |

### Customers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/customers` | Listar todos los clientes |
| GET | `/customers/search?phone=X&nombre=Y` | Buscar clientes |
| POST | `/customers` | Crear cliente |
| GET | `/customers/<id>/addresses` | Obtener direcciones de un cliente |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/orders` | Crear orden (remisión) |
| POST | `/orders/full` | Flujo completo: cliente + orden |

---

## Ejemplos

### Listar Productos
```bash
curl http://localhost:5000/products
```

### Buscar Productos
```bash
curl "http://localhost:5000/products/search?q=rosa"
```

### Obtener Producto por ID
```bash
curl http://localhost:5000/products/3
```

### Crear Cliente
```bash
curl -X POST http://localhost:5000/customers \
  -H "Content-Type: application/json" \
  -d '{
    "dni_number": "123456789",
    "nombre": "Juan Pérez",
    "email": "juan@mail.com",
    "telefono": "8091234567"
  }'
```

### Buscar Cliente
```bash
curl "http://localhost:5000/customers/search?phone=8091234567"
```

### Obtener Direcciones
```bash
curl http://localhost:5000/customers/7/addresses
```

### Crear Orden Directa
```bash
curl -X POST http://localhost:5000/orders \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": 7,
    "direccion_cliente": 1,
    "items": [
      {
        "articulo_id": 3,
        "descripcion": "ROSA DEL PLACER VIBRADOR",
        "cantidad": 1,
        "precio": "2,500"
      }
    ]
  }'
```

### Crear Orden Completa (Auto-crea cliente si no existe)
```bash
curl -X POST http://localhost:5000/orders/full \
  -H "Content-Type: application/json" \
  -d '{
    "dni_number": "987654321",
    "nombre": "María López",
    "email": "maria@mail.com",
    "telefono": "8097654321",
    "items": [
      {
        "articulo_id": 3,
        "descripcion": "ROSA DEL PLACER VIBRADOR",
        "cantidad": 2,
        "precio": "2,500"
      }
    ]
  }'
```

### Refrescar Cookie
```bash
curl -X POST http://localhost:5000/newcookie
```

---

## Estructura MVC

```
effi_api/
├── app.py                 # Entry point
├── config.py              # Configuration
├── controllers/
│   ├── customer_controller.py
│   ├── order_controller.py
│   └── session_controller.py
├── services/
│   ├── customer_service.py
│   ├── order_service.py
│   └── session_service.py
├── routes/
│   ├── customer_routes.py
│   ├── order_routes.py
│   └── session_routes.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Session Management

El cookie de sesión se guarda automáticamente en `effi_session.txt`. Si el cookie expira, el sistema automáticamente hace login y obtiene uno nuevo.

Para forzar un nuevo cookie manualmente:
```bash
curl -X POST http://localhost:5000/newcookie
```
