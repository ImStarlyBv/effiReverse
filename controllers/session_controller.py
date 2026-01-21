"""
Session Controller
Handles session/cookie management endpoints
"""

from flask import jsonify
from services.session_service import session_service


class SessionController:
    
    @staticmethod
    def new_cookie():
        """POST /newcookie - Force refresh session cookie"""
        try:
            cookie = session_service.force_refresh()
            
            if cookie:
                return jsonify({
                    "success": True,
                    "message": "Cookie refreshed successfully",
                    "cookie_preview": f"{cookie[:20]}..."
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Failed to get new cookie"
                }), 500
                
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @staticmethod
    def status():
        """GET /session/status - Check session status"""
        try:
            cookie = session_service._load_cookie()
            is_valid = session_service._test_cookie(cookie) if cookie else False
            
            return jsonify({
                "success": True,
                "has_cookie": cookie is not None,
                "is_valid": is_valid,
                "cookie_preview": f"{cookie[:20]}..." if cookie else None
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
