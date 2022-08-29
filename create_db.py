from api.models import Movie
from api import db, create_app

# Only run this script to first create or reset the database
db.create_all(app=create_app())
