from flask_restful import Resource
from application.estilos.modelos.cursoModel import Curso, CursoSchema
from flask import request
from application.utils.response import Response
from marshmallow import ValidationError
from application.estilos.auth.authMiddleware import token_required
from application.estilos.modelos.asignacionModel import Asignacion

class CursoController(Resource):    
    def __init__(self):
        super().__init__()
        self.schemaMany = CursoSchema(many=True)
        self.schemaOne = CursoSchema()
    
    @token_required
    def get(current_user, self):        
        try:      
            consulta = Curso.get_all()                  
            data = self.schemaMany.dump(consulta)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(mensaje='Error Obtener datos DB',error=str(e), status=500)    
    
    @token_required
    def post(current_user, self):
        try:
            cursoJson = request.get_json()
            cursoSchema = self.schemaOne.load(cursoJson)
            curso = Curso(
                cur_carrera=cursoSchema['cur_carrera'],
                cur_nivel=cursoSchema['cur_nivel'],
                cur_periodo_academico=cursoSchema['cur_periodo_academico']
            )
            curso.save()
            data = self.schemaOne.dump(curso)            
            return Response.ok(data=data, mensaje="Creado", status=201)
        except KeyError as e:
            return Response.error(mensaje='Faltan campos obligatorios', error=f"Falta el campo obligatorio '{e.args[0]}'." , status=400)
        except ValidationError as e:
            return Response.error(mensaje='Error de validación, campo incorrecto', error=e.messages, status=400)
        except Exception as e:
            return Response.error(error=str(e))

class CursoWithIdUsuario(Resource):    
    def __init__(self):
        super().__init__()
        self.schemaOne = CursoSchema()
        self.schemaMany = CursoSchema(many=True)
    
    @token_required
    def get(current_user, self, usu_id):        
        try:
            consulta = (Curso.query
                        .join(Asignacion, Curso.cur_id == Asignacion.cur_id)
                        .filter(Asignacion.usu_id == usu_id)
                        .all())
            data = self.schemaMany.dump(consulta)
            if not data:
                return Response.error(mensaje="No data", error='No existen cursos para ese usuario', status=404)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))

class CursoWithIdController(Resource):    
    def __init__(self):
        super().__init__()
        self.schemaOne = CursoSchema()
    
    @token_required
    def get(current_user, self, cur_id):        
        try:
            consulta = Curso.get_by_id(cur_id)
            data = self.schemaOne.dump(consulta)
            if not data:
                return Response.error(mensaje="No data", error='No existe un curso con ese id', status=404)
            return Response.ok(data=data)
        except Exception as e:
            return Response.error(error=str(e))
    
    @token_required
    def delete(current_user, self, cur_id):
        try:
            data = Curso.get_by_id(cur_id)
            if not data:
                return Response.error(mensaje="No data", error='No existe un curso con ese id', status=404)
            data.delete()
            return Response.ok(status=204)
        except Exception as e:
            return Response.error(error=str(e))
    
    @token_required
    def put(current_user, self, cur_id):
        try:
            curso = Curso.get_by_id(cur_id)
            if not curso:
                return Response.error(mensaje="No data", error='No existe un curso con ese id', status=404)
            curso.cur_carrera=request.json['cur_carrera']
            curso.cur_nivel=request.json['cur_nivel']
            curso.save()            
            return Response.ok(mensaje="Actualizado", data=self.schemaOne.dump(curso))
        except KeyError as e:
            return Response.error(mensaje='Faltan campos obligatorios', error=f"Falta el campo obligatorio '{e.args[0]}'." , status=400)
        except ValidationError as e:
            return Response.error(mensaje='Error de validación, campo incorrecto', error=e.messages, status=400)
        except Exception as e:
            return Response.error(error=str(e))
    