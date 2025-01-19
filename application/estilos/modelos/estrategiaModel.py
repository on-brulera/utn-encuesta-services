from application.conn.db import db, BaseModelMixin
from application.ext import ma
from marshmallow import fields

class Estrategia(db.Model, BaseModelMixin):
    __tablename__ = "estrategia"
    estr_id = db.Column(db.Integer(), primary_key=True)
    est_id = db.Column(db.Integer(),  nullable=True)
    cur_id = db.Column(db.Integer(),  nullable=True)
    cur_nivel = db.Column(db.Integer(),  nullable=True)
    prom_notas = db.Column(db.String(),  nullable=True)
    enc_id = db.Column(db.Integer(),  nullable=True)
    mat_id = db.Column(db.Integer(),  nullable=True)
    estr_estrategia = db.Column(db.String(), nullable=True)

    @classmethod
    def get_by_id(cls, estr_id):
        return cls.query.filter_by(estr_id=estr_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def filter_one_by_fields(cls, est_id=None, cur_id=None, cur_nivel=None, enc_id=None, mat_id=None):
        query = cls.query
        
        if est_id is not None:
            query = query.filter_by(est_id=est_id)
        if cur_id is not None:
            query = query.filter_by(cur_id=cur_id)
        if cur_nivel is not None:
            query = query.filter_by(cur_nivel=cur_nivel)
        if enc_id is not None:
            query = query.filter_by(enc_id=enc_id)
        if mat_id is not None:
            query = query.filter_by(mat_id=mat_id)

        return query.first()


    def __init__(self, est_id, cur_id, cur_nivel, prom_notas, enc_id, mat_id, estr_estrategia):        
        self.est_id = est_id        
        self.cur_id = cur_id
        self.cur_nivel = cur_nivel
        self.prom_notas = prom_notas
        self.enc_id = enc_id
        self.mat_id = mat_id
        self.estr_estrategia = estr_estrategia

    def __repr__(self):
        return f"Estrategia({self.estr_id}, {self.cur_nivel})"


class EstrategiaSchema(ma.Schema):    
    estr_id = fields.Int(dump_only=True)
    est_id = fields.Int()
    cur_id = fields.Int()
    cur_nivel = fields.Int()
    prom_notas = fields.Str()
    enc_id = fields.Int()
    mat_id = fields.Int()
    estr_estrategia = fields.Str()
