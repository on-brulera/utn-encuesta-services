from application.conn.db import db, BaseModelMixin
from application.ext import ma
from marshmallow import fields, validates, ValidationError

class Parcial(db.Model, BaseModelMixin):
    __tablename__ = 'parcial'
    
    par_id = db.Column(db.Integer(), primary_key=True)
    par_descripcion = db.Column(db.String(100), nullable=False)  # Descripción del parcial
    
    def __init__(self, par_descripcion):
        self.par_descripcion = par_descripcion

    def __repr__(self):
        return f'Parcial({self.par_descripcion})'
    
    def __str__(self):
        return f'{self.par_descripcion}'

class ParcialSchema(ma.Schema):
    par_id = fields.Int()
    par_descripcion = fields.Str(required=True)

    @validates('par_descripcion')
    def validate_par_descripcion(self, value):
        if len(value) == 0:
            raise ValidationError("La descripción del parcial es obligatoria.")
        if len(value) > 100:
            raise ValidationError("La descripción del parcial debe tener menos de 100 caracteres.")
