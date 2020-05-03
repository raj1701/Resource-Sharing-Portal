from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import json
import os
from flask import send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


with open('config.json', 'r') as c:
    params = json.load(c)["params"]


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/Resources'
app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key = 'key'

login_manager = LoginManager()
login_manager.init_app(app)


class Uploaders(db.Model):
    UNumber = db.Column(db.Integer, primary_key=True)
    Dname = db.Column(db.String(20), unique=True, nullable=True)


class Resources(db.Model):
    Rno = db.Column(db.Integer, primary_key=True)
    Rname = db.Column(db.String(20), unique=False, nullable=True)
    RDescription = db.Column(db.String(100), unique=False, nullable=True)
    CCode = db.Column(db.String(20), unique=False, nullable=True)
    UNumber = db.Column(db.Integer)
    filepath = db.Column(db.String(100), unique=False, nullable=True)


class department(db.Model):
    DCode = db.Column(db.Integer, primary_key=True)
    Dname = db.Column(db.String(50), unique=True, nullable=False)
    Ddes = db.Column(db.String(200), unique=False, nullable=False)
    ImgLink = db.Column(db.String(50), unique=False, nullable=False)


class Course(db.Model):
    CCode = db.Column(db.String(20), primary_key=True)
    Cname = db.Column(db.String(200), unique=True, nullable=False)
    DCode = db.Column(db.Integer, unique=False, nullable=False)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), unique=True, nullable=False)
    FirstName = db.Column(db.String(50), unique=False, nullable=False)
    LastName = db.Column(db.String(50), unique=False, nullable=False)
    Email = db.Column(db.String(50), unique=True, nullable=False)
    Password = db.Column(db.String(50), unique=False, nullable=False)


@app.route("/")
def home():
    Departments = department.query.filter_by().all()
    return render_template('index.html', params=params, Departments=Departments)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.Username.in_(
            [username]), User.Password.in_([password])).first()

        if user:
            login_user(user)
            return redirect("/")
        else:
            return "Wrong username or password"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "You are logged out"


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/course/<string:crs>")
def course(crs):

    q = "select * from Resources where CCode='"+crs+"'"
    ResourceInfo = db.engine.execute(q)

    q = "select * from Course where CCode='"+crs+"'"
    CourseInfo = db.engine.execute(q)

    return render_template('course.html', CourseInfo=CourseInfo, ResourceInfo=ResourceInfo)


@app.route("/Dept/<string:dept>")
def Dept(dept):
    if dept == "CSE":
        q = "select * from department where DCode=1"
        DeptInfo = db.engine.execute(q)

        q = "select * from Course where DCode=1"
        DeptCourse = db.engine.execute(q)
    elif dept == "IT":
        q = "select * from department where DCode=2"
        DeptInfo = db.engine.execute(q)

        q = "select * from Course where DCode=2"
        DeptCourse = db.engine.execute(q)
    elif dept == "ECE":
        q = "select * from department where DCode=3"
        DeptInfo = db.engine.execute(q)

        q = "select * from Course where DCode=3"
        DeptCourse = db.engine.execute(q)
    else:
        q = "select * from department where DCode=4"
        DeptInfo = db.engine.execute(q)

        q = "select * from Course where DCode=4"
        DeptCourse = db.engine.execute(q)

    return render_template('department.html', DeptInfo=DeptInfo, DeptCourse=DeptCourse)


@app.route("/uploader/<string:crs>", methods=['GET', 'POST'])
def uploader(crs):
    if (request.method == 'POST'):

        name = request.form.get('name')
        rname = request.form.get('rname')
        rdes = request.form.get('rdes')

        q = "select count(*) from Uploaders where UName='"+name+"'"

        Uplds = db.engine.execute(q)

        for Upld in Uplds:

            if Upld[0] == 0:
                q = "insert into Uploaders (Uname) values ('"+name+"')"
                db.engine.execute(q)

        q = "select UNumber from Uploaders where UName='"+name+"'"
        unums = db.engine.execute(q)

        upnum = 0

        for unum in unums:
            upnum = unum[0]

        f = request.files['file1']

        file_path = os.path.join(
            app.config['UPLOAD_FOLDER'], secure_filename(f.filename))

        f.save(file_path)

        q = "insert into Resources (Rname, RDescription, CCode, UNumber, filepath) values ('" + \
            rname+"', '"+rdes+"', '"+crs+"', "+str(upnum)+",'"+file_path+"')"

        db.engine.execute(q)

        flash('Resource Succesfully Uploaded')

        return redirect('course?crs='+crs+'')

        # q = "select * from Resources where CCode='"+crs+"'"
        # ResourceInfo = db.engine.execute(q)

        # q = "select * from Course where CCode='"+crs+"'"
        # CourseInfo = db.engine.execute(q)

        # return render_template('course.html', CourseInfo=CourseInfo, ResourceInfo=ResourceInfo)


@app.route("/download/<string:crs>")
def download(crs):

    q = "select filepath from Resources where Rno="+str(crs)+""

    paths = db.engine.execute(q)

    filepath = "x"

    for path in paths:
        filepath = path[0]

    return send_file(filepath, as_attachment=True)


# @app.route("/login")
# def login():

#     return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
