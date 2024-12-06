from flask_restful import Resource
from application.estilos.modelos.usuarioModel import Usuario, UsuarioSchema
from flask import app, request
from marshmallow import ValidationError
from application.utils.response import Response
import bcrypt
import jwt
import os


class LoginController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaMany = UsuarioSchema(many=True)
        self.schemaOne = UsuarioSchema()
        self.model = Usuario        
    
    def post(self):
        try:
            data = request.json
            if not data:
                return {
                    "message": "Please provide user details: usu_usuario, usu_password",
                    "data": None,
                    "error": "Bad request"
                }, 400
            is_validated = True if ("usu_usuario" in data and "usu_password" in data) else False
            if is_validated is not True:
                return dict(message='Invalid data, provide: usu_usuario, usu_password', data=None, error=is_validated), 400            

            usuario=request.json.get('usu_usuario')
            password=request.json.get('usu_password')
          
            consulta = self.model.query.filter(self.model.usu_usuario==usuario and self.model.usu_password==password).first()            
            if not consulta:
                return Response.error(mensaje="ingrese un usuario existente", error='El usuario no existe en la BDD')
            
            user=self.schemaOne.dump(consulta)            
            if  not bcrypt.checkpw(
                    request.json.get('usu_password').encode('utf-8'),
                    user['usu_password'].encode('utf-8')
                    ):
                return {
                        "error": "Error de credencial",
                        "message": 'contraseña incorrecta'
                    }, 401
            
            try:              
                    token = jwt.encode(
                        {"usu_id": user['usu_id']},
                        os.environ.get('SECRET_KEY'),
                        algorithm="HS256"
                    )                    
                    consulta.usu_estado=True
                    consulta.save()
                    user=self.schemaOne.dump(consulta)
                    user["token"] = token
                    return {
                        "message": "Successfully token",
                        "data": user
                    }
            except Exception as e:
                    return {
                        "error": "Error al crear el token",
                        "message": str(e)
                    }, 500
                        
        except KeyError as e:
            return Response.error(mensaje='Faltan campos obligatorios', error=f"Falta el campo obligatorio '{e.args[0]}'." , status=400)
        except ValidationError as e:
            return Response.error(mensaje='Error de validación, campo incorrecto', error=e.messages, status=400)
        except Exception as e:
            return Response.error(error=str(e))

class LogoutController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaMany = UsuarioSchema(many=True)
        self.schemaOne = UsuarioSchema()        
    
    def get(self, usu_id):
        user = Usuario.get_by_id(usu_id)
        if not user:
                return Response.error(mensaje="ingrese un usuario existente", error='El usuario no existe en la BDD')
        if user.usu_estado==False:
                return Response.error(mensaje="El usuario ya cerró sesión previamente", error='sesión terminada')
        user.usu_estado=False
        user.save()
        return Response.ok(data='Se cerró la sessión correctamente')