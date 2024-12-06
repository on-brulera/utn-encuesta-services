from application.conn.db import db, BaseModelMixin
from application.ext import ma
from marshmallow import fields, validates, ValidationError

class Rol(db.Model, BaseModelMixin):
    __tablename__ = 'rol'    
    rol_id = db.Column(db.String(3), primary_key=True)
    rol_nombre = db.Column(db.String(30))
    rol_descripcion = db.Column(db.String(100))
    
    def __init__(self, rol_id, rol_nombre, rol_descripcion):
        self.rol_id = rol_id
        self.rol_nombre = rol_nombre
        self.rol_descripcion = rol_descripcion
        
    def __repr__(self):
        return f'Rol({self.rol_nombre})'
    
    def __str__(self):
        return f'{self.rol_nombre}'
    
class RolSchema(ma.Schema):
    rol_id=fields.Str(required=True)
    rol_nombre = fields.Str(required=True)
    rol_descripcion=fields.Str()
    
    @validates('rol_id')
    def validate_rol_id(self, value):
        if len(value) != 3:
            raise ValidationError("El rol_id debe tener exactamente 3 caracteres.")

    @validates('rol_nombre')
    def validate_rol_nombre(self, value):
        if len(value) == 0:
            raise ValidationError("El rol_nombre es obligatorio.")
        if len(value) > 30:
            raise ValidationError("El rol_nombre debe tener menos de 30 caracteres.")
        
    @validates('rol_descripcion')
    def validate_rol_descripcion(self, value):
        if len(value) == 0:
            raise ValidationError("El rol_descripcion es obligatorio, no debe estar vacía.")
        if len(value) > 100:
            raise ValidationError("El rol_descripcion debe tener más de 0 y menos de 100 caracteres.")
