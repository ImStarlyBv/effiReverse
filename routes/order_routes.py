"""
Order Routes
"""

from flask import Blueprint
from controllers.order_controller import OrderController

order_bp = Blueprint('orders', __name__)

# POST /orders - Create order
order_bp.route('', methods=['POST'])(OrderController.create)

# POST /orders/full - Full flow (customer + order)
order_bp.route('/full', methods=['POST'])(OrderController.create_full)
