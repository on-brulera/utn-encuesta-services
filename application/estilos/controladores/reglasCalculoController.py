from flask_restful import Resource
from application.estilos.modelos.reglasCalculoModel import ReglasCalculoSchema, ReglasCalculo
from flask import request
from application.utils.response import Response
from marshmallow import ValidationError
from application.estilos.auth.authMiddleware import token_required

class ReglasCalculoController(Resource):    
    def __init__(self):
        super().__init__()
        self.schemaMany = ReglasCalculoSchema(many=True)
        self.schemaOne = ReglasCalculoSchema()
    
    @token_required
    def get(current_user, self):
        try:                        
            consulta = ReglasCalculo.get_all()
            data = self.schemaMany.dump(consulta)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(mensaje='Error Obtener datos DB',error=str(e), status=500)    
    
    @token_required
    def post(current_user, self):
        try:
            reglasJson = request.get_json()
            reglasSchema = self.schemaOne.load(reglasJson)
            regla = ReglasCalculo(
                enc_id=reglasSchema['enc_id'],
                reglas_json=reglasSchema['reglas_json'],
            )
            regla.save()
            data = self.schemaOne.dump(regla)    
            return Response.ok(data=data, mensaje="Creado", status=201)
        except KeyError as e:
            return Response.error(mensaje='Faltan campos obligatorios', error=f"Falta el campo obligatorio '{e.args[0]}'." , status=400)
        except ValidationError as e:
            return Response.error(mensaje='Error de validación, campo incorrecto', error=e.messages, status=400)
        except Exception as e:
            return Response.error(error=str(e))

class ReglasCalculoWithIdController(Resource):    
    def __init__(self):
        super().__init__()
        self.schemaOne = ReglasCalculoSchema()
    
    @token_required
    def get(current_user, self, reg_id):
        try:
            consulta = ReglasCalculo.get_by_id(reg_id)    
            data = self.schemaOne.dump(consulta)
            if not data:
                return Response.error(mensaje="No data", error='No existe una regla con ese id', status=404)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))
        
    @token_required
    def delete(current_user, self, reg_id):
        try:
            data = ReglasCalculo.get_by_id(reg_id)    
            if not data:
                return Response.error(mensaje="No data", error='No existe una regla con ese id', status=404)
            data.delete()
            return Response.ok(status=204)
        except Exception as e:
            return Response.error(error=str(e))
    
    @token_required
    def put(current_user, self, reg_id):       
        try:
            regla = ReglasCalculo.get_by_id(reg_id)
            if not regla:
                return Response.error(mensaje="No data", error='No existe una regla con ese id', status=404)
            regla.enc_id=request.json['enc_id']
            regla.reglas_json=request.json['reglas_json']
            regla.save()
            return Response.ok(mensaje="Actualizado", data=self.schemaOne.dump())
        except KeyError as e:
            return Response.error(mensaje='Faltan campos obligatorios', error=f"Falta el campo obligatorio '{e.args[0]}'." , status=400)
        except ValidationError as e:
            return Response.error(mensaje='Error de validación, campo incorrecto', error=e.messages, status=400)
        except Exception as e:
            return Response.error(error=str(e))
    