import os
from flask import Flask

from database import db

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{0}'.format(os.path.join(basedir, 'db.sqlite3'))

# Init db
db.init_app(app)

with app.app_context():
    from models import AccessRequest, Animal, Center, Species
    db.create_all()

# Run server
if __name__ == "__main__":
    app.run(debug=True)