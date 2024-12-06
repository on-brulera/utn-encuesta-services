from datetime import datetime
from application.conn.db import db, BaseModelMixin
from application.ext import ma
from marshmallow import fields, validates, ValidationError

class CredencialesAPI(db.Model, BaseModelMixin):
    __tablename__ = "credencial_api"
    
    cred_id = db.Column(db.Integer, primary_key=True)
    nombre_servicio = db.Column(db.String(100), nullable=False)
    api_key = db.Column(db.String(500), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, nombre_servicio, api_key):
        self.nombre_servicio = nombre_servicio
        self.api_key = api_key

    def __repr__(self):
        return f'CredencialesAPI({self.id})'
    
    def __str__(self):
        return f'{self.nombre_servicio}'

class CredencialesAPISchema(ma.Schema):
    cred_id = fields.Int()
    nombre_servicio = fields.Str(required=True)
    api_key = fields.Str(required=True)
    fecha_creacion = fields.DateTime()
    
    @validates("nombre_servicio")
    def validate_nombre_servicio(self, value):
        if len(value) == 0:
            raise ValidationError("El campo nombre_servicio es obligatorio.")
