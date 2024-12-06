from datetime import datetime
from application.conn.db import db, BaseModelMixin
from application.ext import ma
from marshmallow import fields, validates, ValidationError

class Historial(db.Model, BaseModelMixin):
    __tablename__ = "historial"
    his_id = db.Column(db.Integer, primary_key=True)
    cur_id = db.Column(db.Integer, db.ForeignKey("curso.cur_id"))
    asi_id = db.Column(db.Integer, db.ForeignKey("asignacion.asi_id"))
    est_cedula = db.Column(db.String(10), db.ForeignKey("persona.per_cedula"))
    his_resultado_encuesta = db.Column(db.String(500))
    his_nota_estudiante = db.Column(db.String(500))
    his_fecha_encuesta = db.Column(db.DateTime, default=datetime.utcnow)

    curso = db.relationship("Curso", backref="historiales")
    asignacion = db.relationship("Asignacion", backref="historiales")
    persona = db.relationship("Persona", backref="historiales")
    
    def __init__(self,cur_id, asi_id, est_cedula, his_resultado_encuesta, his_nota_estudiante, his_fecha_encuesta):
        self.cur_id = cur_id
        self.asi_id = asi_id
        self.est_cedula = est_cedula
        self.his_resultado_encuesta = his_resultado_encuesta
        self.his_fecha_encuesta = his_fecha_encuesta
        self.his_nota_estudiante = his_nota_estudiante
        
        
    def __repr__(self):
        return f'Historial({self.his_id})'
    
    def __str__(self):
        return f'{self.his_id}'


class HistorialSchema(ma.Schema):
    his_id = fields.Int()
    cur_id = fields.Int()
    asi_id = fields.Int()
    est_cedula = fields.Str()
    his_resultado_encuesta = fields.Str()
    his_nota_estudiante = fields.Str()
    his_fecha_encuesta = fields.DateTime()

    @validates("est_cedula")
    def validate_est_cedula(self, value):
        if len(value) == 0:
            raise ValidationError("El campo est_cedula es obligatorio.")
        if len(value) < 10:
            raise ValidationError("El campo est_cedula debe ser de 10 digitos")