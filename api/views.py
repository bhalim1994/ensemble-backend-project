from flask import Blueprint, jsonify, request
from . import db
from .models import Movie

main = Blueprint('main', __name__)

'''
Creates a movie with an automatically generated unique ID
'''
@main.route('/movie', methods=['POST'])
def post_movie():
    title = request.get_json().get('title')
    description = request.get_json().get('description')
    release_year = request.get_json().get('release_year')
    duration_minutes = request.get_json().get('duration_minutes')
    rating = request.get_json().get('rating')

    if Movie.query.filter_by(title=title).first():
        return jsonify({'Error': 'Movie already exists in the database'}), 409

    if is_invalid_release_year(release_year):
        return jsonify({'Error': 'release_year needs to be a positive 4-integer value'}), 409
    if is_invalid_duration_minutes(duration_minutes):
        return jsonify({'Error': 'duration_minutes needs to be an integer greater than 0'}), 409
    if is_invalid_rating(rating):
        return jsonify({'Error': 'rating needs to be an integer'}), 409

    movie = Movie(title=title,
                  description=description,
                  release_year=release_year,
                  duration_minutes=duration_minutes,
                  rating=rating)

    db.session.add(movie)
    db.session.commit()

    return jsonify({
        'id': movie.id,
        'title': movie.title,
        'description': movie.description,
        'release_year': movie.release_year,
        'duration_minutes': movie.duration_minutes,
        'rating': movie.rating
    }), 201


'''
Gets a movie using its ID
'''
@main.route('/movie/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()

    if not movie:
        return jsonify({'Error': 'Movie not found'}), 404

    return jsonify({
        'id': movie.id,
        'title': movie.title,
        'description': movie.description,
        'release_year': movie.release_year,
        'duration_minutes': movie.duration_minutes,
        'rating': movie.rating
    }), 200


'''
Fully updates a movie using its ID
'''
@main.route('/movie/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()

    if not movie:
        return jsonify({'Error': 'Movie not found'}), 404

    title = request.get_json().get('title')
    description = request.get_json().get('description')
    release_year = request.get_json().get('release_year')
    duration_minutes = request.get_json().get('duration_minutes')
    rating = request.get_json().get('rating')

    if is_invalid_release_year(release_year):
        return jsonify({'Error': 'release_year needs to be a positive 4-integer value'}), 409
    if is_invalid_duration_minutes(duration_minutes):
        return jsonify({'Error': 'duration_minutes needs to be an integer greater than 0'}), 409
    if is_invalid_rating(rating):
        return jsonify({'Error': 'rating needs to be an integer'}), 409

    if description is None:
        description = "No description provided"
    if rating is None:
        rating = 0

    movie.title = title
    movie.description = description
    movie.release_year = release_year
    movie.duration_minutes = duration_minutes
    movie.rating = rating

    db.session.commit()

    return jsonify({
        'id': movie.id,
        'title': movie.title,
        'description': movie.description,
        'release_year': movie.release_year,
        'duration_minutes': movie.duration_minutes,
        'rating': movie.rating
    }), 200


'''
Partially updates a movie using its ID
'''
@main.route('/movie/<int:movie_id>', methods=['PATCH'])
def partial_update_movie(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()

    if not movie:
        return jsonify({'Error': 'Movie not found'}), 404

    title = request.get_json().get('title')
    description = request.get_json().get('description')
    release_year = request.get_json().get('release_year')
    duration_minutes = request.get_json().get('duration_minutes')
    rating = request.get_json().get('rating')

    if title:
        movie.title = title
    if description:
        movie.description = description

    if is_invalid_release_year(release_year):
        return jsonify({'Error': 'release_year needs to be a positive 4-integer value'}), 409
    elif release_year:
        movie.release_year = release_year

    if is_invalid_duration_minutes(duration_minutes):
        return jsonify({'Error': 'duration_minutes needs to be an integer greater than 0'}), 409
    elif duration_minutes:
        movie.duration_minutes = duration_minutes

    if is_invalid_rating(rating):
        return jsonify({'Error': 'rating needs to be an integer'}), 409
    # Cannot do "elif rating:" as a rating of 0 would evaluate to False and discard a rating of 0
    elif isinstance(rating, int):
        movie.rating = rating

    db.session.commit()

    return jsonify({
        'id': movie.id,
        'title': movie.title,
        'description': movie.description,
        'release_year': movie.release_year,
        'duration_minutes': movie.duration_minutes,
        'rating': movie.rating
    }), 200


'''
Delete a movie using its ID
'''
@main.route('/movie/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()

    if not movie:
        return jsonify({'Error': 'Movie not found'}), 404

    db.session.delete(movie)
    db.session.commit()

    return jsonify({}), 204


'''
Search a movie by its title
'''
@main.route('/movie', methods=['GET'])
def search_title():
    title = request.args.get('title')

    movie = Movie.query.filter_by(title=title).first()

    if not movie:
        return jsonify({'Error': 'Movie not found'}), 404

    return jsonify({
        'id': movie.id,
        'title': movie.title,
        'description': movie.description,
        'release_year': movie.release_year,
        'duration_minutes': movie.duration_minutes,
        'rating': movie.rating
    }), 200


'''
Anonymously like a movie using its ID
'''
@main.route('/movie/<int:movie_id>/like', methods=['GET'])
def like_movie(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()

    if not movie:
        return jsonify({'Error': 'Movie not found'}), 404

    movie.rating += 1

    db.session.commit()

    return jsonify({
        'id': movie.id,
        'title': movie.title,
        'description': movie.description,
        'release_year': movie.release_year,
        'duration_minutes': movie.duration_minutes,
        'rating': movie.rating
    }), 200


'''
Anonymously dislike a movie using its ID
'''
@main.route('/movie/<int:movie_id>/dislike', methods=['GET'])
def dislike_movie(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()

    if not movie:
        return jsonify({'Error': 'Movie not found'}), 404

    movie.rating -= 1

    db.session.commit()

    return jsonify({
        'id': movie.id,
        'title': movie.title,
        'description': movie.description,
        'release_year': movie.release_year,
        'duration_minutes': movie.duration_minutes,
        'rating': movie.rating
    }), 200


'''
True if release_year's format is invalid, false otherwise
'''
def is_invalid_release_year(release_year):
    # Check if release_year is not an int (None OK since db handles nullables)
    # If release_year is an int, ensure it's in bounds
    return (not isinstance(release_year, int) and release_year is not None) or \
           (isinstance(release_year, int) and (release_year < 1000 or release_year > 9999))


'''
True if duration_minutes' format is invalid, false otherwise
'''
def is_invalid_duration_minutes(duration_minutes):
    # Check if duration_minutes is not an int (None OK since db handles nullables)
    # If duration_minutes is an int, ensure it's positive
    return (not isinstance(duration_minutes, int) and duration_minutes is not None) or \
           (isinstance(duration_minutes, int) and (duration_minutes <= 0))


'''
True if rating's format is invalid, false otherwise
'''
def is_invalid_rating(rating):
    # Check if rating is not an int (None OK since db handles nullables)
    return not isinstance(rating, int) and rating is not None