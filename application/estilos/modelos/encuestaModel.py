from application.conn.db import db, BaseModelMixin
from application.ext import ma
from marshmallow import fields, validates, ValidationError
from datetime import datetime

class Encuesta(db.Model, BaseModelMixin):
    __tablename__ = 'encuesta'    
    enc_id = db.Column(db.Integer(), primary_key=True)
    enc_titulo = db.Column(db.String(75))
    enc_descripcion = db.Column(db.String(300))
    enc_autor = db.Column(db.String(100))
    enc_cuantitativa = db.Column(db.Boolean)
    enc_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, enc_titulo, enc_descripcion, enc_autor, enc_cuantitativa, enc_fecha_creacion):
        self.enc_titulo = enc_titulo
        self.enc_descripcion = enc_descripcion
        self.enc_autor = enc_autor
        self.enc_cuantitativa = enc_cuantitativa
        self.enc_fecha_creacion = enc_fecha_creacion
        
    def __repr__(self):
        return f'Encuesta({self.enc_titulo})'
    
    def __str__(self):
        return f'{self.enc_titulo}'
    
class EncuestaSchema(ma.Schema):    
    enc_id = fields.Int()
    enc_titulo = fields.Str(required=True)
    enc_descripcion = fields.Str(required=True)
    enc_autor = fields.Str()
    enc_cuantitativa = fields.Bool()
    enc_fecha_creacion = fields.DateTime()    

    @validates('enc_titulo')
    def validate_enc_titulo(self, value):
        if len(value) == 0:
            raise ValidationError("El enc_titulo es obligatorio.")
        if len(value) > 75:
            raise ValidationError("El enc_titulo debe tener menos de 75 caracteres.")
        
    @validates('enc_descripcion')
    def validate_enc_descripcion(self, value):
        if len(value) > 100:
            raise ValidationError("El enc_descripcion debe tener menos de 100 caracteres.")
