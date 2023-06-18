# made by Vigo Walker

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from DarkTech import create_app
from DarkTech import db


app = create_app()
app.config['SECRET_KEY'] = 'vigoproxd07'

# Import your models here. For example:
# from your_application.models import Post

def create_database():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    create_database()
    app.run(debug=True)
