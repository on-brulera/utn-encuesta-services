from application.conn.db import db, BaseModelMixin
from application.ext import ma
from marshmallow import fields, validates, ValidationError

class Opcion(db.Model, BaseModelMixin):
    __tablename__ = "opcion"
    opc_id = db.Column(db.Integer, primary_key=True)
    pre_id = db.Column(db.Integer, db.ForeignKey("pregunta.pre_id"))
    est_id = db.Column(db.Integer, db.ForeignKey("estilo.est_id"))
    opc_texto = db.Column(db.String(300))
    opc_valor_cualitativo = db.Column(db.String(50))
    opc_valor_cuantitativo = db.Column(db.Numeric)

    pregunta = db.relationship("Pregunta", backref="opciones")
    pregunta = db.relationship("Estilo", backref="opciones")
    
    def __init__(self, pre_id, est_id, opc_texto, opc_valor_cualitativo, opc_valor_cuantitativo, ):
        self.pre_id = pre_id
        self.est_id = est_id
        self.opc_texto = opc_texto
        self.opc_valor_cualitativo = opc_valor_cualitativo
        self.opc_valor_cuantitativo = opc_valor_cuantitativo
        
    def __repr__(self):
        return f'Opcion({self.opc_id})'
    
    def __str__(self):
        return f'{self.opc_id}'

class OpcionSchema(ma.Schema):
    opc_id = fields.Int()
    pre_id = fields.Int(required=True)
    est_id = fields.Int(required=True)
    opc_texto = fields.Str(required=True)
    opc_valor_cualitativo = fields.Str(data_key="valor_cualitativo")
    opc_valor_cuantitativo = fields.Number(data_key="valor_cuantitativo")
    

    @validates("opc_texto")
    def validate_opc_texto(self, value):
        if len(value) == 0:
            raise ValidationError("El campo opc_texto es obligatorio.")
        if len(value) > 300:
            raise ValidationError("El campo opc_texto debe tener menos de 300 caracteres.")
