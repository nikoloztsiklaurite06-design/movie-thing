from ext import app, db, login_manager
from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

import routes

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)