from ext import app, db, login_manager
from models import User, Movie
from flask import redirect, url_for

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/delete_movie/<int:movie_id>')
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('index'))


with app.app_context():
    db.create_all()
# ------------------------

if __name__ == "__main__":
    app.run(debug=True)