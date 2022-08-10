from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Laporan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.Date())
    nopol = db.Column(db.String(100))
    sopir = db.Column(db.String(100))
    tujuan = db.Column(db.String(500))
    km_awal = db.Column(db.Integer)
    km_isi = db.Column(db.Integer)
    solar_awal = db.Column(db.Integer)
    tujuan = db.Column(db.String(500))
    e_toll = db.Column(db.Integer)
    username = db.Column(db.String(150), db.ForeignKey('user.username'))
    # img = db.relationship('image')

# class image(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     img_name = db.Column(db.String(500))
#     id_laporan = db.Column(db.Integer), db.ForeignKey('Laporan.id')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    laporan = db.relationship('Laporan')