import sqlite3
from flask import Flask
from flask import render_template, request
from werkzeug.security import generate_password_hash
import db

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    next_page = "create.html"
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template(next_page, message = "VIRHE: salasanat eivät ole samat")        
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return render_template(next_page, message = "VIRHE: tunnus on jo varattu")

    return "Tunnus luotu"
    message = request.form["username"]
    return render_template(next_page, message = "Tunnus luotu onnistuneest!")

@app.route("/search")
def search():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("index.html")
