from turtle import title
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, jsonify
from flask_login import login_required, current_user
from .models import Laporan
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, TextAreaField
from wtforms.validators import DataRequired
from . import db
import json

views = Blueprint('views', __name__)

# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# Form untuk Laporan (add & update)
class LaporanForm(FlaskForm):
    tanggal = DateField('Tanggal', validators=[DataRequired()])
    nopol = StringField('Nomor Polisi', validators=[DataRequired()])
    sopir = StringField('Nama Sopir', validators=[DataRequired()])
    km_awal = IntegerField('KM Awal', validators=[DataRequired()])
    km_isi = IntegerField('KM Isi')
    solar_awal = IntegerField('Solar Awal', validators=[DataRequired()])
    tujuan = TextAreaField('Tujuan')
    submit = SubmitField('Submit') 

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    list_laporan = Laporan.query.all()
    return render_template("home.html", user=current_user, laporan=list_laporan)

@views.route('/laporan/<int:id>')
def laporan(id):
    laporan =  Laporan.query.get_or_404(id)
    return render_template('laporan.html', user=current_user, laporan=laporan)

@views.route('/add-laporan', methods=['GET', 'POST'])
@login_required
def add_laporan():
    form = LaporanForm()
    if form.validate_on_submit():
        tanggal = form.tanggal.data
        nopol = form.nopol.data.upper()
        sopir = form.sopir.data
        km_awal = form.km_awal.data
        km_isi = form.km_isi.data
        solar_awal = form.solar_awal.data
        tujuan = form.tujuan.data


        # date = request.form.get('date')
        # y, m, d = date.split('-')
        # nopol = request.form.get('nopol').upper()
        # sopir = request.form.get('sopir')
        # km_awal = request.form.get('km_awal')
        # km_isi = request.form.get('km_isi')
        # solar_awal = request.form.get('solar_awal')
        # tujuan = request.form.get('tujuan')

        cek_nopol = Laporan.query.filter_by(nopol=nopol).first()
        cek_tgl = Laporan.query.filter_by(tanggal=tanggal).first()

        if km_awal =="":
            km_awal = 0
        
        if km_isi == "":
            km_isi = 0

        if solar_awal =="":
            solar_awal = 0
        # datetime(int(y), int(m), int(d))
        if cek_nopol and cek_tgl:
            flash('Nomor Polisi sudah ada di tanggal yang sama.', category='error')
        else :
            new_post = Laporan(tanggal=tanggal, nopol=nopol, sopir=sopir, km_awal=km_awal, 
            km_isi=km_isi, solar_awal=solar_awal, tujuan=tujuan, username=current_user.username)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('views.home'))

    return render_template("add_laporan.html", title="Tambah Laporan", form = form, user=current_user)


@views.route('/laporan/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_laporan(id):
    laporan = Laporan.query.get_or_404(id)
    form = LaporanForm()
    print(laporan.tanggal)
    if laporan.username != current_user.username:
        abort(403)
    if form.validate_on_submit():
        laporan.tanggal = form.tanggal.data
        laporan.nopol = form.nopol.data
        laporan.sopir = form.sopir.data
        laporan.km_awal = form.km_awal.data
        laporan.km_isi = form.km_isi.data
        laporan.solar_awal = form.solar_awal.data
        laporan.tujuan = form.tujuan.data
        db.session.commit()
        flash('Data laporan berhasil diupdate!', 'success')
        return redirect(url_for('views.laporan', id=laporan.id))
    elif request.method == 'GET':
        form.tanggal.data = laporan.tanggal
        form.nopol.data = laporan.nopol
        form.sopir.data = laporan.sopir
        form.km_awal.data = laporan.km_awal
        form.km_isi.data = laporan.km_isi
        form.solar_awal.data = laporan.solar_awal
        form.tujuan.data = laporan.tujuan
    return render_template('add_laporan.html', title="Update Laporan", form = form, user=current_user)

@views.route('/laporan/<int:id>/delete', methods=['POST'])
@login_required
def delete_laporan(id):
    laporan = Laporan.query.get_or_404(id)
    if laporan.username != current_user.username:
        abort(403)
    db.session.delete(laporan)
    db.session.commit()
    flash('Laporan berhasil dihapus', 'success')
    return redirect(url_for('views.home'))
    

# # Aktivitas
# @views.route('/update-aktivitas', methods=['GET', 'POST'])
# def update_aktivitas():
#     if request.method == 'POST':
#         status = Aktivitas.query.get(request.form.get('status'))
#         status.name = "finished"
#         db.session.commit()

#     return render_template("home.html", user=current_user)

# @views.route('/delete-aktivitas', methods=['POST'])
# def delete_aktivitas():
#     aktivitas = json.loads(request.data)
#     IdAktivitas = aktivitas['IdAktivitas']
#     aktivitas = Aktivitas.query.get(IdAktivitas)
#     if aktivitas:
#         if aktivitas.username == current_user.username:
#             db.session.delete(aktivitas)
#             db.session.commit()

#     return jsonify({})