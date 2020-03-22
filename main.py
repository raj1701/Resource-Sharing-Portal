from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length




with open('config.json', 'r') as c:
    params = json.load(c)["params"]


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key = 'key'


class department(db.Model):
    DCode = db.Column(db.Integer, primary_key=True)
    Dname = db.Column(db.String(50), unique=True, nullable = False)
    Ddes = db.Column(db.String(200), unique=False, nullable=False)
    ImgLink = db.Column(db.String(50), unique = False, nullable=False)


class Course(db.Model):
    CCode = db.Column(db.String(20), primary_key=True)
    Cname = db.Column(db.String(200), unique=True, nullable = False)
    DCode = db.Column(db.Integer, unique=False, nullable=False)

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=3, max=80)])
    remember = BooleanField('remember me')



@app.route("/")
def home():
    Departments = department.query.filter_by().all()
    return render_template('index.html', params=params, Departments=Departments)


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/courses")
def courses():
    return render_template('courses.html')


@app.route("/Dept")
def Dept():
    dept = request.args.get("dept",0)
    if dept=="CSE":
        q = "select * from department where DCode=1"
        DeptInfo = db.engine.execute(q)

        q = "select * from Course where DCode=1"
        DeptCourse = db.engine.execute(q)
    elif dept=="IT":
        q = "select * from department where DCode=2"
        DeptInfo = db.engine.execute(q)

        q = "select * from Course where DCode=2"
        DeptCourse = db.engine.execute(q)
    elif dept=="ECE":
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




@app.route("/login")
def login():
    form = LoginForm()

    return render_template('login.html', form = form)


if __name__=='__main__':
    app.run(debug=True)


