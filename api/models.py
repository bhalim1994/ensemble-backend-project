from . import db

'''
Database model for Movie objects
'''
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, index=True)
    description = db.Column(db.String(250), default="No description provided")
    release_year = db.Column(db.Integer, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, default=0)
