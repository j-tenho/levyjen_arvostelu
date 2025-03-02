
import sqlite3
from flask import Flask
from flask import render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import config
import db
import album_queries

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html", top_albums=album_queries.top_ten_albums())

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]

    if username == "":
        flash("VIRHE: käyttäjänimi tyhjä")
        return redirect("/register")

    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2 or password1 == "":
        flash("VIRHE: salasanat eivät ole samat tai syötit tyhjän salasanan")
        return redirect("/register")

    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        flash("VIRHE: käyttäjätunnus on jo varattu.")
        return redirect("/register")

    flash("Tunnus luotu onnistuneesti. Voit nyt kirjautua sisään.")
    return redirect("/")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_test",methods =["POST"])
def login_test():
    username = request.form["username"]
    password = request.form["password"]

    if username == "":
        flash("Et syöttänyt käyttäjätunnusta. Yritä uudelleen.")
        return redirect("/login")

    sql = "SELECT password_hash FROM users WHERE username = ?"

    print(db.query(sql, [username]))

    if len(db.query(sql, [username])) == 0:
        flash("Käyttäjätunnusta ei ole olemassa")
        return redirect("/login")

    password_hash = db.query(sql, [username])[0][0]

    if check_password_hash(password_hash, password):
        session["username"] = username
        session["user_id"] = db.query("SELECT id FROM users WHERE username = ?",[username])[0][0]
        session["csrf_token"] = secrets.token_hex(16)
        flash(f"Tervetuloa {username}!")
        return redirect("/")

    flash("VIRHE: väärä tunnus tai salasana")
    return redirect("/login")

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    del session["csrf_token"]
    flash("Uloskirjautuminen onnistui.")
    return redirect("/")

@app.route("/profile/<user_name>")
def profile(user_name):
    reviews_data = album_queries.users_reviews(user_name)
    return render_template("user.html", username=user_name,reviews=reviews_data)


@app.route("/add_review")
def add_review():
    if session["user_id"]:
        return render_template("add_review.html")

    return redirect("/")

@app.route("/add_review_to_db", methods =["POST"])
def add_review_to_db():
    if session["user_id"]:
        artist = request.form["artist"]
        year = request.form["year"]
        album = request.form["album"]
        genre = request.form["genre"]
        rating = request.form.get("rating")

        print(artist)
        print(year)
        print(album)
        print(genre)
        print(rating)

        if artist == "" or year == "" or album == "" or genre == "" or rating == None:
            flash("VIRHE: kenttä tai kenttiä tyhjänä")
            return redirect("/add_review")

        try:
            sql = "SELECT id FROM artists WHERE name = ?"
            artist_id = int(db.query(sql, [artist])[0][0])

        except:
            sql = "INSERT INTO artists (name) VALUES (?)"
            db.execute(sql, [artist])
            sql = "SELECT id FROM artists WHERE name = ?"
            artist_id = int(db.query(sql, [artist])[0][0])

        try:
            sql = "SELECT id FROM genres WHERE name = ?"
            genre_id = int(db.query(sql, [genre])[0][0])

        except:
            sql = "INSERT INTO genres (name) VALUES (?)"
            db.execute(sql, [genre])
            sql = "SELECT id FROM genres WHERE name = ?"
            genre_id = int(db.query(sql, [genre])[0][0])

        try:
            sql = "SELECT id FROM albums WHERE name = ?"
            album_id = int(db.query(sql, [album])[0][0])

        except:
            sql = "INSERT INTO albums (name, artist, year, genre) VALUES (?, ?, ?, ?)"
            db.execute(sql, [album, artist_id, int(year), genre_id])
            sql = "SELECT id FROM albums WHERE name = ?"
            album_id = int(db.query(sql, [album])[0][0])

        try:
            sql = "SELECT id FROM reviews WHERE user = ? AND album = ?"
            review_id = int(db.query(sql,[session["user_id"],album_id])[0][0])
            sql = "UPDATE reviews SET rating = ? WHERE id  = ?"
            db.execute(sql,[rating, review_id])
            updated = "Edellinen arviosi on päivitetty. "

        except:
            updated = ""
            sql = "INSERT INTO reviews (user, album, rating) VALUES (?, ?, ?)"
            db.execute(sql, [session["user_id"], album_id, rating])

        message = f"{updated}Arvioit artistin {artist} albumin {album} arvosanalla {rating}."
        flash(message)


    return redirect("/")

@app.route("/delete_review/<review_id>", methods = ["POST"])
def delete_review(review_id):
    print("testi")
    print(request.form.get("csrf_token"))
    if session["user_id"] == album_queries.return_reviewer(review_id)[0][0] and request.form["csrf_token"] == session["csrf_token"]:
        sql = "DELETE FROM reviews WHERE id = ?"
        db.execute(sql, [review_id])

        flash("Arvio poistettu")

    return redirect("/")

@app.route("/modify_review/<review_id>", methods = ["POST"])
def form_modify_review(review_id):
    return render_template("/update_review.html", review_id = review_id)

@app.route("/review_updated/<review_id>", methods = ["POST"])
def update_rating(review_id):
    if session["user_id"] == album_queries.return_reviewer(review_id)[0][0] and request.form["csrf_token"] == session["csrf_token"]:
        rating = request.form["rating"]
        print(rating)

        sql = "UPDATE reviews SET rating = ?  WHERE id = ?"
        db.execute(sql, [rating, review_id])

        flash("Arvio muutettu")

    return redirect("/")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/search_results", methods =["POST"])
def search_data():
    search_variable = request.form["search_variable"]
    if search_variable == "":
        flash("VIRHE: ei hakutermiä")
        return redirect("/search")

    if request.form.get("search_type") is None:
        flash("VIRHE: hakutyyppiä ei valittu.")
        return redirect("/search")

    if request.form["search_type"] == "artist":
        return artist_page(search_variable)

    if request.form["search_type"] == "genre":
        return genre_page(search_variable)

    if request.form["search_type"] == "year":
        return year_page(search_variable)

    if request.form["search_type"] == "album":
        return album_page(search_variable)

@app.route("/artist/<artist_name>")
def artist_page(artist_name):
    averages_data = album_queries.artists_albums(artist_name)
    reviews_data = album_queries.artist_all_reviews(artist_name)

    return render_template("artist.html", artist_name=artist_name, averages=averages_data,reviews=reviews_data)

@app.route("/genre/<genre_name>")
def genre_page(genre_name):

    averages_data = album_queries.albums_in_genre(genre_name)
    reviews_data = album_queries.genre_reviews(genre_name)

    return render_template("genre.html", genre_name=genre_name, averages=averages_data,reviews=reviews_data)

@app.route("/year/<year>")
def year_page(year):

    averages_data = album_queries.year_albums(year)
    reviews_data = album_queries.year_reviews(year)

    return render_template("year.html", year=year, averages=averages_data,reviews=reviews_data)

@app.route("/album/<album_name>")
def album_page(album_name):

    reviews_data = album_queries.album_all_reviews(album_name)
    return render_template("album.html", album_name = album_name ,reviews=reviews_data)

@app.route("/review/<review_id>")
def review_page(review_id):

    review_info = album_queries.review_details(review_id)
    comments = album_queries.review_comments(review_id)

    return render_template("review.html", review_id = review_id, review_info=review_info, comments = comments)

@app.route("/add_comment", methods =["POST"])
def add_comment_to_db():
    if request.form["csrf_token"] == session["csrf_token"]:
        review_id = request.form["review_id"]
        comment = request.form["comment"]
        user_id = album_queries.return_reviewer(review_id)[0][0]

        sql = "INSERT INTO comments (review, comment, commenter) VALUES (?, ?, ?)"
        print()
        db.execute(sql, [int(review_id),comment, int(user_id)])
        flash("Kommentti lisätty")

    return redirect(f"/review/{review_id}")

@app.route("/comment/<comment_id>")
def modify_or_remove_comment(comment_id):
    comment = album_queries.return_comment(comment_id)
    print(comment)

    return render_template("modify_comment.html", comment = comment, comment_id = comment_id)

@app.route("/modify_comment/", methods = ["POST"])
def modify_comment_in_db():
    comment = request.form["comment"]
    comment_id = request.form["comment_id"]

    print(album_queries.return_commenter_id(comment_id)[0])

    if session["user_id"] == album_queries.return_commenter_id(comment_id)[0] and request.form["csrf_token"] == session["csrf_token"]:
        sql = "UPDATE comments SET comment = ?  WHERE id = ?"
        db.execute(sql, [comment, comment_id])

        flash("Kommentti muutettu")

    return redirect("/")

@app.route("/delete_comment/", methods = ["POST"])
def remove_comment_in_db():
    comment_id = request.form["comment_id"]

    if session["user_id"] == album_queries.return_commenter_id(comment_id)[0] and request.form["csrf_token"] == session["csrf_token"]:
        sql = "DELETE FROM comments WHERE id = ?"
        db.execute(sql, [comment_id])

        flash("Kommentti poistettu")

    return redirect("/")
