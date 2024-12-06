from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from application.estilos.modelos.promptModel import Prompt, PromptSchema
from application.utils.response import Response
from application.estilos.auth.authMiddleware import token_required

class PromptController(Resource):    
    def __init__(self):
        super().__init__()
        self.schemaMany = PromptSchema(many=True)
        self.schemaOne = PromptSchema()
    
    @token_required
    def get(current_user, self):         
        try:            
            consulta = Prompt.get_all()
            data = self.schemaMany.dump(consulta)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(mensaje='Error al obtener datos de la BD', error=str(e), status=500)    
        
    @token_required
    def post(current_user, self):
        try:
            promptJson = request.get_json()
            promptSchema = self.schemaOne.load(promptJson)
            prompt = Prompt(
                pro_titulo=promptSchema['pro_titulo'],  # Asignación del nuevo campo
                pro_descripcion=promptSchema['pro_descripcion']
            )
            prompt.save()
            data = self.schemaOne.dump(prompt)
            return Response.ok(data=data, mensaje="Creado", status=201)
        except KeyError as e:
            return Response.error(mensaje='Faltan campos obligatorios', error=f"Falta el campo obligatorio '{e.args[0]}'." , status=400)
        except ValidationError as e:
            return Response.error(mensaje='Error de validación, campo incorrecto', error=e.messages, status=400)
        except Exception as e:
            return Response.error(error=str(e))

class PromptWithIdController(Resource):    
    def __init__(self):
        super().__init__()
        self.schemaOne = PromptSchema()
    
    @token_required
    def get(current_user, self, pro_id):
        try:
            consulta = Prompt.get_by_id(pro_id)
            data = self.schemaOne.dump(consulta)
            if not data:
                return Response.error(mensaje="No se encontró el prompt", error='No existe un prompt con ese ID', status=404)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))
    
    @token_required
    def delete(current_user, self, pro_id):
        try:
            prompt = Prompt.get_by_id(pro_id)
            if not prompt:
                return Response.error(mensaje="No data", error='No existe un prompt con ese ID', status=404)
            prompt.delete()
            return Response.ok(status=204)
        except Exception as e:
            return Response.error(error=str(e))    

    @token_required
    def put(current_user, self, pro_id):
        try:
            prompt = Prompt.get_by_id(pro_id)
            if not prompt:
                return Response.error(mensaje="No se encontró el prompt", error='No existe un prompt con ese ID', status=404)
            prompt.pro_titulo = request.json['pro_titulo']  # Actualización del nuevo campo
            prompt.pro_descripcion = request.json['pro_descripcion']
            prompt.save()
            return Response.ok(mensaje="Actualizado correctamente")
        except KeyError as e:
            return Response.error(mensaje='Faltan campos obligatorios', error=f"Falta el campo obligatorio '{e.args[0]}'." , status=400)
        except ValidationError as e:
            return Response.error(mensaje='Error de validación, campo incorrecto', error=e.messages, status=400)
        except Exception as e:
            return Response.error(error=str(e))
