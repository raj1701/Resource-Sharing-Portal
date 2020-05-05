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
    return redirect("/")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if (request.method == 'POST'):

        username = request.form.get('username')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        cnfpassword = request.form.get('cnfpassword')

        q = "select Username from user"
        usernames = db.engine.execute(q)

        f = 0

        for usrnm in usernames:
            if usrnm[0] == username:
                f = 1

        q = "select Email from user"
        emails = db.engine.execute(q)

        for emls in emails:
            if emls[0] == email:
                f = 2

        if cnfpassword == password:

            if(f == 0):

                q = "insert into user (Username, FirstName, LastName, Email, Password) values ('" + \
                    username+"', '"+firstname+"', '"+lastname+"', '"+email+"', '"+password+"')"

                db.engine.execute(q)

                user = User.query.filter(User.Username.in_(
                    [username]), User.Password.in_([password])).first()
                login_user(user)
                return redirect("/")

            elif(f == 1):

                return "Username already exists please enter a different username"

            else:
                return "Email already registered Please enter a different Email Address"

        else:
            return("Password and Confirm Password Fields should match")


@app.route("/contact")
def contact():
    Departments = department.query.filter_by().all()
    return render_template('contact.html', Departments=Departments)


@app.route("/course/<string:crs>")
def course(crs):

    q = "select * from Resources where CCode='"+crs+"'"
    ResourceInfo = db.engine.execute(q)

    q = "select * from Course where CCode='"+crs+"'"
    CourseInfo = db.engine.execute(q)

    q = "select DCode from Course where CCode='"+crs+"'"
    Deptno = db.engine.execute(q)

    deptno = 1

    for dept in Deptno:
        deptno = dept[0]

    q = "select Dname from department where DCode="+str(deptno)+""
    Deptname = db.engine.execute(q)

    deptname = ""

    for dept in Deptname:
        deptname = dept[0]

    Departments = department.query.filter_by().all()

    return render_template('course.html', CourseInfo=CourseInfo, ResourceInfo=ResourceInfo, deptname=deptname, Departments=Departments)


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

    Departments = department.query.filter_by().all()

    return render_template('department.html', DeptInfo=DeptInfo, DeptCourse=DeptCourse, Departments=Departments)


@app.route("/uploader/<string:crs>", methods=['GET', 'POST'])
def uploader(crs):
    if (request.method == 'POST'):

        rname = request.form.get('rname')
        rdes = request.form.get('rdes')
        username = request.form.get('username')
        password = request.form.get('password')

        if current_user.is_authenticated:

            if username == current_user.Username:

                user = User.query.filter(User.Username.in_(
                    [username]), User.Password.in_([password])).first()

                if user:
                    q = "select count(*) from Uploaders where UName='" + \
                        username+"'"

                    Uplds = db.engine.execute(q)

                    for Upld in Uplds:

                        if Upld[0] == 0:
                            q = "insert into Uploaders (Uname) values ('" + \
                                username+"')"
                            db.engine.execute(q)

                    q = "select UNumber from Uploaders where UName='"+username+"'"
                    unums = db.engine.execute(q)

                    upnum = 0

                    for unum in unums:
                        upnum = unum[0]

                    f = request.files['file1']

                    file_path = os.path.join(
                        app.config['UPLOAD_FOLDER'], secure_filename(f.filename))

                    f.save(file_path)

                    q = "insert into Resources (Rname, RDescription, CCode, UNumber, filepath) values ('" + \
                        rname+"', '"+rdes+"', '"+crs+"', " + \
                        str(upnum)+",'"+file_path+"')"

                    db.engine.execute(q)

                    return redirect('/course/'+crs+'')

                else:
                    return "Wrong username or password"
            else:
                return "Enter Correct Username"

        else:
            return "First Login to Upload"


@app.route("/download/<string:crs>")
def download(crs):

    q = "select filepath from Resources where Rno="+str(crs)+""

    paths = db.engine.execute(q)

    filepath = "x"

    for path in paths:
        filepath = path[0]

    return send_file(filepath, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
