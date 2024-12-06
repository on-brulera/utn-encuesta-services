from flask_restful import Resource
from application.estilos.modelos.rolModel import Rol, RolSchema
from flask import request
from application.utils.response import Response
from marshmallow import ValidationError
from application.estilos.auth.authMiddleware import token_required

class RolController(Resource):    
    def __init__(self):
        super().__init__()
        self.schemaMany = RolSchema(many=True)
        self.schemaOne = RolSchema()
    
    @token_required
    def get(current_user, self):         
        try:            
            consulta = Rol.get_all()
            data = self.schemaMany.dump(consulta)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(mensaje='Error Obtener datos DB',error=str(e), status=500)    
        
    @token_required
    def post(current_user, self):
        try:
            rolJson = request.get_json()
            rolSchema = self.schemaOne.load(rolJson)
            rol = Rol(
                rol_id=rolSchema['rol_id'],
                rol_nombre=rolSchema['rol_nombre'],
                rol_descripcion=rolSchema['rol_descripcion']
            )

            consulta = Rol.get_by_id(rolSchema['rol_id'])
            if consulta:
                return Response.error(mensaje='Ya existe un rol con ese código', error='Rol existente', status=400)

            rol.save()
            data = self.schemaOne.dump(rol)
            return Response.ok(data=data, mensaje="Creado", status=201)
        except KeyError as e:
            return Response.error(mensaje='Faltan campos obligatorios', error=f"Falta el campo obligatorio '{e.args[0]}'." , status=400)
        except ValidationError as e:
            return Response.error(mensaje='Error de validación, campo incorrecto', error=e.messages, status=400)
        except Exception as e:
            return Response.error(error=str(e))
        
        

class RolWithIdController(Resource):    
    def __init__(self):
        super().__init__()
        self.schemaOne = RolSchema()
    
    @token_required
    def get(current_user, self, rol_id):
        try:
            consulta = Rol.get_by_id(rol_id)
            data = self.schemaOne.dump(consulta)
            if not data:
                return Response.error(mensaje="No data", error='No existe un rol con ese id', status=404)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))
            
    @token_required
    def delete(current_user, self, rol_id):
        try:
            rol = Rol.get_by_id(rol_id)
            if not rol:
                return Response.error(mensaje="No data", error='No existe un rol con ese id', status=404)
            rol.delete()
            return Response.ok(status=204)
        except Exception as e:
            return Response.error(error=str(e))    
    
    @token_required
    def put(current_user, self, rol_id):
        try:
            rol = Rol.get_by_id(rol_id)
            if not rol:
                return Response.error(mensaje="No data", error='No existe un rol con ese id', status=404)
            rol.rol_id=request.json['rol_id']
            rol.rol_nombre=request.json['rol_nombre']
            rol.rol_descripcion=request.json['rol_descripcion']
            rol.save()
            data = self.schemaOne.dump(rol)
            return Response.ok(data=data, mensaje="Actualizado")
        except KeyError as e:
            return Response.error(mensaje='Faltan campos obligatorios', error=f"Falta el campo obligatorio '{e.args[0]}'." , status=400)
        except ValidationError as e:
            return Response.error(mensaje='Error de validación, campo incorrecto', error=e.messages, status=400)
        except Exception as e:
            return Response.error(error=str(e))
    