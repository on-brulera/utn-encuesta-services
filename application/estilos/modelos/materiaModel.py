from datetime import datetime
from application.conn.db import db, BaseModelMixin
from application.ext import ma
from marshmallow import fields, ValidationError

class Materia(db.Model, BaseModelMixin):
    __tablename__ = "materia"
    mat_id = db.Column(db.Integer(), primary_key=True)
    mat_nombre = db.Column(db.String(100), nullable=False)
    mat_descripcion = db.Column(db.String(255))

    def __init__(self, mat_nombre, mat_descripcion):
        self.mat_nombre = mat_nombre
        self.mat_descripcion = mat_descripcion

    def __repr__(self):
        return f"Materia({self.mat_id}, {self.mat_nombre})"

    def __str__(self):
        return f"{self.mat_nombre}"

class MateriaSchema(ma.Schema):
    mat_id = fields.Int(dump_only=True)
    mat_nombre = fields.Str(required=True)
    mat_descripcion = fields.Str()
