
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from services.session_service import session_service
from config import ENDPOINTS

def debug_locations():
    # Try POST
    print("Testing GET /app/general/llena_provincia with pais=61")
    res_get = session_service.make_request("/app/general/llena_provincia", {"pais": 61}, method="GET")
    print(f"GET Status: {res_get.status_code}")
    print(f"GET Length: {len(res_get.text)}")
    
    print("\nTesting POST /app/general/llena_provincia with pais=61")
    res_post = session_service.make_request("/app/general/llena_provincia", {"pais": 61}, method="POST")
    print(f"POST Status: {res_post.status_code}")
    print(f"POST Length: {len(res_post.text)}")
    if len(res_post.text) > 100:
        print(f"POST Preview: {res_post.text[:200]}")

    print("\nTesting GET /app/general/llena_ciudad with provincia=4131")
    res_c_get = session_service.make_request("/app/general/llena_ciudad", {"provincia": 4131}, method="GET")
    print(f"GET Status: {res_c_get.status_code}")
    print(f"GET Length: {len(res_c_get.text)}")
    print(f"GET Preview: {res_c_get.text[:200]}")

    print("\nTesting POST /app/general/llena_ciudad with provincia=4131")
    res_c_post = session_service.make_request("/app/general/llena_ciudad", {"provincia": 4131}, method="POST")
    print(f"POST Status: {res_c_post.status_code}")
    print(f"POST Length: {len(res_c_post.text)}")
    print(f"POST Preview: {res_c_post.text[:200]}")

if __name__ == "__main__":
    debug_locations()
