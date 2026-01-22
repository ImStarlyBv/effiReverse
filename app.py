"""
EFFI Dropshipping API
=====================
RESTful API for managing customers and orders in Effi system.
MVC Pattern with auto session management.

Run:
    python app.py

Endpoints:
    GET  /health              - Health check
    POST /newcookie           - Force refresh session cookie
    
    GET  /customers           - List all customers
    GET  /customers/search    - Search customers by phone/name
    POST /customers           - Create new customer
    GET  /customers/<id>/addresses - Get customer addresses
    
    POST /orders              - Create order (remision)
    POST /orders/full         - Full flow: create customer + order
"""

from flask import Flask
from routes.customer_routes import customer_bp
from routes.order_routes import order_bp
from routes.session_routes import session_bp
from routes.product_routes import product_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(session_bp, url_prefix='')
app.register_blueprint(customer_bp, url_prefix='/customers')
app.register_blueprint(order_bp, url_prefix='/orders')
app.register_blueprint(product_bp, url_prefix='/products')


@app.route('/health', methods=['GET'])
def health():
    return {"status": "ok", "service": "effi-api"}


import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
