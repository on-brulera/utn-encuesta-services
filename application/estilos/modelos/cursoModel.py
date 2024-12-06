from application.conn.db import db, BaseModelMixin
from application.ext import ma
from marshmallow import fields, validates, ValidationError

class Curso(db.Model, BaseModelMixin):
    __tablename__ = 'curso'    
    cur_id = db.Column(db.Integer(), primary_key=True)
    cur_carrera = db.Column(db.String(50))
    cur_nivel = db.Column(db.Integer())
    cur_periodo_academico = db.Column(db.String(60))
    
    def __init__(self, cur_carrera, cur_nivel,cur_periodo_academico):
        self.cur_carrera = cur_carrera
        self.cur_nivel = cur_nivel
        self.cur_periodo_academico = cur_periodo_academico
        
    def __repr__(self):
        return f'Curso({self.cur_carrera})'
    
    def __str__(self):
        return f'{self.cur_carrera}'

class CursoSchema(ma.Schema):
    cur_id=fields.Int()
    cur_carrera=fields.Str(required=True)
    cur_nivel=fields.Int(required=True)
    cur_periodo_academico  = fields.Str()
    
    @validates('cur_carrera')
    def validate_cur_carrera(self, value):
        if len(value) == 0:
            raise ValidationError("El cur_carrera es obligatorio.")
        if len(value) > 50:
            raise ValidationError("El cur_carrera debe tener menos de 50 caracteres.")
    
    @validates('cur_nivel')
    def validate_cur_nivel(self, value):
        if not isinstance(value, int):
            raise ValidationError("El nivel del curso, cur_nivel debe ser un número entero.")