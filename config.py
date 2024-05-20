from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

SECRET_KEY = '4YrzfpQ4kGXjuP6wasdfKJwer*&6qwasd'

DB = {
    'host': 'localhost:3306',
    # 'host': 'localhost:3305',
    'user': 'root',
    # 'pass': 'develmysql', 
    'pass': 'password',
    'name': 'simplegram'
}

DB_URI = f'mysql+pymysql://{DB["user"]}:{DB["pass"]}@{DB["host"]}/{DB["name"]}?charset=utf8mb4'

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'sg.login'

import simplegram.routes as routes
