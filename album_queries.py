import db

def top_ten_albums():
    sql = """SELECT 
        artists.name,
        albums.name,
        genres.name,
        albums.year,
        AVG(rating) as average_rating
        FROM reviews
        JOIN albums ON reviews.album = albums.id
        JOIN artists ON albums.artist = artists.id
        JOIN genres on albums.genre = genres.id
        GROUP BY artists.name, albums.name, genres.name, albums.year
        ORDER BY average_rating DESC
        LIMIT 10;"""

    return db.query(sql,[])

def users_reviews(username):
    sql = """ SELECT
        artists.name,
        albums.name,
        genres.name,
        albums.year,
        rating,
        reviews.id
        FROM reviews
        JOIN albums ON reviews.album = albums.id
        JOIN artists ON albums.artist = artists.id
        JOIN users ON reviews.user = users.id
        JOIN genres on albums.genre = genres.id
        WHERE users.username  = ?;"""

    return db.query(sql,[username])

def return_reviewer(review_id):
    sql = """ SELECT
        users.id
        FROM reviews
        JOIN users ON reviews.user = users.id
        WHERE reviews.id  = ?;"""
    
    return db.query(sql,[review_id])
    
def artists_albums(artist):
    sql = """ SELECT
        artists.name as artist,
        albums.name as album,
        genres.name as genre,
        albums.year as year,
        AVG(rating) as average_rating
        FROM reviews
        JOIN albums ON reviews.album = albums.id
        JOIN artists ON albums.artist = artists.id
        JOIN genres on albums.genre = genres.id
        WHERE artists.name = ?
        GROUP BY artist, album, genre, year
        ORDER BY average_rating DESC;"""
    
    return db.query(sql, [artist])

def artist_all_reviews(artist):
    sql = """ SELECT
        artists.name,
        albums.name,
        genres.name,
        albums.year,
        rating,
        users.username
        FROM reviews
        JOIN albums ON reviews.album = albums.id
        JOIN artists ON albums.artist = artists.id
        JOIN users ON reviews.user = users.id
        JOIN genres on albums.genre = genres.id
        WHERE artists.name  = ?;"""

    return db.query(sql, [artist])

def album_all_reviews(album):
    sql = """ SELECT
        artists.name,
        albums.name,
        genres.name,
        albums.year,
        rating,
        users.username
        FROM reviews
        JOIN albums ON reviews.album = albums.id
        JOIN artists ON albums.artist = artists.id
        JOIN users ON reviews.user = users.id
        JOIN genres on albums.genre = genres.id
        WHERE albums.name  = ?;"""
    
    return db.query(sql, [album])


def albums_in_genre(genre):
    sql = """ SELECT
        artists.name as artist,
        albums.name as album,
        genres.name as genre,
        albums.year as year,
        AVG(rating) as average_rating
        FROM reviews
        JOIN albums ON reviews.album = albums.id
        JOIN artists ON albums.artist = artists.id
        JOIN genres on albums.genre = genres.id
        WHERE genres.name = ?
        GROUP BY artist, album, genre, year
        ORDER BY average_rating DESC;"""
        
    return db.query(sql, [genre])

def genre_reviews(genre):
    sql = """ SELECT
        artists.name,
        albums.name,
        genres.name,
        albums.year,
        rating,
        users.username
        FROM reviews
        JOIN albums ON reviews.album = albums.id
        JOIN artists ON albums.artist = artists.id
        JOIN users ON reviews.user = users.id
        JOIN genres on albums.genre = genres.id
        WHERE genres.name  = ?;"""
        
    return db.query(sql, [genre])

def year_albums(year):
    sql = """ SELECT
        artists.name as artist,
        albums.name as album,
        genres.name as genre,
        albums.year as year,
        AVG(rating) as average_rating
        FROM reviews  
        JOIN albums ON reviews.album = albums.id
        JOIN artists ON albums.artist = artists.id
        JOIN genres on albums.genre = genres.id   
        WHERE albums.year = ?
        GROUP BY artist, album, genre, year
        ORDER BY average_rating DESC;"""
    
    return db.query(sql, [year])


def year_reviews(year):
    sql = """ SELECT
        artists.name,
        albums.name,
        genres.name,
        albums.year,
        rating,
        users.username
        FROM reviews
        JOIN albums ON reviews.album = albums.id
        JOIN artists ON albums.artist = artists.id
        JOIN users ON reviews.user = users.id
        JOIN genres on albums.genre = genres.id 
        WHERE albums.year  = ?;"""
        
    return db.query(sql, [year])