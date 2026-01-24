# Effi Dropshipping API Reference

A robust RESTful API for managing dropshipping operations, including customer relationships, product inventories, and order fulfillment in the Effi ecosystem.

---

## Service Overview
- **Base URL:** `https://api.vibrarose.fun`
- **Content Type:** `application/json`
- **Session Management:** The system automatically manages session cookies via Playwright. Interactive login is triggered on demand or via the `/newcookie` endpoint.

---

## Operational Flow
To successfully place an order in the Effi system using this API, follow this logical sequence:

1.  **Authentication (`POST /newcookie`)**: Initialize or refresh the session. This is required before any other action.
2.  **Entity Discovery**:
    - **Products**: Use `GET /products` or `GET /products/search` to find the correct `articulo_id` and price for the items you want to sell.
    - **Customer**: Use `GET /customers/search` to check if the customer exists. If not, use `POST /customers` to create them.
3.  **Address Identification (`GET /customers/<id>/addresses`)**: Retrieve the specific address ID for the customer. Orders require a valid address reference.
4.  **Order Submission (`POST /orders`)**: Combine the gathered IDs (Customer ID, Address ID, Product ID) to submit the final order.

> [!TIP]
> Use the **`POST /orders/full`** endpoint to automate steps 2 and 3 in a single call if you already have the customer and product details.

---

## 1. Authentication & Session

### Force Session Refresh
Triggers a headless browser login to generate a fresh `ci_session` cookie. Use this if you encounter authentication errors or if the cookie file is missing.

- **URL:** `/newcookie`
- **Method:** `POST`
- **Response:**
  ```json
  {
    "success": true,
    "message": "Cookie refreshed successfully",
    "cookie_preview": "6h..."
  }
  ```

### Session Status
Checks if the current session cookie is valid.

- **URL:** `/session/status`
- **Method:** `GET`
- **Response:**
  ```json
  {
    "active": true,
    "success": true
  }
  ```

---

## 2. Customer Management

### List Customers
Retrieves a list of available customers from the Effi dashboard.

- **URL:** `/customers`
- **Method:** `GET`
- **Response:**
  ```json
  {
    "count": 4,
    "customers": [
      {
        "id": 23273,
        "nombre": "CLIENTE EJEMPLO",
        "documento": "123456789",
        "telefono": "8090000000",
        "t_precio": "1",
        "t_forma_pago": "2"
      }
    ],
    "success": true
  }
  ```

### Search Customers
Fine-grained search for specific customers using identifiers or contact info.

- **URL:** `/customers/search`
- **Method:** `GET`
- **Query Parameters:**
  - `nombre` (string): Full or partial name.
  - `phone` (string): Phone number or WhatsApp.
  - `id` (string): Internal Effi customer ID.
- **Example:** `/customers/search?phone=8091112233`

### Create Customer
Registers a new customer in the system.

- **URL:** `/customers`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "dni_number": "40212345678",
    "nombre": "Jane Doe",
    "email": "jane@example.com",
    "telefono": "8095551212",
    "direccion": "Calle Principal 123, frente al parque",
    "pais": 61,
    "provincia": 4131,
    "ciudad": 62304,
    "dni_type": 21
  }
  ```
> [!NOTE]
> `pais` (default 61), `provincia` (default 981), and `ciudad` (default 62304) use the IDs obtained from the `/locations` endpoints. The `direccion` field should contain the detailed street address and references.

### Get Customer Addresses
Retrieves all registered shipping addresses for a specific customer ID.

- **URL:** `/customers/<id>/addresses`
- **Method:** `GET`

---

## 3. Product Inventory

### List All Products
Fetches all articles/products available in the inventory.

- **URL:** `/products`
- **Method:** `GET`
- **Response Schema:**
  ```json
  {
    "count": 25,
    "products": [
      {
        "id": 26343,
        "codigo": "TIKTOK-01",
        "descripcion": "L TIK TOK - LUZ LED",
        "p_min_venta": "1200",
        "url_foto": "https://...",
        "image_url": "https://...",
        "dropshipping": true
      }
    ],
    "success": true
  }
  ```

### Global Search
Search products by name or description.

- **URL:** `/products/search?q=<query>`
- **Method:** `GET`

---

## 4. Order Fulfillment (Remisión)

### Simple Order Creation
Creates a new order (Remisión) for an existing customer.

- **URL:** `/orders`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "cliente_id": 23273,
    "direccion_cliente": 1,
    "items": [
      {
        "articulo_id": 26343,
        "descripcion": "L TIK TOK - LUZ LED",
        "cantidad": 2,
        "precio": 1200
      }
    ],
    "forma_pago": 2
  }
  ```

### Full Flow Ordering
Handles the end-to-end process: searches for the customer, creates them if they don't exist, retrieves their primary address, and submits the order.

- **URL:** `/orders/full`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "dni_number": "40212345678",
    "nombre": "Jane Doe",
    "email": "jane@example.com",
    "telefono": "8095551212",
    "items": [
      {
        "articulo_id": 26343,
        "cantidad": 1,
        "precio": 1200
      }
    ]
  }
  ```

---

## 5. Location Discovery (Dynamic Forms)

### List Provinces
Retrieves all provinces for a country.

- **URL:** `/locations/provinces`
- **Method:** `GET`
- **Query Parameters:**
  - `pais_id` (int, default: 61): Country ID.
- **Example Response:**
  ```json
  {
    "count": 32,
    "provinces": [
      { "id": "4131", "nombre": "4131 - Santo Domingo" },
      { "id": "1006", "nombre": "1006 - Santiago" }
    ],
    "success": true
  }
  ```

### List Cities
Retrieves all cities for a specific province. Use this to populate the `ciudad` field when creating a customer.

- **URL:** `/locations/cities`
- **Method:** `GET`
- **Query Parameters:**
  - `provincia_id` (int, required): The ID of the province.
- **Example Response:**
  ```json
  {
    "cities": [
      { "id": "62304", "nombre": "62304 - SANTO DOMINGO" }
    ],
    "count": 1,
    "success": true
  }
  ```

---

## Error Handling
The API returns standard HTTP status codes and a JSON error object:

```json
{
  "success": false,
  "error": "Short description of error",
  "details": { "technical": "Optional deeper context" }
}
```
- `400 Bad Request`: Missing required fields or invalid data.
- `404 Not Found`: Resource not found.
- `500 Internal Server Error`: Server-side exception.
