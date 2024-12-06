from flask_restful import Resource
from application.estilos.modelos.asignacionModel import Asignacion
from application.estilos.modelos.encuestaModel import EncuestaSchema, Encuesta
from application.estilos.modelos.reglasCalculoModel import (
    ReglasCalculoSchema,
    ReglasCalculo,
)
from application.estilos.modelos.preguntaModel import PreguntaSchema, Pregunta
from application.estilos.modelos.estilosModel import EstiloSchema, Estilo
from application.estilos.modelos.opcionModel import OpcionSchema, Opcion
from flask import request
from application.utils.response import Response
from marshmallow import ValidationError
from application.estilos.auth.authMiddleware import token_required


class EncuestaController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaMany = EncuestaSchema(many=True)
        self.schemaOne = EncuestaSchema()

    @token_required
    def get(current_user, self):
        try:
            consulta = Encuesta.get_all()
            data = self.schemaMany.dump(consulta)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(
                mensaje="Error Obtener datos DB", error=str(e), status=500
            )

    @token_required
    def post(current_user, self):
        try:
            encuestaJson = request.get_json()
            encuestaSchema = self.schemaOne.load(encuestaJson)
            encuesta = Encuesta(
                enc_autor=encuestaSchema["enc_autor"],
                enc_cuantitativa=encuestaSchema["enc_cuantitativa"],
                enc_descripcion=encuestaSchema["enc_descripcion"],
                enc_fecha_creacion=encuestaSchema["enc_fecha_creacion"],
                enc_titulo=encuestaSchema["enc_titulo"],
            )
            encuesta.save()
            data = self.schemaOne.dump(encuesta)
            return Response.ok(data=data, mensaje="Creado", status=201)
        except KeyError as e:
            return Response.error(
                mensaje="Faltan campos obligatorios",
                error=f"Falta el campo obligatorio '{e.args[0]}'.",
                status=400,
            )
        except ValidationError as e:
            return Response.error(
                mensaje="Error de validación, campo incorrecto",
                error=e.messages,
                status=400,
            )
        except Exception as e:
            return Response.error(error=str(e))


class EncuestaRoutesPersonalized(Resource):
    def __init__(self):
        super().__init__()
        self.schemaOne = EncuestaSchema()
        self.reglasSchemaMany = ReglasCalculoSchema(many=True)
        self.preguntasSchemaMany = PreguntaSchema(many=True)
        self.opcionesSchemaMany = OpcionSchema(many=True)
        self.estiloSchema = EstiloSchema(many=True)

    @token_required
    def get(current_user,self, enc_id):
        try:
            encuesta = Encuesta.get_by_id(enc_id)
            if not encuesta:
                return Response.error(
                    mensaje="No data",
                    error="No existe una encuesta con ese id",
                    status=404,
                )
            # Obtener estilos de aprendizaje asociados
            estilos = Estilo.query.filter_by(enc_id=enc_id).all()
            estilos_data = self.estiloSchema.dump(estilos)
            # Obtener reglas de cálculo asociadas
            reglas = ReglasCalculo.query.filter_by(enc_id=enc_id).all()
            reglas_data = self.reglasSchemaMany.dump(reglas)

            # Obtener preguntas asociadas
            preguntas = (
                encuesta.preguntas
            )  # Asumiendo que hay una relación backref 'preguntas' en Encuesta
            preguntas_data = self.preguntasSchemaMany.dump(preguntas)

            # Obtener opciones de cada pregunta
            for pregunta in preguntas_data:
                opciones = Opcion.query.filter_by(pre_id=pregunta["pre_id"]).all()
                pregunta["opciones"] = self.opcionesSchemaMany.dump(opciones)

            # Preparar la respuesta final
            encuesta_data = self.schemaOne.dump(encuesta)
            encuesta_data["reglas"] = reglas_data
            encuesta_data["preguntas"] = preguntas_data
            encuesta_data["estilos"] = estilos_data

            return Response.ok(data=encuesta_data)
        except Exception as e:
            return Response.error(error=str(e))

class EncuestToDeleteAllEncuestaRelationed(Resource):
    def __init__(self):
        super().__init__()
        self.reglasSchemaMany = ReglasCalculoSchema(many=True)
        self.preguntasSchemaMany = PreguntaSchema(many=True)
        self.opcionesSchemaMany = OpcionSchema(many=True)
        self.estiloSchema = EstiloSchema(many=True)
        self.schemaOne = EncuestaSchema()    

    @token_required
    def delete(current_user, self, enc_id):
        try:
            asignacion = Asignacion.query.filter_by(enc_id=enc_id).all()            
            if asignacion:
                return Response.error(
                    mensaje="No data",
                    error="No se puede eliminar porque ya ha sido asignado",
                    status=400,
                )
             # Eliminar los registros relacionados en la tabla Estilo
            estilos = Estilo.query.filter_by(enc_id=enc_id).all()            
            if estilos:
                for estilo in estilos:
                    estilo.delete()
                                
            # Eliminar los registros relacionados en la tabla Pregunta
            preguntas = Pregunta.query.filter_by(enc_id=enc_id).all()
            
            if preguntas:
                for pregunta in preguntas:
                    # Eliminar las opciones relacionadas con cada pregunta                    
                    opciones = Opcion.query.filter_by(pre_id=pregunta.pre_id).all()                
                    if opciones:
                        for opcion in opciones:
                            opcion.delete()
                    pregunta.delete()
                        
            encuesta = Encuesta.get_by_id(enc_id)
            if not encuesta:
                return Response.ok(status=204)
            encuesta.delete()        
            return Response.ok(status=204)
        except Exception as e:
            return Response.error(error=str(e))    
    



class EncuestaWithIdController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaOne = EncuestaSchema()

    @token_required
    def get(current_user, self, enc_id):
        try:
            consulta = Encuesta.get_by_id(enc_id)
            data = self.schemaOne.dump(consulta)
            if not data:
                return Response.error(
                    mensaje="No data",
                    error="No existe una encuesta con ese id",
                    status=404,
                )
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))

    @token_required
    def delete(current_user, self, enc_id):
        try:
            data = Encuesta.get_by_id(enc_id)
            if not data:
                return Response.error(
                    mensaje="No data",
                    error="No existe una encuesta con ese id",
                    status=404,
                )
            data.delete()
            return Response.ok(status=204)
        except Exception as e:
            return Response.error(error=str(e))

    @token_required
    def put(current_user, self, enc_id):
        try:
            encuesta = Encuesta.get_by_id(enc_id)
            if not encuesta:
                return Response.error(
                    mensaje="No data",
                    error="No existe una encuesta con ese id",
                    status=404,
                )
            encuesta.enc_autor = request.json["enc_autor"]
            encuesta.enc_cuantitativa = request.json["enc_cuantitativa"]
            encuesta.enc_descripcion = request.json["enc_descripcion"]
            encuesta.enc_fecha_creacion = request.json["enc_fecha_creacion"]
            encuesta.enc_titulo = request.json["enc_titulo"]
            encuesta.save()
            return Response.ok(
                mensaje="Actualizado", data=self.schemaOne.dump(encuesta)
            )
        except KeyError as e:
            return Response.error(
                mensaje="Faltan campos obligatorios",
                error=f"Falta el campo obligatorio '{e.args[0]}'.",
                status=400,
            )
        except ValidationError as e:
            return Response.error(
                mensaje="Error de validación, campo incorrecto",
                error=e.messages,
                status=400,
            )
        except Exception as e:
            return Response.error(error=str(e))
