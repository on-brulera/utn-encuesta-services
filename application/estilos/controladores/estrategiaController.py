from flask_restful import Resource
from application.estilos.modelos.estrategiaModel import Estrategia, EstrategiaSchema
from flask import request
from application.utils.response import Response
from marshmallow import ValidationError
from application.estilos.auth.authMiddleware import token_required

class EstrategiaController(Resource):    
    def __init__(self):
        super().__init__()
        self.schemaMany = EstrategiaSchema(many=True)
        self.schemaOne = EstrategiaSchema()
    
    @token_required
    def get(current_user, self):         
        try:            
            consulta = Estrategia.get_all()
            data = self.schemaMany.dump(consulta)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(mensaje='Error Obtener datos DB',error=str(e), status=500)    
        
    @token_required
    def post(current_user, self):
        try:
            estrategiaJson = request.get_json()
            estrategiaSchema = self.schemaOne.load(estrategiaJson)
            estrategia = Estrategia(                
                est_id = estrategiaSchema['est_id'],
                cur_id = estrategiaSchema['cur_id'],
                cur_nivel = estrategiaSchema['cur_nivel'],
                prom_notas = estrategiaSchema['prom_notas'],
                enc_id = estrategiaSchema['enc_id'],
                mat_id = estrategiaSchema['mat_id'],
                estr_estrategia = estrategiaSchema['estr_estrategia']                
            )            

            estrategia.save()
            data = self.schemaOne.dump(estrategia)
            return Response.ok(data=data, mensaje="Creado", status=201)
        except KeyError as e:
            return Response.error(mensaje='Faltan campos obligatorios', error=f"Falta el campo obligatorio '{e.args[0]}'." , status=400)
        except ValidationError as e:
            return Response.error(mensaje='Error de validación, campo incorrecto', error=e.messages, status=400)
        except Exception as e:
            return Response.error(error=str(e))
        
        

class EstrategiaWithIdController(Resource):    
    def __init__(self):
        super().__init__()
        self.schemaOne = EstrategiaSchema()
    
    @token_required
    def get(current_user, self, estr_id):
        try:
            consulta = Estrategia.get_by_id(estr_id)
            data = self.schemaOne.dump(consulta)
            if not data:
                return Response.error(mensaje="No data", error='No existe una estrategia con ese id', status=404)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))
            
    @token_required
    def delete(current_user, self, estr_id):
        try:
            estrategia = Estrategia.get_by_id(estr_id)
            if not estrategia:
                return Response.error(mensaje="No data", error='No existe una estrategia con ese id', status=404)
            estrategia.delete()
            return Response.ok(status=204)
        except Exception as e:
            return Response.error(error=str(e))    
    
    @token_required
    def put(current_user, self, estr_id):
        try:
            estrategia = Estrategia.get_by_id(estr_id)
            if not estrategia:
                return Response.error(mensaje="No data", error='No existe una estrategia con ese id', status=404)            
            estrategia.est_id=request.json['est_id']
            estrategia.cur_id=request.json['cur_id']
            estrategia.cur_nivel=request.json['cur_nivel']
            estrategia.prom_notas=request.json['prom_notas']
            estrategia.enc_id=request.json['enc_id']
            estrategia.mat_id=request.json['mat_id']
            estrategia.estr_estrategia=request.json['estr_estrategia']                        
            estrategia.save()
            data = self.schemaOne.dump(estrategia)
            return Response.ok(data=data, mensaje="Actualizado")
        except KeyError as e:
            return Response.error(mensaje='Faltan campos obligatorios', error=f"Falta el campo obligatorio '{e.args[0]}'." , status=400)
        except ValidationError as e:
            return Response.error(mensaje='Error de validación, campo incorrecto', error=e.messages, status=400)
        except Exception as e:
            return Response.error(error=str(e))
        

class EstrategiaWithAllFieldsController(Resource):    
    def __init__(self):
        super().__init__()
        self.schemaOne = EstrategiaSchema()
    
    @token_required
    def post(current_user, self):
        try:
            filters = request.get_json()  # Obtén los filtros enviados en el JSON
            estrategia = Estrategia.filter_one_by_fields(
                est_id=filters.get("est_id"),
                cur_id=filters.get("cur_id"),
                cur_nivel=filters.get("cur_nivel"),
                enc_id=filters.get("enc_id"),
                mat_id=filters.get("mat_id")
            )
            if not estrategia:
                return Response.error(mensaje="No se encontró una estrategia con esos filtros", status=404)

            data = EstrategiaSchema().dump(estrategia)
            return Response.ok(data=data, mensaje="Estrategia encontrada", status=200)
        except Exception as e:
            return Response.error(error=str(e))

    