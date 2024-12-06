from flask_restful import Resource
from application.estilos.modelos.asignacionModel import Asignacion, AsignacionSchema
from application.estilos.modelos.cursoModel import Curso
from application.estilos.modelos.materiaModel import Materia
from application.estilos.modelos.notaModel import Nota
from application.estilos.modelos.parcialModel import Parcial
from application.estilos.modelos.preguntaModel import Pregunta
from application.estilos.modelos.respuestaModel import Respuesta
from application.estilos.modelos.historialModel import Historial
from application.estilos.modelos.opcionModel import Opcion
from application.estilos.modelos.encuestaModel import Encuesta
from application.estilos.modelos.estilosModel import Estilo
from application.estilos.modelos.reglasCalculoModel import ReglasCalculo
from flask import jsonify, request
from application.utils.response import Response
from marshmallow import ValidationError
from application.estilos.auth.authMiddleware import token_required


class AsignacionController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaMany = AsignacionSchema(many=True)
        self.schemaOne = AsignacionSchema()

    @token_required
    def get(current_user, self):
        try:
            consulta = Asignacion.get_all()
            data = self.schemaMany.dump(consulta)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(
                mensaje="Error Obtener datos DB", error=str(e), status=500
            )

    @token_required
    def post(current_user, self):
        try:
            asignacionJson = request.get_json() 
            asignacionSchema = self.schemaOne.load(asignacionJson)
            asignacion = Asignacion(
                asi_descripcion=asignacionSchema["asi_descripcion"],
                asi_fecha_completado=asignacionSchema["asi_fecha_completado"],
                cur_id=asignacionSchema["cur_id"],
                enc_id=asignacionSchema["enc_id"],
                usu_id=asignacionSchema["usu_id"],
                mat_id=asignacionSchema["mat_id"], 
                usu_id_asignador=asignacionSchema.get("usu_id_asignador", None),
                par_parcial_seleccionado=asignacionSchema.get("par_parcial_seleccionado", None),
            )
            asignacion.save()
            data = self.schemaOne.dump(asignacion)
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


class AsignacionWithIdController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaOne = AsignacionSchema()

    @token_required
    def get(current_user, self, asi_id):
        try:
            consulta = Asignacion.get_by_id(asi_id)
            data = self.schemaOne.dump(consulta)
            if not data:
                return Response.error(
                    mensaje="No data",
                    error="No existe una asignacion con ese id",
                    status=404,
                )
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))

    @token_required
    def delete(current_user, self, asi_id):
        try:
            data = Asignacion.get_by_id(asi_id)
            if not data:
                return Response.error(
                    mensaje="No data",
                    error="No existe una asignacion con ese id",
                    status=404,
                )
            data.delete()
            return Response.ok(status=204)
        except Exception as e:
            return Response.error(error=str(e))

    @token_required
    def put(current_user, self, asi_id):
        try:
            asignacion = Asignacion.get_by_id(asi_id)
            if not asignacion:
                return Response.error(
                    mensaje="No data",
                    error="No existe una asignacion con ese id",
                    status=404,
                )
            asignacion.enc_id = request.json["enc_id"]
            asignacion.usu_id = request.json["usu_id"]
            asignacion.cur_id = request.json["cur_id"]
            asignacion.mat_id = request.json["mat_id"] 
            asignacion.asi_descripcion = request.json["asi_descripcion"]
            asignacion.asi_fecha_completado = request.json["asi_fecha_completado"]
            asignacion.asi_realizado = request.json["asi_realizado"]
            asignacion.save()
            return Response.ok(
                mensaje="Actualizado", data=self.schemaOne.dump(asignacion)
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


class AsignacionWithUsuarioId(Resource):
    def __init__(self):
        super().__init__()
        self.schemaOne = AsignacionSchema()
        self.schemaMany = AsignacionSchema(many=True)

    def get(self, usu_id):
        try:
            consulta = Asignacion.get_by_usu_id(usu_id)
            data = self.schemaMany.dump(consulta)
            if not data:
                return Response.error(
                    mensaje="No data",
                    error=f"No existe una asignación con usu_id {usu_id}",
                    status=404,
                )
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(
                mensaje="Error Obtener datos DB", error=str(e), status=500
            )

class AsignacionWithUsuarioDocenteId(Resource):
    def __init__(self):
        super().__init__()
        self.schemaOne = AsignacionSchema()
        self.schemaMany = AsignacionSchema(many=True)

    def get(self, usu_id):
        try:            
                  
            consulta = (
                Asignacion.query
                .with_entities(
                    Asignacion.enc_id,
                    Encuesta.enc_titulo,                                  
                    Curso.cur_id, 
                    Curso.cur_carrera,                   
                    Curso.cur_nivel,                   
                    Curso.cur_periodo_academico,
                    Materia.mat_nombre,                   
                    Nota.mat_id,
                    Asignacion.par_parcial_seleccionado
                )                
                .join(Encuesta, Asignacion.enc_id == Encuesta.enc_id)
                .join(Curso, Asignacion.cur_id == Curso.cur_id)
                .join(Materia, Asignacion.mat_id == Materia.mat_id)
                .join(Nota, Materia.mat_id == Nota.mat_id)                
                .filter(Asignacion.usu_id_asignador == usu_id)
                .group_by(Asignacion.enc_id, 
                        Curso.cur_id, 
                        Materia.mat_id,
                        Encuesta.enc_titulo, 
                        Nota.mat_id,
                        Asignacion.par_parcial_seleccionado    
                        )
                        .all()
            )

            data = [
                {
                    "enc_id": row.enc_id,
                    "enc_titulo": row.enc_titulo,
                    "cur_id": row.cur_id,
                    "cur_carrera": row.cur_carrera,
                    "cur_nivel": row.cur_nivel,
                    "cur_periodo_academico": row.cur_periodo_academico,                    
                    "mat_nombre": row.mat_nombre,
                    "mat_id": row.mat_id,
                    "par_id": row.par_parcial_seleccionado
                }
                for row in consulta
            ]
                
            return Response.ok(data=data)                        
            
        except Exception as e:
            return Response.error(
                mensaje="Error Obtener datos DB", error=str(e), status=500
            )

from flask_restful import Resource
from flask import request
from application.utils.response import Response
from application.estilos.modelos.asignacionModel import Asignacion
from marshmallow import ValidationError

class AsignacionesDeleteController(Resource):
    def post(self):
        """
        Endpoint para eliminar asignaciones basadas en parámetros específicos.
        """
        try:
            # Obtener los parámetros del cuerpo de la solicitud
            params = request.get_json()

            enc_id = params.get("enc_id")
            cur_id = params.get("cur_id")
            mat_id = params.get("mat_id")
            par_parcial_seleccionado = params.get("par_parcial_seleccionado")
            usu_id_asignador = params.get("usu_id_asignador")

            # Validar que todos los parámetros requeridos estén presentes
            if not all([enc_id, cur_id, mat_id, par_parcial_seleccionado, usu_id_asignador]):
                return Response.error(
                    mensaje="Faltan campos obligatorios",
                    error="Se requiere enc_id, cur_id, mat_id, par_parcial_seleccionado, y usu_id_asignador.",
                    status=400
                )

            # Llamar al método del modelo para realizar la eliminación
            rows_deleted = Asignacion.delete_by_filters(
                enc_id=enc_id,
                cur_id=cur_id,
                mat_id=mat_id,
                par_parcial_seleccionado=par_parcial_seleccionado,
                usu_id_asignador=usu_id_asignador
            )

            if rows_deleted > 0:
                return Response.ok(
                    mensaje=f"{rows_deleted} asignación(es) eliminada(s).",
                    status=200
                )
            else:
                return Response.error(
                    mensaje="No se encontraron registros para eliminar.",
                    status=404
                )

        except Exception as e:
            return Response.error(
                mensaje="Error al eliminar asignaciones.",
                error=str(e),
                status=500
            )



class AsignacionTerminada(Resource):
    def __init__(self):
        super().__init__()
        self.schemaOne = AsignacionSchema()
        self.schemaMany = AsignacionSchema(many=True)

    def get(self, asi_id):
        try:
            asignacion = Asignacion.get_by_id(asi_id)
            if not asignacion:
                return Response.error(
                    mensaje="No data",
                    error="No existe una asignacion con ese id",
                    status=404,
                )            
            asignacion.asi_realizado = True
            asignacion.save()
            return Response.ok(
                mensaje="Actualizado", data=self.schemaOne.dump(asignacion)
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

class AsignacionWithCursoId(Resource):
    def __init__(self):
        super().__init__()
        self.schemaMany = AsignacionSchema(many=True)
        self.schemaOne = AsignacionSchema()

    @token_required
    def get(current_user, self, cur_id):
        try:
            consulta = Asignacion.query.filter_by(cur_id=cur_id).all()
            data = []
            for asignacion in consulta:
                asignacion_info = {
                    "asi_id": asignacion.asi_id,
                    "curso": None,
                    "mat_id":None,
                    "materia": None,
                    "usu_id": asignacion.usu_id,
                    "asi_descripcion": asignacion.asi_descripcion,
                    "asi_fecha_completado": asignacion.asi_fecha_completado,
                    "asi_realizado": asignacion.  asi_realizado,
                    "encuesta": None,
                }
                if asignacion.usuario:
                    asignacion_info["usuario"] = {
                        "usu_id": asignacion.usuario.usu_id,
                        "usu_usuario": asignacion.usuario.usu_usuario,
                    }
                if asignacion.materia:
                    asignacion_info["materia"] = asignacion.materia.mat_nombre
                    asignacion_info["mat_id"] = asignacion.materia.mat_id
                if asignacion.encuesta:
                    asignacion_info["encuesta"] = {
                        "enc_id": asignacion.encuesta.enc_id,
                        "enc_titulo": asignacion.encuesta.enc_titulo,
                        "enc_descripcion": asignacion.encuesta.enc_descripcion,
                        "enc_autor": asignacion.encuesta.enc_autor,
                        "enc_cuantitativa": asignacion.encuesta.enc_cuantitativa,
                        "enc_fecha_creacion": asignacion.encuesta.enc_fecha_creacion,
                    }
                if asignacion.curso:
                    asignacion_info["curso"] = {
                        "cur_id": asignacion.curso.cur_id,
                        "cur_carrera": asignacion.curso.cur_carrera,
                        "cur_nivel": asignacion.curso.cur_nivel,
                    }
                    data.append(asignacion_info)
            if not data:
                return Response.error(
                    mensaje="No data",
                    error=f"No existe una asignación con cur_id {cur_id}",
                    status=404,
                )
            return jsonify({"data": data, "mensaje": "Petición Exitosa"})
            # return Response.ok(data=jsonify(data))
        except Exception as e:
            return Response.error(
                mensaje="Error Obtener datos DB", error=str(e), status=500
            )

class AsignacionWithCursoIdMaterias(Resource):
    def __init__(self):
        super().__init__()
        self.schemaMany = AsignacionSchema(many=True)

    @token_required
    def get(current_user, self, cur_id):
        try:
            # Consultar asignaciones que coincidan con el cur_id
            consulta = Asignacion.query.filter_by(cur_id=cur_id).all()

            # Si no se encuentran resultados
            if not consulta:
                return Response.error(
                    mensaje=f"No existen asignaciones para el curso con cur_id {cur_id}",
                    status=404,
                )

            # Serializar los datos de las asignaciones y materias relacionadas
            data = []
            for asignacion in consulta:
                materia = asignacion.materia  # Relación con la tabla materia
                asignacion_info = {
                    "asi_id": asignacion.asi_id,
                    "cur_id": asignacion.cur_id,
                    "mat_id": asignacion.mat_id,
                    "materia": materia.mat_nombre if materia else "No asignada",
                    "asi_descripcion": asignacion.asi_descripcion,
                    "asi_fecha_completado": asignacion.asi_fecha_completado,
                    "asi_realizado": asignacion.asi_realizado,
                }
                data.append(asignacion_info)

            # Devolver los datos en la respuesta
            return Response.ok(data=data, mensaje="Consulta exitosa")
        
        except Exception as e:
            return Response.error(
                mensaje="Error al obtener datos de la base de datos", 
                error=str(e), 
                status=500
            )


class AsignacionTestWithId(Resource):
    def __init__(self):
        super().__init__()
        self.schemaOne = AsignacionSchema()
        
    @token_required
    def get(current_user, self, asi_id):
        try:
            asignacion = Asignacion.query.filter_by(asi_id=asi_id).first()
            if not asignacion:
                return Response.error(
                mensaje="No data",
                error="No existe una asignacion con ese id",
                status=404,
                )
            
            encuesta = Encuesta.query.filter_by(enc_id=asignacion.enc_id).first()
            estilos = Estilo.query.filter_by(enc_id=asignacion.enc_id).all()
            estilos_aprendizaje = [
                {
                "est_id": estilo.est_id,
                "est_nombre": estilo.est_nombre,
                "est_descripcion": estilo.est_descripcion,
                "est_parametro":estilo.est_parametro
                }
                for estilo in estilos
            ]
            
            preguntas = Pregunta.query.filter_by(enc_id=asignacion.enc_id).all()
            respuestas = Respuesta.query.filter_by(asi_id=asi_id).all()
            respuesta_historial = Historial.query.filter_by(asi_id=asi_id).all()
            asignacion_data = {
                "asi_id": asignacion.asi_id,
                "respuesta_historial":respuesta_historial[0].his_resultado_encuesta,
                "encuesta": {
                    "enc_id": encuesta.enc_id,
                    "enc_titulo": encuesta.enc_titulo,
                    "estilos_aprendizaje": estilos_aprendizaje, 
                },
                "preguntas": [],
            }

            for pregunta in preguntas:
                pregunta_data = {
                    "pre_id": pregunta.pre_id,
                    "pre_enunciado": pregunta.pre_enunciado,
                    "opciones": [],
                    "respuesta": [],
                }
                opciones = Opcion.query.filter_by(pre_id=pregunta.pre_id).all()
                
                for opcion in opciones:
                    opcion_data = {
                        "opc_id": opcion.opc_id,
                        "opc_texto": opcion.opc_texto,
                        "opc_valor_cualitativo": opcion.opc_valor_cualitativo,
                        "opc_valor_cuantitativo": float(opcion.opc_valor_cuantitativo),
                        }
                    pregunta_data["opciones"].append(opcion_data)
                     
                respuestas_pregunta = list(filter(lambda x:x.pre_id==pregunta.pre_id,respuestas))
                if respuestas_pregunta:
                    for res in respuestas_pregunta:
                        respuesta_opcion = Opcion.query.filter_by(opc_id=res.opc_id).first()
                        nueva_respuesta =  {
                        "opc_id": respuesta_opcion.opc_id,
                        "opc_texto": respuesta_opcion.opc_texto,
                        "opc_valor_cualitativo": respuesta_opcion.opc_valor_cualitativo,
                        "opc_valor_cuantitativo": float(res.res_valor_cuantitativo),}
                        pregunta_data["respuesta"].append(nueva_respuesta)
                    
                asignacion_data["preguntas"].append(pregunta_data)
            return Response.ok(data=asignacion_data)
        except Exception as e:
            return Response.error(error=str(e))


class AsignacionWithEncuestaId(Resource):
    def __init__(self):
        super().__init__()
        self.schemaOne = AsignacionSchema()
        
    @token_required
    def get(current_user, self, enc_id):
        try:
            asignacion = Asignacion.query.filter_by(enc_id=enc_id).first()     
            data = self.schemaOne.dump(asignacion)    
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))


 
