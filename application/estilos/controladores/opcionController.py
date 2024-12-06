from flask_restful import Resource
from application.estilos.modelos.opcionModel import Opcion, OpcionSchema
from flask import request
from application.utils.response import Response
from marshmallow import ValidationError
from application.estilos.auth.authMiddleware import token_required
class OpcionController(Resource):    
    def __init__(self):
        super().__init__()
        self.schemaMany = OpcionSchema(many=True)
        self.schemaOne = OpcionSchema()
    
    @token_required
    def get(current_user, self):        
        try:      
            consulta = Opcion.get_all()                  
            data = self.schemaMany.dump(consulta)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(mensaje='Error Obtener datos DB',error=str(e), status=500)    
    
    @token_required
    def post(current_user, self):        
        try:
            opcionJson = request.get_json()
            opcionSchema = self.schemaOne.load(opcionJson)
            opcion = Opcion(
                est_id=opcionSchema['est_id'],
                opc_texto=opcionSchema['opc_texto'],
                opc_valor_cualitativo=opcionSchema['opc_valor_cualitativo'],
                opc_valor_cuantitativo=opcionSchema['opc_valor_cuantitativo'],
                pre_id=opcionSchema['pre_id'],
            )
            opcion.save()
            data = self.schemaOne.dump(opcion)            
            return Response.ok(data=data, mensaje="Creado", status=201)
        except KeyError as e:
            return Response.error(mensaje='Faltan campos obligatorios', error=f"Falta el campo obligatorio '{e.args[0]}'." , status=400)
        except ValidationError as e:
            return Response.error(mensaje='Error de validación, campo incorrecto', error=e.messages, status=400)
        except Exception as e:
            return Response.error(error=str(e))

class OpcionWithIdController(Resource):    
    def __init__(self):
        super().__init__()
        self.schemaOne = OpcionSchema()
    
    @token_required
    def get(current_user, self, opc_id):        
        try:
            consulta = Opcion.get_by_id(opc_id)
            data = self.schemaOne.dump(consulta)
            if not data:
                return Response.error(mensaje="No data", error='No existe una opcion con ese id', status=404)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))        
    
    @token_required
    def delete(current_user, self, opc_id):
        try:
            data = Opcion.get_by_id(opc_id)            
            if not data:
                return Response.error(mensaje="No data", error='No existe una opcion con ese id', status=404)
            data.delete()
            return Response.ok(status=204)
        except Exception as e:
            return Response.error(error=str(e))        
    
    @token_required
    def put(current_user, self, opc_id):
        try:
            opcion = Opcion.get_by_id(opc_id)
            if not opcion:
                return Response.error(mensaje="No data", error='No existe una opcion con ese id', status=404)
            opcion.est_id=request.json['est_id']
            opcion.opc_texto=request.json['opc_texto']
            opcion.opc_valor_cualitativo=request.json['opc_valor_cualitativo']
            opcion.opc_valor_cuantitativo=request.json['opc_valor_cuantitativo']
            opcion.pre_id=request.json['pre_id']
            opcion.save()            
            return Response.ok(mensaje="Actualizado", data=self.schemaOne.dump(opcion))
        except KeyError as e:
            return Response.error(mensaje='Faltan campos obligatorios', error=f"Falta el campo obligatorio '{e.args[0]}'." , status=400)
        except ValidationError as e:
            return Response.error(mensaje='Error de validación, campo incorrecto', error=e.messages, status=400)
        except Exception as e:
            return Response.error(error=str(e))
    