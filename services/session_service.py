"""
Session Service
Handles cookie management and auto-login with Playwright
"""

import os
import time
import requests
from config import (
    BASE_URL, LOGIN_URL, COOKIE_FILE, 
    EMAIL, PASSWORD, HEADERS, ENDPOINTS
)


class SessionService:
    _instance = None
    _cookie = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._cookie = cls._instance._load_cookie()
        return cls._instance
    
    @property
    def cookie(self):
        if not self._cookie or not self._test_cookie(self._cookie):
            self._cookie = self._login()
        return self._cookie
    
    def force_refresh(self):
        """Force a new login regardless of current cookie state"""
        self._cookie = self._login()
        return self._cookie
    
    def _save_cookie(self, cookie: str):
        with open(COOKIE_FILE, 'w') as f:
            f.write(cookie)
    
    def _load_cookie(self) -> str:
        if os.path.exists(COOKIE_FILE):
            with open(COOKIE_FILE, 'r') as f:
                cookie = f.read().strip()
                if cookie:
                    return cookie
        return None
    
    def _test_cookie(self, cookie: str) -> bool:
        """Test if cookie is still valid"""
        try:
            cookies = {"ci_session": cookie}
            response = requests.post(
                f"{BASE_URL}{ENDPOINTS['search_customers']}",
                headers=HEADERS,
                cookies=cookies,
                data={"id": "", "nombre": "", "celular_whatsapp": ""},
                timeout=10
            )
            return response.status_code == 200 and 'data-codigo' in response.text
        except:
            return False
    
    def _login(self) -> str:
        """Login using Playwright and get session cookie"""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise Exception("Playwright not installed. Run: pip install playwright && playwright install chromium")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            
            context = browser.new_context(user_agent=HEADERS["user-agent"])
            page = context.new_page()
            
            try:
                page.goto(LOGIN_URL, wait_until="networkidle")
                page.fill("#email", EMAIL)
                page.fill("#password", PASSWORD)
                page.click('button:has-text("Ingresar")')
                page.wait_for_load_state("networkidle")
                time.sleep(2)
                
                cookies = context.cookies()
                for cookie in cookies:
                    if cookie['name'] == 'ci_session':
                        self._save_cookie(cookie['value'])
                        return cookie['value']
                
                raise Exception("No session cookie found after login")
                
            except Exception as e:
                raise Exception(f"Login failed: {str(e)}")
            finally:
                browser.close()
    
    def make_request(self, endpoint: str, data, method: str = "POST"):
        """Make authenticated request with auto-retry on session expiry"""
        cookies = {"ci_session": self.cookie}
        
        if method == "POST":
            response = requests.post(
                f"{BASE_URL}{endpoint}",
                headers=HEADERS,
                cookies=cookies,
                data=data,
                timeout=30
            )
        else:
            response = requests.get(
                f"{BASE_URL}{endpoint}",
                headers=HEADERS,
                cookies=cookies,
                params=data,
                timeout=30
            )
        
        # Check if session expired
        if 'ingreso' in response.url or response.status_code == 302:
            # Refresh cookie and retry
            self._cookie = self._login()
            cookies = {"ci_session": self._cookie}
            
            if method == "POST":
                response = requests.post(
                    f"{BASE_URL}{endpoint}",
                    headers=HEADERS,
                    cookies=cookies,
                    data=data,
                    timeout=30
                )
            else:
                response = requests.get(
                    f"{BASE_URL}{endpoint}",
                    headers=HEADERS,
                    cookies=cookies,
                    params=data,
                    timeout=30
                )
        
        return response


# Singleton instance
session_service = SessionService()
