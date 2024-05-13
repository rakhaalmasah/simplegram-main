from flask import Flask, render_template
from config import *
from simplegram import SG

app = Flask(__name__)
app.register_blueprint(SG)
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

with app.app_context():
    db.init_app(app)
    db.create_all()
    
    login_manager.init_app(app=app)