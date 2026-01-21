"""
Session Routes
"""

from flask import Blueprint
from controllers.session_controller import SessionController

session_bp = Blueprint('session', __name__)

# POST /newcookie - Force refresh cookie
session_bp.route('/newcookie', methods=['POST'])(SessionController.new_cookie)

# GET /session/status - Check session status
session_bp.route('/session/status', methods=['GET'])(SessionController.status)
