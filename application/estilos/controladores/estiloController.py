from flask_restful import Resource
from application.estilos.modelos.estilosModel import Estilo, EstiloSchema
from flask import request
from application.utils.response import Response
from marshmallow import ValidationError
from application.estilos.auth.authMiddleware import token_required


class EstiloController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaMany = EstiloSchema(many=True)
        self.schemaOne = EstiloSchema()

    @token_required
    def get(current_user, self):
        try:
            consulta = Estilo.get_all()
            data = self.schemaMany.dump(consulta)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(
                mensaje="Error Obtener datos DB", error=str(e), status=500
            )

    @token_required
    def post(current_user, self):
        try:
            estiloJson = request.get_json()
            estiloSchema = self.schemaOne.load(estiloJson)
            estilo = Estilo(
                est_descripcion=estiloSchema["est_descripcion"],
                est_nombre=estiloSchema["est_nombre"],
                enc_id=estiloSchema["enc_id"],
                est_parametro=estiloSchema["est_parametro"],
            )
            estilo.save()
            data = self.schemaOne.dump(estilo)
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


class EstiloWithIdController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaOne = EstiloSchema()

    @token_required
    def get(current_user, self, est_id):
        try:
            consulta = Estilo.get_by_id(est_id)
            data = self.schemaOne.dump(consulta)
            if not data:
                return Response.error(
                    mensaje="No data",
                    error="No existe un estilo con ese id",
                    status=404,
                )
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))

    @token_required
    def delete(current_user, self, est_id):
        try:
            data = Estilo.get_by_id(est_id)
            if not data:
                return Response.error(
                    mensaje="No data",
                    error="No existe un estilo con ese id",
                    status=404,
                )
            data.delete()
            return Response.ok(status=204)
        except Exception as e:
            return Response.error(error=str(e))

    @token_required
    def put(current_user, self, est_id):
        try:
            estilo = Estilo.get_by_id(est_id)
            if not estilo:
                return Response.error(
                    mensaje="No data",
                    error="No existe un estilo con ese id",
                    status=404,
                )
            estilo.est_nombre = request.json["est_nombre"]
            estilo.est_descripcion = request.json["est_descripcion"]
            estilo.enc_id = request.json["enc_id"]
            estilo.est_parametro = request.json["est_parametro"]
            estilo.save()
            return Response.ok(mensaje="Actualizado", data=self.schemaOne.dump(estilo))
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


class EstiloWithIdEncuesta(Resource):
    def __init__(self):
        super().__init__()
        self.schemaOne = EstiloSchema(many=True)

    @token_required
    def get(current_user, self, enc_id):
        try:
            consulta = Estilo.get_by_enc_id(enc_id)
            data = self.schemaOne.dump(consulta)
            if not data:
                return Response.error(
                    mensaje="No data",
                    error="No existe un estilo con ese enc_id",
                    status=404,
                )
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))


class EstiloWithIdActualizarCampos(Resource):
    def __init__(self):
        super().__init__()
        self.schemaOne = EstiloSchema()  # Para un solo objeto

    @token_required
    def put(current_user,self, est_id):
        estiloJson = request.get_json()
        try:
            estilo = Estilo.get_by_est_id(est_id)

            if not estilo:
                return Response.error(
                    mensaje="No data",
                    error="No existe un estilo con ese est_id",
                    status=404,
                )

            nueva_descripcion = estiloJson.get("est_descripcion", None)

            if not nueva_descripcion:
                return Response.error(
                    mensaje="Falta la descripción",
                    error="El campo 'est_descripcion' es obligatorio",
                    status=400,
                )

            # Actualizar el campo y guardar
            estilo.est_descripcion = nueva_descripcion
            estilo.save()

            return Response.ok(
                mensaje="Descripción actualizada correctamente",
                data=self.schemaOne.dump(estilo),
            )

        except Exception as e:
            return Response.error(
                mensaje="Error al actualizar",
                error=str(e),
                status=500,
            )
