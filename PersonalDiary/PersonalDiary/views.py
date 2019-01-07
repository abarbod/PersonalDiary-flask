"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from PersonalDiary import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request
from PersonalDiary.forms import RegistrationForm, LoginForm, DiaryNoteForm
from PersonalDiary.models import User, DiaryNote



@app.route('/home')
@app.route('/')
def home():
    """Renders the home page."""   
    return render_template(
            'index.html',
            title='Home Page',
            year=datetime.now().year,  
            )



@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/note')
def note():
    """Renders the about page."""
    if current_user.is_authenticated:
        notes = DiaryNote.query.filter_by(user_id=current_user.id).all() 
    else:
        notes = []

    return render_template(
        'note.html',
        title='About',
        year=datetime.now().year,
        notes = notes        
    )

@app.route('/note/new', methods=["GET","POST"])
def create_note():
    form = DiaryNoteForm()
    if form.validate_on_submit():       
        post = DiaryNote(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')       
        return redirect(url_for('home'))
    return render_template('create_note.html', title='New Post', form=form, legend='New Post')
   
@app.route("/note/<int:note_id>")
def viwe_note(note_id):
    note = DiaryNote.query.get_or_404(note_id)
    return render_template('viwe_note.html', title=note.title, note=note)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('/'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
