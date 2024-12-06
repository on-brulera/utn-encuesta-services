from flask_restful import Resource
from flask import request
from application.estilos.modelos.notaModel import NotaSchema, Nota
from application.utils.response import Response
from marshmallow import ValidationError
from application.estilos.auth.authMiddleware import token_required


class NotaController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaMany = NotaSchema(many=True)
        self.schemaOne = NotaSchema()

    @token_required
    def get(current_user, self):
        try:
            consulta = Nota.query.all()
            data = self.schemaMany.dump(consulta)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(
                mensaje="Error al obtener datos de la base de datos",
                error=str(e),
                status=500,
            )

    @token_required
    def post(current_user, self):
        try:
            notaJson = request.get_json()
            notaSchema = self.schemaOne.load(notaJson)

            nota_existente = Nota.query.filter_by(
                usu_id=notaSchema["usu_id"],
                cur_id=notaSchema["cur_id"],
                mat_id=notaSchema["mat_id"],
                par_id=notaSchema["par_id"],
            ).first()
            # print(nota_existente)
            if nota_existente:
                nota_existente.not_nota = notaSchema["not_nota"]
                nota_existente.save()
                data = self.schemaOne.dump(nota_existente)
                return Response.ok(data=data, mensaje="Nota actualizada", status=200)
            else:
                nueva_nota = Nota(
                    usu_id=notaSchema["usu_id"],
                    cur_id=notaSchema["cur_id"],
                    mat_id=notaSchema["mat_id"],
                    par_id=notaSchema["par_id"],
                    not_nota=notaSchema["not_nota"],
                )
                nueva_nota.save()
                data = self.schemaOne.dump(nueva_nota)
                return Response.ok(data=data, mensaje="Nota creada", status=201)

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


class NotaWithIdController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaOne = NotaSchema()

    @token_required
    def get(current_user, self, not_id):
        try:
            consulta = Nota.query.get(not_id)
            if not consulta:
                return Response.error(
                    mensaje="No data",
                    error="No existe una nota con ese id",
                    status=404,
                )
            data = self.schemaOne.dump(consulta)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))

    @token_required
    def delete(current_user, self, not_id):
        try:
            nota = Nota.query.get(not_id)
            if not nota:
                return Response.error(
                    mensaje="No data",
                    error="No existe una nota con ese id",
                    status=404,
                )
            nota.delete()
            return Response.ok(status=204)
        except Exception as e:
            return Response.error(error=str(e))

    @token_required
    def put(current_user, self, not_id):
        try:
            nota = Nota.query.get(not_id)
            if not nota:
                return Response.error(
                    mensaje="No data",
                    error="No existe una nota con ese id",
                    status=404,
                )
            nota.usu_id = request.json["usu_id"]
            nota.cur_id = request.json["cur_id"]
            nota.mat_id = request.json["mat_id"]
            nota.par_id = request.json["par_id"]
            nota.not_nota = request.json["not_nota"]
            nota.save()
            return Response.ok(mensaje="Actualizado", data=self.schemaOne.dump(nota))
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
