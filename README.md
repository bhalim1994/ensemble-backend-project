# Movie API
An API to manage, search, and like/dislike movies.

# App Instructions
1) `cd` to the project root on your Terminal
2) Input `pip install flask flask-sqlalchemy` or `pip3 install flask flask-sqlalchemy` (Python 3)
3) (Optional) If you do not have a .db file, you can create a database by inputting `python create_db.py`
4) Input `flask --app api --debug run` to run the Movie API in debug mode

# Database Instructions
1) `cd` to the project root on your Terminal
2) (Optional) If you do not have SQLite installed, you can install it from https://www.sqlite.org/download.html
3) Input `sqlite3 api/database.db`
4) Input `.tables` to show tables
5) Input `SELECT * FROM movie;` to show what is inside the movie table


# Project Layout
1) `api/__init__.py` - Initializes the application
2) `api/models.py` - Contains the Movie model
3) `api/views.py` - Contains the API routes
4) `create_db.py` - Simple script to create the database for the first time

# Technologies Used
1) Python
2) Flask & Flask-SQLAlchemy
3) SQLite
