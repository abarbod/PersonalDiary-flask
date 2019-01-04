"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from PersonalDiary import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request
from PersonalDiary.forms import RegistrationForm, LoginForm
from PersonalDiary.models import User, Post

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

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/note')
def note():
    return render_template("blogWrite.html")

@app.route("/uploadimage/", methods=["POST",])
def UploadImage():
    app.logger.debug(request.files)
    f = request.files.get("WriteBlogImage")
    if f and allowed_file(f.filename):
        filename = secure_filename(f.filename)
        filedir  = os.path.join(app.root_path, UPLOAD_FOLDER)
        if not os.path.exists(filedir): os.makedirs(filedir)
        app.logger.debug(filedir)
        f.save(os.path.join(filedir, filename))
        imgUrl = request.url_root + IMAGE_UPLOAD_DIR + filename
        res =  Response(imgUrl)
        res.headers["ContentType"] = "text/html"
        res.headers["Charset"] = "utf-8"
        return res
    else:
        result = r"error|未成功获取文件，上传失败"
        res =  Response(result)
        res.headers["ContentType"] = "text/html"
        res.headers["Charset"] = "utf-8"
        return res

@app.route("/test/")
def GetImage():
    return """<html><body>
<form action="/uploadimage/" method="post" enctype="multipart/form-data" name="upload_form">
  <label>选择图片文件</label>
  <input name="WriteBlogImage" type="file" accept="image/gif, image/jpeg"/>
  <input name="upload" type="submit" value="上传" />
</form>
</body></html>"""

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
