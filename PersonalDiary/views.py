"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from PersonalDiary import app

@app.route('/')
@app.route('/home')
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
def index():
    return render_template("blogWrite.html")

#对图片上传进行响应
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

