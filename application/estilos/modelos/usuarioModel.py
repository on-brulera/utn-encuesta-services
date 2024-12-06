from sqlalchemy import and_
from application.conn.db import db, BaseModelMixin
from application.ext import ma
from marshmallow import fields, validates, ValidationError


class Usuario(db.Model, BaseModelMixin):
    __tablename__ = "usuario"
    usu_id = db.Column(db.Integer(), primary_key=True)
    rol_codigo = db.Column(db.String(3), db.ForeignKey("rol.rol_id"))
    per_cedula = db.Column(db.String(10), db.ForeignKey("persona.per_cedula"),unique=True)
    cur_id = db.Column(db.Integer(), db.ForeignKey("curso.cur_id"))
    usu_usuario = db.Column(db.String(25))
    usu_password = db.Column(db.String(60))
    usu_estado = db.Column(db.Boolean, default=False)
    rol = db.relationship("Rol", backref="usuarios")
    persona = db.relationship("Persona", backref="usuarios")
    curso = db.relationship("Curso", backref="usuarios")

    def __init__(
        self, rol_codigo, per_cedula, cur_id, usu_usuario, usu_password, usu_estado
    ):
        self.rol_codigo = rol_codigo
        self.per_cedula = per_cedula
        self.cur_id = cur_id
        self.usu_usuario = usu_usuario
        self.usu_password = usu_password
        self.usu_estado = usu_estado

    def __repr__(self):
        return f"Usuario({self.usu_usuario})"

    def __str__(self):
        return f"{self.usu_usuario}"

    @classmethod
    def get_by_cedula(cls, per_cedula):
        return cls.query.filter_by(per_cedula=per_cedula).first()

    @classmethod
    def get_by_rol_codigo(cls, rol_codigo):
        return cls.query.filter_by(rol_codigo=rol_codigo).all()


class UsuarioSchema(ma.Schema):
    usu_id = fields.Int()
    usu_usuario = fields.Str(required=True)
    usu_password = fields.Str(required=True)
    rol_codigo = fields.Str(required=True)
    per_cedula = fields.Str(equired=True)
    cur_id = fields.Int(required=True)
    usu_estado = fields.Bool()    

    @validates("usu_usuario")
    def validate_usu_usuario(self, value):
        if len(value) == 0:
            raise ValidationError("El usu_usuario es obligatorio.")
        if len(value) > 25:
            raise ValidationError("El usu_usuario debe tener menos de 25 caracteres.")

    @validates("usu_password")
    def validate_usu_password(self, value):
        if len(value) == 0:
            raise ValidationError("El usu_password es obligatorio.")
        if len(value) > 60:
            raise ValidationError("El usu_password debe tener menos de 60 caracteres.")
