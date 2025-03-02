CREATE TABLE artists (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE albums (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    artist INTEGER NOT NULL,
    year INTEGER,
    genre INTEGER,
    FOREIGN KEY (artist) REFERENCES artists(id),
    FOREIGN KEY (genre) REFERENCES genres(id)
);

CREATE TABLE genres (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    user INTEGER NOT NULL,
    album INTEGER NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    FOREIGN KEY (user) REFERENCES users(id),
    FOREIGN KEY (album) REFERENCES albums(id)
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    review INTEGER NOT NULL,
    comment TEXT NOT NULL,
    commenter INTEGER NOT NULL,
    FOREIGN KEY (review) REFERENCES reviews(id)
    FOREIGN KEY (commenter) REFERENCES users(id)
);
