from application.conn.db import db, BaseModelMixin
from application.ext import ma
from marshmallow import fields, validates, ValidationError

class Estilo(db.Model, BaseModelMixin):
    __tablename__ = 'estilo'    
    est_id = db.Column(db.Integer(), primary_key=True)
    enc_id = db.Column(db.Integer, db.ForeignKey("encuesta.enc_id"))
    est_nombre = db.Column(db.String(100))
    est_descripcion = db.Column(db.String(500))
    est_parametro = db.Column(db.Boolean)
    
    def __init__(self,enc_id ,est_nombre, est_descripcion, est_parametro):        
        self.enc_id = enc_id
        self.est_nombre = est_nombre
        self.est_descripcion = est_descripcion
        self.est_parametro = est_parametro
        
    def __repr__(self):
        return f'Estilo({self.est_nombre})'
    
    def __str__(self):
        return f'{self.est_nombre}'
    
    @classmethod
    def get_by_enc_id(cls, enc_id):        
        return cls.query.filter_by(enc_id=enc_id, est_parametro=False).all()
    
    @classmethod
    def get_by_est_id(cls, est_id):
        return cls.query.filter_by(est_id=est_id).first()

class EstiloSchema(ma.Schema):
    est_id=fields.Str()
    enc_id=fields.Int(required=True)
    est_nombre = fields.Str( required=True)
    est_descripcion=fields.Str()
    est_parametro = fields.Bool()
    
    @validates('est_nombre')
    def validate_rol_id(self, value):
        if len(value) == 0:
            raise ValidationError("El est_nombre del estilo es obligatorio, no debe estar vacío.")