
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from app import app

def verify_cors():
    print("Verifying CORS configuration...")
    client = app.test_client()
    
    # Test /health endpoint
    response = client.get('/health')
    print(f"Status: {response.status_code}")
    
    cors_header = response.headers.get('Access-Control-Allow-Origin')
    print(f"Access-Control-Allow-Origin: {cors_header}")
    
    if cors_header == '*':
        print("SUCCESS: CORS is enabled and allowing all origins.")
    else:
        print("FAILURE: CORS header missing or incorrect.")

if __name__ == "__main__":
    verify_cors()
