# app.py
from flask import Flask
from flask_login import LoginManager
import matplotlib.pyplot as plt

from models import db, User

# Import Blueprints
from routes.auth_routes import auth_bp
from routes.customer_routes import customer_bp
from routes.author_routes import author_bp
from routes.book_routes import book_bp
from routes.order_routes import order_bp
from routes.chart_routes import chart_bp


# ---------------- APP SETUP ----------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret123'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------- REGISTER BLUEPRINTS ----------------
app.register_blueprint(auth_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(author_bp)
app.register_blueprint(book_bp)
app.register_blueprint(order_bp)
app.register_blueprint(chart_bp)

# ---------------- CREATE DB ----------------
with app.app_context():
    db.create_all()


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
