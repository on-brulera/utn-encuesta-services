from flask_restful import Resource
from application.estilos.modelos.parcialModel import ParcialSchema, Parcial
from flask import request
from application.utils.response import Response
from marshmallow import ValidationError
from application.estilos.auth.authMiddleware import token_required


class   ParcialController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaMany = ParcialSchema(many=True)
        self.schemaOne = ParcialSchema()

    @token_required
    def get(current_user, self):
        try:
            consulta = Parcial.get_all()  # Método para obtener todos los registros de Parcial
            data = self.schemaMany.dump(consulta)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(
                mensaje="Error al obtener los parciales", error=str(e), status=500
            )

    @token_required
    def post(current_user, self):
        try:
            parcialJson = request.get_json()
            parcialData = self.schemaOne.load(parcialJson)
            parcial = Parcial(
                par_descripcion=parcialData["par_descripcion"]
            )
            parcial.save()  # Guardar en la base de datos
            data = self.schemaOne.dump(parcial)
            return Response.ok(data=data, mensaje="Parcial creado", status=201)
        except KeyError as e:
            return Response.error(
                mensaje="Faltan campos obligatorios",
                error=f"Falta el campo obligatorio '{e.args[0]}'.",
                status=400,
            )
        except ValidationError as e:
            return Response.error(
                mensaje="Error de validación en los datos del parcial",
                error=e.messages,
                status=400,
            )
        except Exception as e:
            return Response.error(error=str(e))


class ParcialWithIdController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaOne = ParcialSchema()

    @token_required
    def get(current_user, self, par_id):
        try:
            parcial = Parcial.get_by_id(par_id)  # Método para obtener un Parcial por ID
            if not parcial:
                return Response.error(
                    mensaje="No data",
                    error="No existe un parcial con ese ID",
                    status=404,
                )
            data = self.schemaOne.dump(parcial)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))

    @token_required
    def delete(current_user, self, par_id):
        try:
            parcial = Parcial.get_by_id(par_id)
            if not parcial:
                return Response.error(
                    mensaje="No data",
                    error="No existe un parcial con ese ID",
                    status=404,
                )
            parcial.delete()  # Método para eliminar un Parcial
            return Response.ok(mensaje="Parcial eliminado", status=204)
        except Exception as e:
            return Response.error(error=str(e))

    @token_required
    def put(current_user, self, par_id):
        try:
            parcial = Parcial.get_by_id(par_id)
            if not parcial:
                return Response.error(
                    mensaje="No data",
                    error="No existe un parcial con ese ID",
                    status=404,
                )
            # Actualizar el parcial con los nuevos datos
            parcial.par_descripcion = request.json["par_descripcion"]
            parcial.save()
            return Response.ok(
                mensaje="Parcial actualizado", data=self.schemaOne.dump(parcial)
            )
        except KeyError as e:
            return Response.error(
                mensaje="Faltan campos obligatorios",
                error=f"Falta el campo obligatorio '{e.args[0]}'.",
                status=400,
            )
        except ValidationError as e:
            return Response.error(
                mensaje="Error de validación en los datos del parcial",
                error=e.messages,
                status=400,
            )
        except Exception as e:
            return Response.error(error=str(e))
