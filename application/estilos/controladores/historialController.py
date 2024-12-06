from flask_restful import Resource
from application.estilos.modelos.historialModel import Historial, HistorialSchema
from flask import request
from application.utils.response import Response
from marshmallow import ValidationError
from application.estilos.auth.authMiddleware import token_required
from application.estilos.modelos.asignacionModel import Asignacion
from application.estilos.modelos.usuarioModel import Usuario
from application.estilos.modelos.notaModel import Nota


class HistorialController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaMany = HistorialSchema(many=True)
        self.schemaOne = HistorialSchema()

    @token_required
    def get(current_user, self):
        try:
            consulta = Historial.get_all()
            data = self.schemaMany.dump(consulta)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(
                mensaje="Error Obtener datos DB", error=str(e), status=500
            )

    @token_required
    def post(current_user, self):
        try:
            historialJson = request.get_json()
            historialSchema = self.schemaOne.load(historialJson)
            historial = Historial(
                asi_id=historialSchema["asi_id"],
                cur_id=historialSchema["cur_id"],
                est_cedula=historialSchema["est_cedula"],
                his_fecha_encuesta=historialSchema["his_fecha_encuesta"],
                his_nota_estudiante=historialSchema["his_nota_estudiante"],
                his_resultado_encuesta=historialSchema["his_resultado_encuesta"],
            )
            historial.save()
            data = self.schemaOne.dump(historial)
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


class HistorialWithIdAsignacion(Resource):
    def __init__(self):
        super().__init__()
        self.schemaMany = HistorialSchema(many=True)
        self.schemaOne = HistorialSchema()

    @token_required
    def post(current_user, self):
        try:
            ids_asignacion = request.get_json().get("ids_asignacion", [])

            if not isinstance(ids_asignacion, list):
                return Response.error(
                    mensaje="El campo ids_asignacion debe ser una lista.", status=400
                )

            consulta = Historial.query.filter(
                Historial.asi_id.in_(ids_asignacion)
            ).all()

            data = self.schemaMany.dump(consulta)

            return Response.ok(data=data)
        except Exception as e:
            return Response.error(
                mensaje="Error al obtener datos", error=str(e), status=500
            )


class HistorialWithIdController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaOne = HistorialSchema()

    @token_required
    def get(current_user, self, his_id):
        try:
            consulta = Historial.get_by_id(his_id)
            data = self.schemaOne.dump(consulta)
            if not data:
                return Response.error(
                    mensaje="No data",
                    error="No existe una historial con ese id",
                    status=404,
                )
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))

    @token_required
    def delete(current_user, self, his_id):
        try:
            data = Historial.get_by_id(his_id)
            if not data:
                return Response.error(
                    mensaje="No data",
                    error="No existe una historial con ese id",
                    status=404,
                )
            data.delete()
            return Response.ok(status=204)
        except Exception as e:
            return Response.error(error=str(e))

    @token_required
    def put(current_user, self, his_id):
        try:
            historial = Historial.get_by_id(his_id)
            if not historial:
                return Response.error(
                    mensaje="No data",
                    error="No existe una historial con ese id",
                    status=404,
                )
            historial.cur_id = request.json["cur_id"]
            historial.asi_id = request.json["asi_id"]
            historial.est_cedula = request.json["est_cedula"]
            historial.his_resultado_encuesta = request.json["his_resultado_encuesta"]
            historial.his_nota_estudiante = request.json["his_nota_estudiante"]
            historial.his_fecha_encuesta = request.json["his_fecha_encuesta"]
            historial.save()
            return Response.ok(
                mensaje="Actualizado", data=self.schemaOne.dump(historial)
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


class HistorialByCursoMateriaController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaMany = HistorialSchema(many=True)

    # @token_required
    # def post(current_user, self):
    #     try:
    #         # Recibir `cur_id` y `mat_id` desde el cuerpo de la solicitud
    #         data = request.get_json()
    #         cur_id = data.get("cur_id")
    #         mat_id = data.get("mat_id")

    #         if not cur_id or not mat_id:
    #             return Response.error(
    #                 mensaje="Faltan los parámetros 'cur_id' o 'mat_id'", status=400
    #             )

    #         # Consultar asignaciones que coincidan con el curso y la materia
    #         asignaciones = Asignacion.query.filter_by(
    #             cur_id=cur_id, mat_id=mat_id
    #         ).all()

    #         if not asignaciones:
    #             return Response.error(
    #                 mensaje="No se encontraron asignaciones para los parámetros proporcionados",
    #                 status=404,
    #             )

    #         # Extraer los asi_id de las asignaciones
    #         asi_ids = [asignacion.asi_id for asignacion in asignaciones]

    #         # Consultar el historial basado en los asi_id obtenidos
    #         historial = Historial.query.filter(Historial.asi_id.in_(asi_ids)).all()

    #         if not historial:
    #             return Response.error(
    #                 mensaje="No se encontraron resultados en el historial", status=404
    #             )

    #         # Serializar los datos
    #         data = self.schemaMany.dump(historial)

    #         return Response.ok(data=data)
    #     except Exception as e:
    #         return Response.error(
    #             mensaje="Error al procesar la solicitud", error=str(e), status=500
    #         )

    # @token_required
    # def post(current_user, self):
    #     try:
    #         data = request.get_json()
    #         cur_id = data.get("cur_id")
    #         mat_id = data.get("mat_id")

    #         if not cur_id or not mat_id:
    #             return Response.error(
    #                 mensaje="Faltan los parámetros 'cur_id' o 'mat_id'", status=400
    #             )

    #         asignaciones = Asignacion.query.filter_by(
    #             cur_id=cur_id, mat_id=mat_id
    #         ).all()

    #         if not asignaciones:
    #             return Response.error(
    #                 mensaje="No se encontraron asignaciones para los parámetros proporcionados",
    #                 status=404,
    #             )

    #         asi_ids = [asignacion.asi_id for asignacion in asignaciones]

    #         historial = Historial.query.filter(Historial.asi_id.in_(asi_ids)).all()

    #         if not historial:
    #             return Response.error(
    #                 mensaje="No se encontraron resultados en el historial", status=404
    #             )

    #         historial_data = []

    #         for entry in historial:
    #             usuario = Usuario.query.filter_by(per_cedula=entry.est_cedula).first()

    #             if not usuario:
    #                 return Response.error(
    #                     mensaje=f"No se encontró el usuario con la cédula {entry.est_cedula}",
    #                     status=404,
    #                 )

    #             historial_data.append(
    #                 {
    #                     "his_id": entry.his_id,
    #                     "cur_id": entry.cur_id,
    #                     "asi_id": entry.asi_id,
    #                     "usu_id": usuario.usu_id,
    #                     "his_resultado_encuesta": entry.his_resultado_encuesta,
    #                     "his_nota_estudiante": entry.his_nota_estudiante,
    #                     # "his_fecha_encuesta": entry.his_fecha_encuesta,
    #                 }
    #             )

    #         return Response.ok(data=historial_data)
    #     except Exception as e:
    #         return Response.error(
    #             mensaje="Error al procesar la solicitud", error=str(e), status=500
    #         )

    @token_required
    def post(current_user, self):
        # print('PROBANDOOO 11')
        # try:
        #     data = request.get_json()
        #     cur_id = data.get("cur_id")
        #     mat_id = data.get("mat_id")
        #     par_id = data.get("par_id")
        #     print('PROBANDOO')
        #     # Verificación de los parámetros requeridos
        #     if not cur_id or not mat_id or not par_id:
        #         return Response.error(
        #             mensaje="Faltan los parámetros 'cur_id', 'mat_id' o 'par_id'",
        #             status=400,
        #         )

        #     # Consulta de asignaciones que coincidan con cur_id, mat_id y par_id
        #     asignaciones = Asignacion.query.filter_by(
        #         cur_id=cur_id, mat_id=mat_id, par_id=par_id
        #     ).all()

        #     if not asignaciones:
        #         return Response.error(
        #             mensaje="No se encontraron asignaciones para los parámetros proporcionados",
        #             status=404,
        #         )

        #     asi_ids = [asignacion.asi_id for asignacion in asignaciones]

        #     # Consulta del historial según las asignaciones encontradas
        #     historial = Historial.query.filter(Historial.asi_id.in_(asi_ids)).all()

        #     if not historial:
        #         return Response.error(
        #             mensaje="No se encontraron resultados en el historial", status=404
        #         )

        #     historial_data = []

        #     # Recorre los resultados del historial
        #     for entry in historial:
        #         # Consulta del usuario según la cédula almacenada en el historial
        #         usuario = Usuario.query.filter_by(per_cedula=entry.est_cedula).first()

        #         if not usuario:
        #             return Response.error(
        #                 mensaje=f"No se encontró el usuario con la cédula {entry.est_cedula}",
        #                 status=404,
        #             )

        #         # Construcción de la respuesta con los datos del historial
        #         historial_data.append(
        #             {
        #                 "his_id": entry.his_id,
        #                 "cur_id": entry.cur_id,
        #                 "asi_id": entry.asi_id,
        #                 "usu_id": usuario.usu_id,
        #                 "his_resultado_encuesta": entry.his_resultado_encuesta,
        #                 "his_nota_estudiante": entry.his_nota_estudiante,
        #                 # "his_fecha_encuesta": entry.his_fecha_encuesta,  # Si es necesario, se puede incluir
        #             }
        #         )

        #     # Retorno de la respuesta con los datos obtenidos
        #     return Response.ok(data=historial_data)

        # except Exception as e:
        #     return Response.error(
        #         mensaje="Error al procesar la solicitud", error=str(e), status=500
        #     )

        try:
            data = request.get_json()
            cur_id = data.get("cur_id")
            mat_id = data.get("mat_id")
            par_id = data.get("par_id")

            # Verificamos que los parámetros 'cur_id', 'mat_id' y 'par_id' estén presentes
            if not cur_id or not mat_id or not par_id:
                return Response.error(
                    mensaje="Faltan los parámetros 'cur_id', 'mat_id' o 'par_id'",
                    status=400,
                )

            # Consultar todas las asignaciones que coinciden con 'cur_id' y 'mat_id'
            asignaciones = Asignacion.query.filter_by(
                cur_id=cur_id, mat_id=mat_id
            ).all()

            if not asignaciones:
                return Response.error(
                    mensaje="No se encontraron asignaciones para los parámetros proporcionados",
                    status=404,
                )

            # Obtener los 'asi_id' de las asignaciones
            asi_ids = [asignacion.asi_id for asignacion in asignaciones]

            # Consultar los registros en la tabla 'historial' para esos 'asi_id' y el 'cur_id'
            historial = Historial.query.filter(
                Historial.asi_id.in_(asi_ids), Historial.cur_id == cur_id
            ).all()

            if not historial:
                return Response.error(
                    mensaje="No se encontraron resultados de encuestas en el historial",
                    status=404,
                )

            # Consultamos todas las notas de los estudiantes en la tabla 'nota'
            notas = Nota.query.filter_by(
                cur_id=cur_id, mat_id=mat_id, par_id=par_id
            ).all()
           

            if not notas:
                return Response.error(
                    mensaje="No se encontraron notas para los parámetros proporcionados",
                    status=404,
                )

            # Estructurar los datos combinados de notas y resultados de encuestas
            resultados_data = []
            for nota in notas:
                usuario = Usuario.query.filter_by(usu_id=nota.usu_id).first()

                if not usuario:
                    return Response.error(
                        mensaje=f"No se encontró el usuario con el ID {nota.usu_id}",
                        status=404,
                    )

               # Obtener el historial del estudiante basado en 'asi_id'
                historial_estudiante = next(
                    (h for h in historial if h.est_cedula == usuario.per_cedula), None
                )

                if not historial_estudiante:
                    # return Response.error(
                    #     mensaje=f"No se encontró historial para el usuario con la cédula {usuario.per_cedula}",
                    #     status=404,
                    # )
                    print('')
                else:
                    resultados_data.append(
                    # Agregar la información a la lista
                    {
                        "usu_id": usuario.usu_id,
                        "nombre": f"{usuario.per_cedula}",  # Nombre del estudiante
                        "cur_id": nota.cur_id,
                        "mat_id": nota.mat_id,
                        "par_id": nota.par_id,
                        "not_nota": nota.not_nota,  # Nota del estudiante
                        "his_resultado_encuesta": historial_estudiante.his_resultado_encuesta,
                        # "his_nota_estudiante": historial_estudiante.his_nota_estudiante,
                    }
                )

            # Retornar los resultados encontrados
            return Response.ok(data=resultados_data)


        except Exception as e:
            return Response.error(
                mensaje="Error al procesar la solicitud", error=str(e), status=500
            )




class HistorialByCursoMateriaEncuestaController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaMany = HistorialSchema(many=True)
    
    @token_required
    def post(current_user, self):        

        try:
            data = request.get_json()
            cur_id = data.get("cur_id")
            mat_id = data.get("mat_id")
            par_id = data.get("par_id")
            enc_id = data.get("enc_id")

            # Verificamos que los parámetros 'cur_id', 'mat_id' y 'par_id' estén presentes
            if not cur_id or not mat_id or not par_id:
                return Response.error(
                    mensaje="Faltan los parámetros 'cur_id', 'mat_id' o 'par_id'",
                    status=400,
                )

            # Consultar todas las asignaciones que coinciden con 'cur_id' y 'mat_id'
            asignaciones = Asignacion.query.filter_by(
                cur_id=cur_id, mat_id=mat_id, enc_id=enc_id                
            ).all()

            if not asignaciones:
                return Response.error(
                    mensaje="No se encontraron asignaciones para los parámetros proporcionados",
                    status=404,
                )

            # Obtener los 'asi_id' de las asignaciones
            asi_ids = [asignacion.asi_id for asignacion in asignaciones]

            # Consultar los registros en la tabla 'historial' para esos 'asi_id' y el 'cur_id'
            historial = Historial.query.filter(
                Historial.asi_id.in_(asi_ids), Historial.cur_id == cur_id
            ).all()

            if not historial:
                return Response.error(
                    mensaje="No se encontraron resultados de encuestas en el historial",
                    status=404,
                )

            # Consultamos todas las notas de los estudiantes en la tabla 'nota'
            notas = Nota.query.filter_by(
                cur_id=cur_id, mat_id=mat_id, par_id=par_id, 
            ).all()
           

            if not notas:
                return Response.error(
                    mensaje="No se encontraron notas para los parámetros proporcionados",
                    status=404,
                )

            # Estructurar los datos combinados de notas y resultados de encuestas
            resultados_data = []
            for nota in notas:
                usuario = Usuario.query.filter_by(usu_id=nota.usu_id).first()

                if not usuario:
                    return Response.error(
                        mensaje=f"No se encontró el usuario con el ID {nota.usu_id}",
                        status=404,
                    )

               # Obtener el historial del estudiante basado en 'asi_id'
                historial_estudiante = next(
                    (h for h in historial if h.est_cedula == usuario.per_cedula), None
                )

                if historial_estudiante:
                    # return Response.error(
                    #     mensaje=f"No se encontró historial para el usuario con la cédula {usuario.per_cedula}",
                    #     status=404,
                    # )
                    
                
                    resultados_data.append(
                    # Agregar la información a la lista
                    {
                        "usu_id": usuario.usu_id,
                        "nombre": f"{usuario.per_cedula}",  # Nombre del estudiante
                        "cur_id": nota.cur_id,
                        "mat_id": nota.mat_id,
                        "par_id": nota.par_id,
                        "not_nota": nota.not_nota,  # Nota del estudiante
                        "his_resultado_encuesta": historial_estudiante.his_resultado_encuesta,
                        # "his_nota_estudiante": historial_estudiante.his_nota_estudiante,
                    })
                

            # Retornar los resultados encontrados
            return Response.ok(data=resultados_data)


        except Exception as e:
            return Response.error(
                mensaje="Error al procesar la solicitud", error=str(e), status=500
            )
