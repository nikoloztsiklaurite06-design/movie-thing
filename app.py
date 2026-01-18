from ext import app, db, login_manager
from models import User, Movie
from flask import redirect, url_for

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

import routes

if __name__ == "__main__":
    app.run(debug=True)