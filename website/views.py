from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, Response
from flask_login import login_required, current_user
from sqlalchemy import desc
from .models import Laporan
import xlwt
import io


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, TextAreaField, DecimalField
from wtforms.validators import DataRequired
from . import db
import json

views = Blueprint('views', __name__)

# Form untuk Laporan (add & update)
class LaporanForm(FlaskForm):
    tanggal = DateField('Tanggal', validators=[DataRequired()])
    nopol = StringField('Nomor Polisi', validators=[DataRequired()])
    sopir = StringField('Nama Sopir', validators=[DataRequired()])
    km_awal = IntegerField('KM Awal', validators=[DataRequired()])
    km_isi = IntegerField('KM Isi')
    solar_awal = DecimalField('Solar Awal (L)')
    e_toll = IntegerField('E-Toll')
    tujuan = TextAreaField('Tujuan')
    submit = SubmitField('Submit')

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    list_laporan = Laporan.query.order_by(desc(Laporan.tanggal)).paginate(page = page, per_page=20)
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
        sopir = form.sopir.data.upper()
        km_awal = form.km_awal.data
        km_isi = form.km_isi.data
        solar_awal = form.solar_awal.data
        e_toll = form.e_toll.data
        tujuan = form.tujuan.data

        cek_nopol = Laporan.query.filter_by(nopol=nopol).first()
        cek_tgl = Laporan.query.filter_by(tanggal=tanggal).first()
        cek_sopir = Laporan.query.filter_by(sopir=sopir).first()

        if km_awal =="":
            km_awal = 0
        
        if km_isi == "":
            km_isi = 0

        if solar_awal =="":
            solar_awal = 0
            
        if cek_nopol and cek_tgl:
            flash('Nomor Polisi sudah ada di tanggal yang sama.', category='error')
        elif cek_sopir and cek_tgl: 
            flash('Sopir sudah ada di tanggal yang sama.', category='error')
        else :
            new_post = Laporan(tanggal=tanggal, nopol=nopol, sopir=sopir, km_awal=km_awal, 
            km_isi=km_isi, solar_awal=solar_awal, e_toll=e_toll, tujuan=tujuan, username=current_user.username)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('views.home'))

    return render_template("add_laporan.html", title="Tambah Laporan", form = form, user=current_user)

@views.route('/laporan/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_laporan(id):
    laporan = Laporan.query.get_or_404(id)
    form = LaporanForm()
    if laporan.username != current_user.username:
        abort(403)
    if form.validate_on_submit():
        laporan.tanggal = form.tanggal.data
        laporan.nopol = form.nopol.data.upper()
        laporan.sopir = form.sopir.data.upper()
        laporan.km_awal = form.km_awal.data
        laporan.km_isi = form.km_isi.data
        laporan.solar_awal = form.solar_awal.data
        laporan.e_toll = form.e_toll.data
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
        form.e_toll.data = laporan.e_toll
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

@views.route('/nopol', methods=['GET'])
@login_required
def get_nopol_list():
    list_laporan = Laporan.query.order_by(desc(Laporan.nopol))
    list_nopol = []
    jum_list = []
    for list in list_laporan:
        if list.nopol in list_nopol:
            jum_list[list_nopol.index(list.nopol)] += 1
        else:
            list_nopol.append(list.nopol)
            jum_list.append(1)
    data = sorted(zip(jum_list, list_nopol), key = lambda x: (-x[0], x[1]))
    return render_template('list_nopol.html', title="List Nomor Polisi",  data=data, user=current_user)

@views.route('/sopir', methods=['GET'])
@login_required
def get_sopir_list():
    list_laporan = Laporan.query.order_by(desc(Laporan.sopir))
    list_sopir = []
    jum_list = []
    for list in list_laporan:
        if list.sopir in list_sopir:
            jum_list[list_sopir.index(list.sopir)] += 1
        else:
            list_sopir.append(list.sopir)
            jum_list.append(1)
    data = sorted(zip(jum_list, list_sopir), key = lambda x: (-x[0], x[1]))
    return render_template('list_sopir.html', title="List Sopir",  data=data, user=current_user)


@views.route('/nopol/<nopol>', methods=['GET'])
@login_required
def laporan_nopol(nopol):
    page = request.args.get('page', 1, type=int)
    list_laporan = Laporan.query.filter(Laporan.nopol==nopol).order_by(desc(Laporan.tanggal)).paginate(page = page, per_page=20)
    return render_template("home.html", user=current_user, laporan=list_laporan)

@views.route('/sopir/<sopir>', methods=['GET'])
@login_required
def laporan_sopir(sopir):
    page = request.args.get('page', 1, type=int)
    list_laporan = Laporan.query.filter(Laporan.sopir==sopir).order_by(desc(Laporan.tanggal)).paginate(page = page, per_page=20)
    return render_template("home.html", user=current_user, laporan=list_laporan)

@views.route('/download/laporan/<data>', methods=['GET'])
def download_laporan(data):
    try:
        output = io.BytesIO()

        workbook = xlwt.Workbook()

        dl = workbook.add_sheet('Laporan Truk')

        dl.write(0, 1, 'Tanggal Laporan')
        dl.write(0, 2, 'Nomor Polisi')
        dl.write(0, 3, 'Nama Sopir')
        dl.write(0, 4, 'KM Awal')
        dl.write(0, 5, 'KM Isi')
        dl.write(0, 6, 'Isi Solar Awal')
        dl.write(0, 7, 'Tujuan')
        dl.write(0, 8, 'E-Toll')
    
        idx = 0
        for row in data:
            dl.write(idx+1, 1, str(row.tanggal))
            dl.write(idx+1, 2, row.nopol)
            dl.write(idx+1, 3, row.sopir)
            dl.write(idx+1, 4, row.km_awal)
            dl.write(idx+1, 5, row.km_isi)
            dl.write(idx+1, 6, row.solar_awal)
            dl.write(idx+1, 7, row.tujuan)
            dl.write(idx+1, 8, row.e_toll)
            idx += 1

        workbook.save(output)
        output.seek(0)

        return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=download.xls"})
    except Exception as e:
	    print(e)