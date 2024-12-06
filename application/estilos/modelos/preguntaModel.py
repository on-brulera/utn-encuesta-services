from sqlalchemy import Enum
from application.conn.db import db, BaseModelMixin
from application.ext import ma
from marshmallow import fields, validates, ValidationError

class Pregunta(db.Model, BaseModelMixin):
    __tablename__ = 'pregunta'
    pre_id = db.Column(db.Integer, primary_key=True)
    enc_id = db.Column(db.Integer, db.ForeignKey('encuesta.enc_id'))
    pre_orden = db.Column(db.Integer)
    pre_enunciado = db.Column(db.String(300))
    pre_num_respuestas_min = db.Column(db.Integer)
    pre_num_respuestas_max = db.Column(db.Integer)
    pre_valor_total = db.Column(db.Numeric)
    pre_tipo_pregunta = db.Column(Enum('seleccion', 'verdadero','likert', 'likert2', name='preguntas_enum'))    

    encuesta = db.relationship('Encuesta', backref='preguntas')
    
    def __init__(self, enc_id, pre_orden, pre_enunciado, pre_num_respuestas_min, pre_num_respuestas_max, pre_valor_total, pre_tipo_pregunta):
        self.enc_id = enc_id
        self.pre_orden = pre_orden
        self.pre_enunciado = pre_enunciado
        self.pre_num_respuestas_min = pre_num_respuestas_min
        self.pre_num_respuestas_max = pre_num_respuestas_max
        self.pre_valor_total = pre_valor_total
        self.pre_tipo_pregunta = pre_tipo_pregunta
        
    def __repr__(self):
        return f'Pregunta({self.pre_id})'
    
    def __str__(self):
        return f'{self.pre_id}'
    
    @classmethod
    def get_enum_values(cls):
        return ['seleccion', 'verdadero','likert', 'likert2']

class PreguntaSchema(ma.Schema):
    pre_id = fields.Int()
    enc_id = fields.Int(required=True)
    pre_orden = fields.Int(required=True)
    pre_enunciado = fields.Str(required=True)    
    pre_num_respuestas_min = fields.Int()
    pre_num_respuestas_max = fields.Int()    
    pre_valor_total = fields.Number()    
    pre_tipo_pregunta = fields.Str()        

    @validates('pre_enunciado')
    def validate_pre_enunciado(self, value):
        if len(value) == 0:
            raise ValidationError("El campo enunciado es obligatorio.")
        if len(value) > 300:
            raise ValidationError("El campo enunciado debe tener menos de 300 caracteres.")