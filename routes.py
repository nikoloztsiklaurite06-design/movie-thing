from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user

from ext import app, db
from models import Movie, User
from forms import AddMovieForm, RegisterForm, LoginForm
from translations import translations


@app.route("/")
def index():
    lang = request.args.get('lang', 'ka')
    t = translations.get(lang, translations['ka'])

    search_query = request.args.get('search', '')
    genre_query = request.args.get('genre', 'ყველა')

    query = Movie.query.order_by(Movie.rating.desc())

    if search_query:
        query = query.filter(
            (Movie.title_ka.contains(search_query)) |
            (Movie.title_en.contains(search_query))
        )

    if genre_query and genre_query != 'ყველა':
        query = query.filter(Movie.genre.contains(genre_query))

    movies = query.all()

    genres = db.session.query(Movie.genre).distinct().all()
    genres = [g[0] for g in genres]

    return render_template("index.html",
                           movies=movies,
                           t=t,
                           current_lang=lang,
                           genres=genres)


@app.route("/movie/<int:movie_id>")
def movie_details(movie_id):
    lang = request.args.get('lang', 'ka')
    t = translations.get(lang, translations['ka'])

    movie = Movie.query.get_or_404(movie_id)

    return render_template("movie_details.html", movie=movie, t=t, current_lang=lang)


@app.route("/add_movie", methods=["GET", "POST"])
@login_required
def add_movie():
    lang = request.args.get('lang', 'ka')
    t = translations.get(lang, translations['ka'])

    if current_user.role != 'Admin':
        flash("წვდომა აკრძალულია!", "danger")
        return redirect(url_for('index', lang=lang))

    form = AddMovieForm()
    if form.validate_on_submit():
        new_movie = Movie(
            title_ka=form.title_ka.data,
            title_en=form.title_en.data,
            description_ka=form.description_ka.data,
            description_en=form.description_en.data,
            director=form.director.data,
            year=form.year.data,
            genre=form.genre.data,
            img_url=form.img_url.data,
            rating=form.rating.data,
            movie_url=form.movie_url.data
        )
        db.session.add(new_movie)
        db.session.commit()

        flash("ფილმი წარმატებით დაემატა!", "success")
        return redirect(url_for('index', lang=lang))

    return render_template("add_movie.html", form=form, t=t, current_lang=lang)


@app.route("/delete_movie/<int:movie_id>")
@login_required
def delete_movie(movie_id):
    if current_user.role == 'Admin':
        movie = Movie.query.get_or_404(movie_id)
        db.session.delete(movie)
        db.session.commit()
        flash("ფილმი წაიშალა ბაზიდან", "warning")

    return redirect(url_for('index'))


@app.route("/register", methods=["GET", "POST"])
def register():
    lang = request.args.get('lang', 'ka')
    t = translations.get(lang, translations['ka'])

    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("მომხმარებელი ასეთი სახელით უკვე არსებობს", "danger")
        else:
            new_user = User(username=form.username.data,
                            password=form.password.data,
                            role='Admin')
            db.session.add(new_user)
            db.session.commit()
            flash("რეგისტრაცია წარმატებულია, გაიარეთ ავტორიზაცია", "success")
            return redirect(url_for('login'))

    return render_template("register.html", form=form, t=t)


@app.route("/login", methods=["GET", "POST"])
def login():
    lang = request.args.get('lang', 'ka')
    t = translations.get(lang, translations['ka'])

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("პაროლი ან მომხმარებლის სახელი არასწორია", "danger")

    return render_template("login.html", form=form, t=t)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))