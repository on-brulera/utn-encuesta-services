from application.conn.db import db, BaseModelMixin
from application.ext import ma
from marshmallow import fields, validates, ValidationError

class ReglasCalculo(db.Model, BaseModelMixin):
    __tablename__ = 'reglascalculo'
    reg_id = db.Column(db.Integer, primary_key=True)
    enc_id = db.Column(db.Integer, db.ForeignKey('encuesta.enc_id'))
    reglas_json = db.Column(db.JSON)
    # Relaciones
    encuesta = db.relationship('Encuesta', backref='reglascalculo')
    
    def __init__(self, enc_id, reglas_json):
        self.enc_id = enc_id
        self.reglas_json = reglas_json
        
    def __repr__(self):
        return f'Reglas({self.enc_id})'
    
    def __str__(self):
        return f'{self.enc_id}'

class ReglasCalculoSchema(ma.Schema):
    reg_id = fields.Int()
    enc_id = fields.Int(required=True)
    reglas_json = fields.Raw()

    @validates('enc_id')
    def validate_enc_id(self, value):
        if value <= 0:
            raise ValidationError("El campo enc_id es obligatorio (Id de la encuesta).")
