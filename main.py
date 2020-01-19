from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import json

with open('config.json', 'r') as c:
    params = json.load(c)["params"]


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key = 'key'


class Departments(db.Model):
    DeptNo = db.Column(db.Integer, primary_key=True)
    DeptName = db.Column(db.String(50), unique=True, nullable = False)
    DeptInfo = db.Column(db.String(200), unique=False, nullable=False)
    NoOfCouses = db.Column(db.Integer, unique=False, nullable=True)


@app.route("/")
def home():
    departments = Departments.query.filter_by().all()
    return render_template('index.html', params=params, departments=departments)


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/courses")
def courses():
    return render_template('courses.html')


@app.route("/login")
def login():
    return render_template('login.html')


if __name__=='__main__':
    app.run(debug=True)


