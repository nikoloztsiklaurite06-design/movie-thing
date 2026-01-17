from ext import db
from flask_login import UserMixin


class Movie(db.Model):
    # ეს ხაზი დააზღვევს შეცდომას, თუ ბაზა ბოლომდე არ წაიშალა
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    title_ka = db.Column(db.String(100), nullable=False)
    title_en = db.Column(db.String(100), nullable=False)

    description_ka = db.Column(db.Text, nullable=False)
    description_en = db.Column(db.Text, nullable=False)

    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(100), nullable=False)  # გავზარდეთ ზომა მრავალი ჟანრისთვის
    img_url = db.Column(db.String(300), nullable=False)

    # ახალი ველი ბმულისთვის
    movie_url = db.Column(db.String(500), nullable=False)

    rating = db.Column(db.Float, default=0.0)


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='User')