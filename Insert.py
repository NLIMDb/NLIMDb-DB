import Schema
from datetime import datetime

# pylint: disable=no-value-for-parameter

def insert_movie(val):
    if type(val['release_date']) is str and len(val['release_date']) > 0:
        release_date = datetime.strptime(val['release_date'], "%Y-%m-%d")
    else:
        release_date = None

    return Schema.movies.insert().values(
        adult = val['adult'],
        backdrop_path = val['backdrop_path'],
        budget = val['budget'],
        id = val['id'],
        overview = val['overview'],
        popularity = val['popularity'],
        poster_path = val['poster_path'],
        release_date = release_date,
        revenue = val['revenue'],
        runtime = val['runtime'],
        tagline = val['tagline'],
        title = val['title'],
        vote_average = val['vote_average'],
        vote_count = val['vote_count']
    )

def insert_movie_genre(val, movie_id):
    return Schema.genres.insert().values(
        name = val['name'],
        movie_id = movie_id
    )

def insert_video(val, movie_id):
    return Schema.videos.insert().values(
        id = val['id'],
        key = val['key'],
        name = val['name'],
        type = val['type'],
        movie_id = movie_id
    )

def insert_movie_series(val):
    return Schema.movie_series.insert().values(
        id = val['id'],
        name = val['name'],
        overview = val['overview'],
        poster_path = val['poster_path'],
        backdrop_path = val['backdrop_path']
    )

def insert_part_of_series(val, movie_id):
    return Schema.part_of_series.insert().values(
        movie_series_id = val['id'],
        movie_id = movie_id
    )

def insert_person(val):
    if type(val['deathday']) is str and len(val['deathday']) > 0:
        deathday = datetime.strptime(val['deathday'], "%Y-%m-%d")
    else:
        deathday = None

    if type(val['birthday']) is str and len(val['birthday']) > 0:
        birthday = datetime.strptime(val['birthday'], "%Y-%m-%d")
    else:
        birthday = None

    return Schema.people.insert().values(
        birthday = birthday,
        known_for_department = val['known_for_department'],
        deathday = deathday,
        id = val['id'],
        name = val['name'],
        gender = val['gender'],
        biography = val['biography'],
        popularity = val['popularity'],
        place_of_birth = val['place_of_birth'],
        profile_path = val['profile_path']
    )

def insert_movie_cast(val, person_id):
    return Schema.cast_in_movie.insert().values(
        character = val['character'] if 'character' in val else '',
        movie_id = val['id'],
        person_id = person_id
    )

def insert_movie_crew(val, person_id):
    return Schema.crew_in_movie.insert().values(
        department = val['department'] if 'department' in val else '',
        job = val['job'] if 'job' in val else '',
        movie_id = val['id'],
        person_id = person_id
    )