from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                flash('Login Berhasil!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password Salah, Coba Lagi.', category='error')
        else:
            flash('Username Tidak Ditemukan', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username telah digunakan.', category='error')
        elif len(username) < 4:
            flash('Username terlalu pendek', category='error')
        elif password1 != password2:
            flash('Password tidak sama.', category='error')
        elif len(password1) < 4:
            flash('Password harus lebih dari 3 karakter.', category='error')
        else:
            new_user = User(username=username, password=password1)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Akun telah dibuat', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
