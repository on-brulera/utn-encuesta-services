from application.conn.db import db, BaseModelMixin
from application.ext import ma
from marshmallow import fields, validates, ValidationError

class Nota(db.Model, BaseModelMixin):
    __tablename__ = 'nota'
    
    not_id = db.Column(db.Integer(), primary_key=True)
    usu_id = db.Column(db.Integer(), db.ForeignKey('usuario.usu_id'), nullable=False)  # FK a Usuario
    cur_id = db.Column(db.Integer(), db.ForeignKey('curso.cur_id'), nullable=False)    # FK a Curso
    mat_id = db.Column(db.Integer(), db.ForeignKey('materia.mat_id'), nullable=False)   # FK a Materia
    par_id = db.Column(db.Integer(), db.ForeignKey('parcial.par_id'), nullable=False)    # FK a Parcial
    not_nota = db.Column(db.Float(), nullable=False)  # Nota

    usuario = db.relationship('Usuario', backref='notas')
    curso = db.relationship('Curso', backref='notas')
    materia = db.relationship('Materia', backref='notas')
    parcial = db.relationship('Parcial', backref='notas')

    def __init__(self, usu_id, cur_id, mat_id, par_id, not_nota):
        self.usu_id = usu_id
        self.cur_id = cur_id
        self.mat_id = mat_id
        self.par_id = par_id
        self.not_nota = not_nota

    def __repr__(self):
        return f'Nota({self.not_nota})'

class NotaSchema(ma.Schema):
    not_id = fields.Int()
    usu_id = fields.Int(required=True)
    cur_id = fields.Int(required=True)
    mat_id = fields.Int(required=True)
    par_id = fields.Int(required=True)
    not_nota = fields.Float(required=True)

    @validates('not_nota')
    def validate_not_nota(self, value):
        if value < 0 or value > 100:
            raise ValidationError("La nota debe estar entre 0 y 100.")
