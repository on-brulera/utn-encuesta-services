import select
from flask_restful import Resource
from flask import request, jsonify
from marshmallow import ValidationError
from application.estilos.modelos.asignacionModel import Asignacion
from application.estilos.modelos.materiaModel import Materia, MateriaSchema
from application.utils.response import Response
from application.estilos.auth.authMiddleware import token_required

class MateriaController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaMany = MateriaSchema(many=True)
        self.schemaOne = MateriaSchema()

    @token_required
    def get(current_user, self):
        try:
            consulta = Materia.query.all()
            data = self.schemaMany.dump(consulta)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(
                mensaje="Error al obtener datos de la base de datos",
                error=str(e),
                status=500
            )

    @token_required
    def post(current_user, self):
        try:
            materia_json = request.get_json()
            materia_data = self.schemaOne.load(materia_json)
            materia = Materia(
                mat_nombre=materia_data["mat_nombre"],
                mat_descripcion=materia_data.get("mat_descripcion")
            )
            materia.save()
            data = self.schemaOne.dump(materia)
            return Response.ok(data=data, mensaje="Materia creada", status=201)
        except KeyError as e:
            return Response.error(
                mensaje="Faltan campos obligatorios",
                error=f"Falta el campo obligatorio '{e.args[0]}'.",
                status=400
            )
        except ValidationError as e:
            return Response.error(
                mensaje="Error de validación, campo incorrecto",
                error=e.messages,
                status=400
            )
        except Exception as e:
            return Response.error(error=str(e))

class MateriaWithIdController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaOne = MateriaSchema()

    @token_required
    def get(current_user, self, mat_id):
        try:
            materia = Materia.query.get(mat_id)
            if not materia:
                return Response.error(
                    mensaje="Materia no encontrada",
                    error="No existe una materia con ese ID",
                    status=404
                )
            data = self.schemaOne.dump(materia)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))

    @token_required
    def put(current_user, self, mat_id):
        try:
            materia = Materia.query.get(mat_id)
            if not materia:
                return Response.error(
                    mensaje="Materia no encontrada",
                    error="No existe una materia con ese ID",
                    status=404
                )
            materia_data = request.get_json()
            materia = self.schemaOne.load(materia_data, instance=materia) 
            materia.save()  
            data = self.schemaOne.dump(materia)
            return Response.ok(data=data, mensaje="Materia actualizada")
        except KeyError as e:
            return Response.error(
                mensaje="Faltan campos obligatorios",
                error=f"Falta el campo obligatorio '{e.args[0]}'.",
                status=400
            )
        except ValidationError as e:
            return Response.error(
                mensaje="Error de validación, campo incorrecto",
                error=e.messages,
                status=400
            )
        except Exception as e:
            return Response.error(error=str(e))

    @token_required
    def delete(current_user, self, mat_id):
        try:
            materia = Materia.query.get(mat_id)
            if not materia:
                return Response.error(
                    mensaje="Materia no encontrada",
                    error="No existe una materia con ese ID",
                    status=404
                )
            materia.delete()
            return Response.ok(status=204, mensaje="Materia eliminada")
        except Exception as e:
            return Response.error(error=str(e))


    


class MateriaEstudianteController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaMany = MateriaSchema(many=True)
        self.schemaOne = MateriaSchema()

    @token_required
    def post(current_user, self):
        try:
            # Obtener `cur_id` del cuerpo de la solicitud
            datos = request.get_json()
            cur_id = datos.get("cur_id")

            if cur_id is None:
                return Response.error(
                    mensaje="El parámetro 'cur_id' es obligatorio.",
                    status=400
                )

            # Consulta utilizando SQLAlchemy con `with_entities`
            consulta = (
                Materia.query
                .with_entities(
                    Materia.mat_id,
                    Materia.mat_nombre,
                    Materia.mat_descripcion
                )
                .join(Asignacion, Materia.mat_id == Asignacion.mat_id)
                .filter(Asignacion.cur_id == cur_id)
                .group_by(
                    Materia.mat_id,
                    Materia.mat_nombre,
                    Materia.mat_descripcion
                )
                .all()
            )

            # Convertir los resultados en una lista de diccionarios
            materias = [
                {
                    "mat_id": row.mat_id,
                    "mat_nombre": row.mat_nombre,
                    "mat_descripcion": row.mat_descripcion
                }
                for row in consulta
            ]

            return Response.ok(data=materias, mensaje="Materias encontradas")

        except Exception as e:
            return Response.error(
                mensaje="Error al obtener materias",
                error=str(e),
                status=500
            )
