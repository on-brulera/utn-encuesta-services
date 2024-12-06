from application.conn.db import db, BaseModelMixin
from application.estilos.modelos.asignacionModel import AsignacionSchema
from application.estilos.modelos.opcionModel import OpcionSchema
from application.estilos.modelos.preguntaModel import PreguntaSchema
from application.estilos.modelos.usuarioModel import UsuarioSchema
from application.ext import ma
from marshmallow import fields, validates, ValidationError

class Respuesta(db.Model, BaseModelMixin):
    __tablename__ = 'respuesta'
    res_id = db.Column(db.Integer, primary_key=True)
    usu_id = db.Column(db.Integer, db.ForeignKey('usuario.usu_id'))
    asi_id = db.Column(db.Integer, db.ForeignKey('asignacion.asi_id'))
    pre_id = db.Column(db.Integer, db.ForeignKey('pregunta.pre_id'))
    opc_id = db.Column(db.Integer, db.ForeignKey('opcion.opc_id'))
    res_valor_cuantitativo = db.Column(db.Integer)
    
    usuario = db.relationship('Usuario', backref='respuestas')
    asignacion = db.relationship('Asignacion', backref='respuestas')
    pregunta = db.relationship('Pregunta', backref='respuestas')
    opcion = db.relationship('Opcion', backref='respuestas')
    
    def __init__(self, usu_id, asi_id, pre_id, opc_id,res_valor_cuantitativo):
        self.usu_id = usu_id
        self.asi_id = asi_id
        self.pre_id = pre_id
        self.opc_id = opc_id
        self.res_valor_cuantitativo=res_valor_cuantitativo        
        
    def __repr__(self):
        return f'Respuesta({self.res_id})'
    
    def __str__(self):
        return f'{self.res_id}'
    
class RespuestaSchema(ma.Schema):
    res_id = fields.Int()
    usu_id = fields.Int(required=True)
    asi_id = fields.Int(required=True)
    pre_id = fields.Int(required=True)
    opc_id = fields.Int(required=True)
    res_valor_cuantitativo = fields.Int(required=True)
    usuario = fields.Nested(UsuarioSchema, only=('usu_id','usu_usuario'))
    asignacion = fields.Nested(AsignacionSchema, only=('usu_id', 'enc_id'))
    pregunta = fields.Nested(PreguntaSchema, only=('pre_enunciado',))
    opcion = fields.Nested(OpcionSchema, only=('opc_texto', 'opc_valor_cualitativo', 'opc_valor_cuantitativo'))
    

