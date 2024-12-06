from flask_restful import Resource
from application.estilos.modelos.usuarioModel import Usuario, UsuarioSchema
from application.estilos.modelos.personaModel import Persona
from flask import request
from application.utils.response import Response
from marshmallow import ValidationError
import bcrypt


class UsuarioController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaMany = UsuarioSchema(many=True)
        self.schemaOne = UsuarioSchema()

    def get(self):
        try:
            consulta = Usuario.get_all()
            data = self.schemaMany.dump(consulta)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(
                mensaje="Error Obtener datos DB", error=str(e), status=500
            )

    def post(self):
        try:
            usuarioJson = request.get_json(force=True)
            usuarioSchema = self.schemaOne.load(usuarioJson)
            usuario = Usuario(
                cur_id=usuarioSchema["cur_id"],
                per_cedula=usuarioSchema["per_cedula"],
                rol_codigo=usuarioSchema["rol_codigo"],
                usu_estado=usuarioSchema["usu_estado"],
                usu_password=bcrypt.hashpw(
                    usuarioSchema["usu_password"].encode("utf-8"), bcrypt.gensalt()
                ).decode("utf-8"),
                usu_usuario=usuarioSchema["usu_usuario"],
            )
            usuario.save()
            data = self.schemaOne.dump(usuario)
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


class UsuarioWithIdController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaOne = UsuarioSchema()

    def get(self, usu_id):
        try:
            consulta = Usuario.get_by_id(usu_id)
            data = self.schemaOne.dump(consulta)
            if not data:
                return Response.error(
                    mensaje="No data",
                    error="No existe un usuario con ese id",
                    status=404,
                )
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))

    def delete(self, usu_id):
        try:
            data = Usuario.get_by_id(usu_id)
            if not data:
                return Response.error(
                    mensaje="No data",
                    error="No existe un usuario con ese id",
                    status=404,
                )
            data.delete()
            return Response.ok(status=204)
        except Exception as e:
            return Response.error(error=str(e))

    def put(self, usu_id):
        try:
            usuario = Usuario.get_by_id(usu_id)
            if not usuario:
                return Response.error(
                    mensaje="No data",
                    error="No existe un usuario con ese id",
                    status=404,
                )
            usuario.cur_id = request.json["cur_id"]
            usuario.per_cedula = request.json["per_cedula"]
            usuario.rol_codigo = request.json["rol_codigo"]
            usuario.usu_estado = request.json["usu_estado"]
            usuario.usu_password = bcrypt.hashpw(request.json["usu_password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            usuario.usu_usuario = request.json["usu_usuario"]
            usuario.save()
            return Response.ok(mensaje="Actualizado", data=self.schemaOne.dump(usuario))
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

class UsuarioWithCedula(Resource):
    def __init__(self):
        super().__init__()
        self.schemaOne = UsuarioSchema()

    def get(self, per_cedula):
        try:
            usuario = Usuario.get_by_cedula(per_cedula)
            if not usuario:
                return Response.error(
                    mensaje="No data",
                    error=f"No existe un usuario con la cédula {per_cedula}",
                    status=404,
                )
            data = self.schemaOne.dump(usuario)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))
        
class UsuarioWithRolCodigo(Resource):
    def __init__(self):
        super().__init__()
        self.schemaMany = UsuarioSchema(many=True)

    def get(self, rol_codigo):
        try:
            usuario = Usuario.get_by_rol_codigo(rol_codigo)
            if not usuario:
                return Response.error(
                    mensaje="No data",
                    error=f"No existe un usuario con la cédula {rol_codigo}",
                    status=404,
                )
            data = self.schemaMany.dump(usuario)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))

class UsuarioCedulas(Resource):
    def __init__(self):
        super().__init__()
        self.schemaMany = UsuarioSchema(many=True)
        self.schemaOne = UsuarioSchema()

    def get(self):
        try:
            cedulas = Persona.query.with_entities(Persona.per_cedula).all()
            cedula_list = [cedula.per_cedula for cedula in cedulas]
            return Response.ok(data=cedula_list)
        except Exception as e:
            return Response.error(
                mensaje="Error al obtener cédulas de las personas",
                error=str(e),
                status=500
            )
