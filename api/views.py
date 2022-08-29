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

    title = request.get_json().get('title')
    description = request.get_json().get('description')
    release_year = request.get_json().get('release_year')
    duration_minutes = request.get_json().get('duration_minutes')
    rating = request.get_json().get('rating')

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

    title = request.get_json().get('title')
    description = request.get_json().get('description')
    release_year = request.get_json().get('release_year')
    duration_minutes = request.get_json().get('duration_minutes')
    rating = request.get_json().get('rating')

    if title:
        movie.title = title
    if description:
        movie.description = description
    if release_year:
        movie.release_year = release_year
    if duration_minutes:
        movie.duration_minutes = duration_minutes
    if rating:
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