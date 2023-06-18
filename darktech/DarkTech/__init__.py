from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\CODE\\BUSINESS\\Dark Tech\\intento 2\\DarkTech-web-v2-main\\darktech\\instance\\site.db'
    db.init_app(app)

    with app.app_context():
        db.create_all()

    from DarkTech.routes import main
    app.register_blueprint(main)

    return app
