from functools import wraps
from flask import request, jsonify
import os

API_KEYS = os.getenv("API_KEYS").split(",")

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if api_key not in API_KEYS:
            return jsonify({"error": "Forbidden: Invalid API key"}), 403
        return f(*args, **kwargs)
    return decorated_function