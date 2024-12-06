from flask_restful import Resource
from application.estilos.modelos.preguntaModel import Pregunta, PreguntaSchema
from flask import request
from application.utils.response import Response
from marshmallow import ValidationError
from application.estilos.auth.authMiddleware import token_required

class PreguntaController(Resource):    
    def __init__(self):
        super().__init__()
        self.schemaMany = PreguntaSchema(many=True)
        self.schemaOne = PreguntaSchema()
    
    @token_required
    def get(current_user, self):
        try:                        
            consulta = Pregunta.get_all()
            data = self.schemaMany.dump(consulta)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(mensaje='Error Obtener datos DB',error=str(e), status=500)    
    
    @token_required
    def post(current_user, self):        
        try:
            preguntaJson = request.get_json()
            preguntaSchema = self.schemaOne.load(preguntaJson)
            pregunta = Pregunta(
                enc_id=preguntaSchema['enc_id'],
                pre_enunciado=preguntaSchema['pre_enunciado'],
                pre_num_respuestas_max=preguntaSchema['pre_num_respuestas_max'],
                pre_num_respuestas_min=preguntaSchema['pre_num_respuestas_min'],
                pre_orden=preguntaSchema['pre_orden'],
                pre_tipo_pregunta=preguntaSchema['pre_tipo_pregunta'],
                pre_valor_total=preguntaSchema['pre_valor_total'],
            )
            pregunta.save()
            data = self.schemaOne.dump(pregunta)
            return Response.ok(data=data, mensaje="Creado", status=201)
        except KeyError as e:
            return Response.error(mensaje='Faltan campos obligatorios', error=f"Falta el campo obligatorio '{e.args[0]}'." , status=400)
        except ValidationError as e:
            return Response.error(mensaje='Error de validación, campo incorrecto', error=e.messages, status=400)
        except Exception as e:
            return Response.error(error=str(e))

class PreguntaWithIdController(Resource):    
    def __init__(self):
        super().__init__()
        self.schemaOne = PreguntaSchema()
    
    @token_required
    def get(current_user, self, pre_id):
        try:
            consulta = Pregunta.get_by_id(pre_id)
            data = self.schemaOne.dump(consulta)
            if not data:
                return Response.error(mensaje="No data", error='No existe una pregunta con ese id', status=404)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))
    
    @token_required
    def delete(current_user, self, pre_id):
        try:
            data = Pregunta.get_by_id(pre_id)            
            if not data:
                return Response.error(mensaje="No data", error='No existe una pregunta con ese id', status=404)
            return Response.ok(status=204)
        except Exception as e:
            return Response.error(error=str(e))
    
    @token_required
    def put(current_user, self, pre_id):       
        try:
            pregunta = Pregunta.get_by_id(pre_id)
            if not pregunta:
                return Response.error(mensaje="No data", error='No existe una pregunta con ese id', status=404)
            pregunta.enc_id=request.json['enc_id']
            pregunta.pre_enunciado=request.json['pre_enunciado']
            pregunta.pre_num_respuestas_max=request.json['pre_num_respuestas_max']
            pregunta.pre_num_respuestas_min=request.json['pre_num_respuestas_min']
            pregunta.pre_orden=request.json['pre_orden']
            pregunta.pre_tipo_pregunta=request.json['pre_tipo_pregunta']
            pregunta.pre_valor_total=request.json['pre_valor_total']
            pregunta.save()            
            return Response.ok(mensaje="Actualizado", data=self.schemaOne.dump(pregunta))
        except KeyError as e:
            return Response.error(mensaje='Faltan campos obligatorios', error=f"Falta el campo obligatorio '{e.args[0]}'." , status=400)
        except ValidationError as e:
            return Response.error(mensaje='Error de validación, campo incorrecto', error=e.messages, status=400)
        except Exception as e:
            return Response.error(error=str(e))
    