from datetime import datetime
from application.conn.db import db, BaseModelMixin
from application.ext import ma
from marshmallow import fields, validates, ValidationError


class Asignacion(db.Model, BaseModelMixin):
    __tablename__ = "asignacion"
    asi_id = db.Column(db.Integer(), primary_key=True)
    enc_id = db.Column(db.Integer(), db.ForeignKey("encuesta.enc_id"))
    usu_id = db.Column(db.Integer(), db.ForeignKey("usuario.usu_id"))
    cur_id = db.Column(db.Integer(), db.ForeignKey("curso.cur_id"))
    asi_descripcion = db.Column(db.String(100))
    mat_id = db.Column(db.Integer(), db.ForeignKey("materia.mat_id"))
    asi_fecha_completado = db.Column(db.DateTime, default=datetime.utcnow)
    asi_realizado = db.Column(db.Boolean)
    usu_id_asignador = db.Column(db.Integer(), nullable=True) 
    par_parcial_seleccionado = db.Column(db.Integer(), nullable=True) 

    encuesta = db.relationship("Encuesta", backref="asignaciones")
    curso = db.relationship("Curso", backref="asignaciones")
    usuario = db.relationship("Usuario", backref="asignaciones")
    materia = db.relationship("Materia", backref="asignaciones")

    @classmethod
    def get_by_usu_id(cls, usu_id):
        return cls.query.filter_by(usu_id=usu_id).all()
    
    @classmethod
    def delete_by_filters(cls, enc_id, cur_id, mat_id, par_parcial_seleccionado, usu_id_asignador):
        """
        Elimina registros basados en filtros específicos.
        """
        try:
            # Realizar la eliminación
            rows_deleted = (
                cls.query.filter(
                    cls.enc_id == enc_id,
                    cls.cur_id == cur_id,
                    cls.mat_id == mat_id,
                    cls.par_parcial_seleccionado == par_parcial_seleccionado,
                    cls.usu_id_asignador == usu_id_asignador
                ).delete(synchronize_session=False)
            )

            # Confirmar la transacción directamente con db.session
            db.session.commit()
            return rows_deleted
        except Exception as e:
            # Hacer rollback en caso de error
            db.session.rollback()
            raise RuntimeError(f"Error al eliminar registros: {str(e)}")


    
    @classmethod
    def get_by_cur_id(cls, cur_id):
        return cls.query.filter_by(cur_id=cur_id).all()

    def __init__(
        self,
        enc_id,
        usu_id,
        cur_id,
        mat_id,
        asi_descripcion,
        asi_fecha_completado,
        usu_id_asignador=None,
        par_parcial_seleccionado=None
    ):
        self.enc_id = enc_id
        self.usu_id = usu_id
        self.cur_id = cur_id
        self.mat_id = mat_id 
        self.asi_descripcion = asi_descripcion
        self.asi_fecha_completado = asi_fecha_completado
        self.asi_realizado = False
        self.usu_id_asignador = usu_id_asignador
        self.par_parcial_seleccionado = par_parcial_seleccionado

    def __repr__(self):
        return f"Asignacion({self.asi_id})"

    def __str__(self):
        return f"{self.asi_id}"


class AsignacionSchema(ma.Schema):
    asi_id = fields.Int()
    enc_id = fields.Int(required=True)
    cur_id = fields.Int(required=True)
    mat_id = fields.Int(required=True)
    usu_id = fields.Int(required=True)
    asi_descripcion = fields.Str()
    asi_fecha_completado = fields.DateTime(required=True)
    asi_realizado = fields.Bool()    
    usu_id_asignador = fields.Int()
    par_parcial_seleccionado = fields.Int()
