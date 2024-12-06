from application.conn.db import db, BaseModelMixin
from application.ext import ma
from marshmallow import fields, validates, ValidationError

class Persona(db.Model, BaseModelMixin):
    __tablename__ = 'persona'  
    per_cedula = db.Column(db.String(), primary_key=True)
    per_nombres = db.Column(db.String(100))
    
    def __init__(self, per_cedula, per_nombres):
        self.per_cedula = per_cedula
        self.per_nombres = per_nombres
        
    def __repr__(self):
        return f'Persona({self.per_cedula})'
    
    def __str__(self):
        return f'{self.per_cedula}'
    

class PersonaSchema(ma.Schema):
    per_cedula=fields.Str(required=True)
    per_nombres=fields.Str(required=True)            
    
    @validates('per_nombres')
    def validate_per_nombres(self, value):
        if len(value) == 0:
            raise ValidationError("El per_nombres es obligatorio.")
        if len(value) > 100:
            raise ValidationError("El per_nombres debe tener menos de 50 caracteres.")
    