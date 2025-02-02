import sqlite3
from flask import Flask
from flask import render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    next_page = "message.html"
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

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_test",methods =["POST"]) 
def login_test():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT password_hash FROM users WHERE username = ?"
    password_hash = db.query(sql, [username])[0][0]

    if check_password_hash(password_hash, password):
        print("Toimii 1")
        session["username"] = username
        print("Toimii 2")
        return redirect("/")

    return render_template("message.html", message = "VIRHE: väärä tunnus tai salasana")
