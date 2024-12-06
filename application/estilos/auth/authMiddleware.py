from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
from application.estilos.modelos.usuarioModel import Usuario

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])                        
            current_user=Usuario.get_by_id(data["usu_id"])
            if current_user is None:
                return {
                "message": " Authentication invalida de token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
            
            if not current_user.usu_estado:
                return {
                "message": "El usuario ya cerró sesión, inicie la sesión nuevamente",
                "data": None,                
            }, 500
        except Exception as e:
            return {
                "message": "Error desconocido",
                "data": None,
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated