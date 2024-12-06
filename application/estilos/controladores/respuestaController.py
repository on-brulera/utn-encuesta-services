from flask_restful import Resource
from application.estilos.modelos.respuestaModel import Respuesta, RespuestaSchema
from application.estilos.modelos.reglasCalculoModel import (ReglasCalculoSchema, ReglasCalculo)
from application.estilos.modelos.asignacionModel import (Asignacion, AsignacionSchema)
from flask import request
from application.utils.response import Response
from marshmallow import ValidationError
from application.estilos.auth.authMiddleware import token_required

class RespuestaController(Resource):    
    def __init__(self):
        super().__init__()
        self.schemaMany = RespuestaSchema(many=True)
        self.schemaOne = RespuestaSchema()
    
    @token_required
    def get(current_user, self):
        try:                        
            consulta = Respuesta.get_all()
            data = self.schemaMany.dump(consulta)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(mensaje='Error Obtener datos DB',error=str(e), status=500)    
    
    @token_required
    def post(current_user, self):
        try:
            respuestaJson = request.get_json()
            respuestaSchema = self.schemaOne.load(respuestaJson)
            respuesta = Respuesta(
                asi_id=respuestaSchema['asi_id'],
                opc_id=respuestaSchema['opc_id'],
                pre_id=respuestaSchema['pre_id'],
                usu_id=respuestaSchema['usu_id'],
                res_valor_cuantitativo=respuestaSchema['res_valor_cuantitativo']
            )
            respuesta.save()
            data = self.schemaOne.dump(respuesta)
            return Response.ok(data=data, mensaje="Creado", status=201)
        except KeyError as e:
            return Response.error(mensaje='Faltan campos obligatorios', error=f"Falta el campo obligatorio '{e.args[0]}'." , status=400)
        except ValidationError as e:
            return Response.error(mensaje='Error de validación, campo incorrecto', error=e.messages, status=400)
        except Exception as e:
            return Response.error(error=str(e))        

class RespuestaWithIdController(Resource):    
    def __init__(self):
        super().__init__()
        self.schemaOne = RespuestaSchema()
    
    @token_required
    def get(current_user, self, res_id):
        try:
            consulta = Respuesta.get_by_id(res_id)
            data = self.schemaOne.dump(consulta)
            if not data:
                return Response.error(mensaje="No data", error='No existe respuesta con ese id', status=404)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))
    
    @token_required
    def delete(current_user, self, res_id):
        try:
            data = Respuesta.get_by_id(res_id)            
            if not data:
                return Response.error(mensaje="No data", error='No existe respuesta con ese id', status=404)
            data.delete()
            return Response.ok(status=204)
        except Exception as e:
            return Response.error(error=str(e))
        
    @token_required
    def put(current_user, self, res_id):
        try:
            respuesta = Respuesta.get_by_id(res_id)
            if not respuesta:
                return Response.error(mensaje="No data", error='No existe respuesta con ese id', status=404)
            respuesta.asi_id=request.json['asi_id']        
            respuesta.opc_id=request.json['opc_id']        
            respuesta.pre_id=request.json['pre_id']        
            respuesta.usu_id=request.json['usu_id']        
            respuesta.save()            
            return Response.ok(mensaje="Actualizado", data=self.schemaOne.dump(respuesta))
        except KeyError as e:
            return Response.error(mensaje='Faltan campos obligatorios', error=f"Falta el campo obligatorio '{e.args[0]}'." , status=400)
        except ValidationError as e:
            return Response.error(mensaje='Error de validación, campo incorrecto', error=e.messages, status=400)
        except Exception as e:
            return Response.error(error=str(e))

class RespuestaWithasi_id(Resource):    
    def __init__(self):
        super().__init__()
        self.schemaMany = RespuestaSchema(many=True)
        self.schemaOne = RespuestaSchema()
        self.schemaReglas = ReglasCalculoSchema(many=True)
        self.schemaAsignacion = AsignacionSchema(many=True)
    
    @token_required
    def post(current_user, self,asi_id):
        try:
            asignacion = Asignacion.query.filter_by(asi_id=asi_id).all()
            asignacion_data = self.schemaAsignacion.dump(asignacion)
            
            respuestas = Respuesta.query.filter_by(asi_id=asi_id).all()
            respuestas_data = self.schemaMany.dump(respuestas)
            
            reglas = ReglasCalculo.query.filter_by(enc_id=asignacion_data[0]['enc_id'])
            reglas_data = self.schemaReglas.dump(reglas)

            response_data = {
                'respuestas': respuestas_data,
                'reglas_json': reglas_data,
                'idAsignacion': asi_id
            }
            
            return Response.ok(data=response_data)
        
        except ValidationError as e:
            return Response.error(mensaje='Error de validación', error=e.messages, status=400)
        except Exception as e:
            return Response.error(error=str(e))
    