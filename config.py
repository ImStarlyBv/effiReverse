"""
Configuration
"""
import os

# Effi URLs
BASE_URL = "https://effi.com.co"
LOGIN_URL = f"{BASE_URL}/ingreso"

# Endpoints
ENDPOINTS = {
    "create_customer": "/app/tercero/cliente/crearCliente",
    "search_customers": "/app/tercero/cliente/llena_cliente_buscar",
    "get_addresses": "/app/tercero/tercero/llena_direccion_tercero",
    "create_remision": "/app/remision_v/crear",
}

# Credentials
EMAIL = os.getenv("EFFI_EMAIL", "l_urbaez@yahoo.com")
PASSWORD = os.getenv("EFFI_PASSWORD", "DV2TE.e3kFp5anR")

# Session
COOKIE_FILE = os.getenv("COOKIE_FILE", "effi_session.txt")

# Defaults
DEFAULT_CONVENIO_DROPSHIPPING = "tmuKRh3b"
DEFAULT_SESSION_EMPRESA = "48745"
DEFAULT_RESPONSABLE = EMAIL

# Request headers
HEADERS = {
    "accept": "*/*",
    "accept-language": "es-US,es;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": BASE_URL,
    "referer": f"{BASE_URL}/app/remision_v",
    "x-requested-with": "XMLHttpRequest",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
