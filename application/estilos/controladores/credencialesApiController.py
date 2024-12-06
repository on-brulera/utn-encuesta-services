from flask_restful import Resource
from flask import request
from application.utils.response import Response
from application.estilos.auth.authMiddleware import token_required
from application.estilos.modelos.credencialesApiModel import CredencialesAPI, CredencialesAPISchema
from marshmallow import ValidationError

class CredencialesAPIController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaMany = CredencialesAPISchema(many=True)
        self.schemaOne = CredencialesAPISchema()

    @token_required
    def get(current_user, self):
        try:
            consulta = CredencialesAPI.query.all()
            data = self.schemaMany.dump(consulta)
            if not data:
                return Response.error(
                mensaje="No existen credenciales registradas",error='No hay datos', status=404
            )
            else:
                return Response.ok(data=data)
        except Exception as e:
            return Response.error(
                mensaje="Error al obtener las credenciales", error=str(e), status=500
            )

    @token_required
    def post(current_user, self):
        try:
            credencialesJson = request.get_json()
            credenciales = self.schemaOne.load(credencialesJson)
            nueva_credencial = CredencialesAPI(
                nombre_servicio=credenciales["nombre_servicio"],
                api_key=credenciales["api_key"]
            )
            nueva_credencial.save()
            data = self.schemaOne.dump(nueva_credencial)
            return Response.ok(data=data, mensaje="Credencial creada con éxito", status=201)
        except ValidationError as e:
            return Response.error(
                mensaje="Error de validación, campo incorrecto",
                error=e.messages,
                status=400,
            )
        except Exception as e:
            return Response.error(error=str(e))

    
class CredencialesWithcredIdController(Resource):
    def __init__(self):
        super().__init__()
        self.schemaOne = CredencialesAPISchema()
        
    @token_required
    def put(current_user, self, cred_id):
        try:
            credencial = CredencialesAPI.query.get(cred_id)
            if not credencial:
                return Response.error(
                    mensaje="No se encontró la credencial",
                    error=f"No existe una credencial con el id {cred_id}",
                    status=404,
                )
            credencialesJson = request.get_json()
            credencialesActualizadas = self.schemaOne.load(credencialesJson, partial=True)

            credencial.nombre_servicio = credencialesActualizadas.get("nombre_servicio", credencial.nombre_servicio)
            credencial.api_key = credencialesActualizadas.get("api_key", credencial.api_key)
            credencial.save()

            data = self.schemaOne.dump(credencial)
            return Response.ok(data=data, mensaje="Credencial actualizada con éxito")
        except ValidationError as e:
            return Response.error(
                mensaje="Error de validación, campo incorrecto",
                error=e.messages,
                status=400,
            )
        except Exception as e:
            return Response.error(error=str(e))
    
    @token_required
    def get(current_user, self, cred_id):
        try:
            if cred_id:
                credencial = CredencialesAPI.get_by_id(cred_id)
                if not credencial:
                    return Response.error(
                        mensaje="No se encontró la credencial",
                        error=f"No existe una credencial con id {cred_id}",
                        status=404,
                    )
                data = self.schemaOne.dump(credencial)
                return Response.ok(data=data)
            else:
                return Response.error(
                    mensaje="ID no proporcionado",
                    error="Se requiere un cred_id para esta solicitud.",
                    status=400,
                )
        except Exception as e:
            return Response.error(
                mensaje="Error al obtener la credencial",
                error=str(e),
                status=500,
            )