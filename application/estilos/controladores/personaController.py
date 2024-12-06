from flask_restful import Resource
from sqlalchemy import case, func
from application.estilos.modelos.notaModel import Nota
from application.estilos.modelos.personaModel import Persona, PersonaSchema
from flask import request
from application.estilos.modelos.usuarioModel import Usuario
from application.utils.response import Response
from marshmallow import ValidationError
from application.estilos.auth.authMiddleware import token_required
class PersonaController(Resource):    
    def __init__(self):
        super().__init__()
        self.schemaMany = PersonaSchema(many=True)
        self.schemaOne = PersonaSchema()
    
    @token_required
    def get(current_user, self):
        try:                        
            consulta = Persona.get_all()
            data = self.schemaMany.dump(consulta)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(mensaje='Error Obtener datos DB',error=str(e), status=500)    
    
    @token_required
    def post(current_user, self):        
        try:
            personaJson = request.get_json()
            personaSchema = self.schemaOne.load(personaJson)
            persona = Persona(
                per_cedula=personaSchema['per_cedula'],
                per_nombres=personaSchema['per_nombres'],
            )
            persona.save()
            data = self.schemaOne.dump(persona)
            return Response.ok(data=data, mensaje="Creado", status=201)
        except KeyError as e:
            return Response.error(mensaje='Faltan campos obligatorios', error=f"Falta el campo obligatorio '{e.args[0]}'." , status=400)
        except ValidationError as e:
            return Response.error(mensaje='Error de validación, campo incorrecto', error=e.messages, status=400)
        except Exception as e:
            return Response.error(error=str(e))
        

class PersonaWithIdController(Resource):    
    def __init__(self):
        super().__init__()
        self.schemaOne = PersonaSchema()
    
    @token_required
    def get(current_user, self, per_cedula):
        try:
            consulta = Persona.get_by_id(per_cedula)            
            data = self.schemaOne.dump(consulta)
            if not data:
                return Response.error(mensaje="No data", error='No existe una persona con ese id', status=404)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))
        
    @token_required
    def delete(current_user, self, per_cedula):
        try:
            data = Persona.get_by_id(per_cedula)                        
            if not data:
                return Response.error(mensaje="No data", error='No existe una persona con ese id', status=404)
            data.delete()
            return Response.ok(status=204)
        except Exception as e:
            return Response.error(error=str(e))
    
    @token_required
    def put(current_user, self, per_cedula):      
        try:
            persona = Persona.get_by_id(per_cedula)
            if not persona:
                return Response.error(mensaje="No data", error='No existe una persona con ese id', status=404)
            persona.per_cedula=request.json['per_cedula']
            persona.per_nombres=request.json['per_nombres']
            persona.save()            
            return Response.ok(mensaje="Actualizado", data=self.schemaOne.dump(persona))
        except KeyError as e:
            return Response.error(mensaje='Faltan campos obligatorios', error=f"Falta el campo obligatorio '{e.args[0]}'." , status=400)
        except ValidationError as e:
            return Response.error(mensaje='Error de validación, campo incorrecto', error=e.messages, status=400)
        except Exception as e:
            return Response.error(error=str(e))
    

class NotasPorCursoMateriaController(Resource):
    def __init__(self):
        super().__init__()

    @token_required
    def get(current_user, self, cur_id, mat_id):
        try:
            # Construcción de la consulta
            consulta = (
                Nota.query
                .with_entities(
                    Usuario.usu_id,
                    Usuario.per_cedula,
                    Persona.per_nombres,                
                    func.max(case((Nota.par_id == 1, Nota.not_nota))).label('Nota1'),
                    func.max(case((Nota.par_id == 1, Nota.not_id))).label('Nota1Id'),
                    func.max(case((Nota.par_id == 2, Nota.not_nota))).label('Nota2'),
                    func.max(case((Nota.par_id == 2, Nota.not_id))).label('Nota2Id')
                )
                .join(Usuario, Usuario.usu_id == Nota.usu_id)
                .join(Persona, Persona.per_cedula == Usuario.per_cedula)
                .filter(Nota.cur_id == cur_id, Nota.mat_id == mat_id)
                .group_by(Usuario.usu_id ,Usuario.per_cedula, Persona.per_nombres)
                .all()
            )

            # Formatear los resultados
            data = [
                {
                    "usu_id": row.usu_id,
                    "per_cedula": row.per_cedula,
                    "per_nombres": row.per_nombres,
                    "Nota1": row.Nota1,
                    "Nota1Id": row.Nota1Id,
                    "Nota2": row.Nota2,
                    "Nota2Id": row.Nota2Id
                }
                for row in consulta
            ]

            return Response.ok(data=data)

        except ValidationError as e:
            return Response.error(mensaje='Error de validación', error=e.messages, status=400)
        except Exception as e:
            return Response.error(mensaje='Error al obtener las notas', error=str(e), status=500)