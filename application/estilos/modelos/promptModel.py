from application.conn.db import db, BaseModelMixin
from application.ext import ma
from marshmallow import fields

class Prompt(db.Model, BaseModelMixin):
    __tablename__ = "prompt"
    pro_id = db.Column(db.Integer(), primary_key=True)
    pro_titulo = db.Column(db.String(100), nullable=False)  # Nuevo campo para el título
    pro_descripcion = db.Column(db.String(700), nullable=False)  # Descripción del prompt

    @classmethod
    def get_by_id(cls, pro_id):
        return cls.query.filter_by(pro_id=pro_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def __init__(self, pro_titulo, pro_descripcion):
        self.pro_titulo = pro_titulo
        self.pro_descripcion = pro_descripcion

    def __repr__(self):
        return f"Prompt({self.pro_id}, {self.pro_titulo})"


class PromptSchema(ma.Schema):
    pro_id = fields.Int()
    pro_titulo = fields.Str(required=True)  # Validación del nuevo campo
    pro_descripcion = fields.Str(required=True)  # Validación para la descripción
