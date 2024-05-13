from flask import render_template, redirect, flash, url_for
from simplegram.forms import LoginForm, RegisterForm, ProfileForm
from simplegram.models.models import Post, User, Comment, Bookmark, Message, Like
from config import db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, current_user, login_required

def login():
    if current_user.is_authenticated:
        return redirect('/')

    loginForm = LoginForm()
    return render_template('login.html', form=loginForm)

def login_post():
    # from bootstrap import bcrypt
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user: 
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect('/')
            else:
                flash({'error': 'Username & Password tidak sesuai'})
        else:
            flash({'error': 'Username & Password tidak sesuai'})
    
    return render_template('login.html', form=form)

def register():
    if current_user.is_authenticated:
        return redirect('/')
    
    form = RegisterForm()
    return render_template('register.html', form=form)

def register_post():
    # from bootstrap import bcrypt
    form = RegisterForm()
    if form.validate_on_submit():
        safe_pass = generate_password_hash(form.password.data)
        newUser = User(username=form.username.data, email=form.email.data, 
                       password=safe_pass, fullname=form.fullname.data)
        db.session.add(newUser)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html', form=form)

# Perbaikan Kode

@login_required
def my_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        user.fullname = form.fullname.data
        user.description = form.description.data
        if form.profpic.data:
            filename = secure_filename(form.profpic.data.filename)
            form.profpic.data.save(f'./static/uploads/{filename}')
            user.profpic = filename
        if form.password.data:
            user.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash({'info': 'Profil berhasil diperbarui'})
        return redirect('/myprofile')
    form.fullname.data = current_user.fullname
    form.description.data = current_user.description
    form.profpic.data = current_user.profpic
    return render_template('profil.html', form=form)

def logout():
    logout_user()
    return redirect('/login')