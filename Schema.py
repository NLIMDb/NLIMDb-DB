from sqlalchemy import Table, Column, MetaData, ForeignKey
from sqlalchemy.dialects.sqlite import BOOLEAN, DATE, FLOAT, INTEGER, TEXT

metadata = MetaData()

people = Table('people', metadata,
    Column('birthday', DATE),
    Column('known_for_department', TEXT, nullable=False),
    Column('deathday', TEXT),
    Column('id', INTEGER, primary_key=True),
    Column('name', TEXT, nullable=False),
    Column('gender', INTEGER, nullable=False),
    Column('biography', TEXT, nullable=False),
    Column('popularity', FLOAT, nullable=False),
    Column('place_of_birth', TEXT),
    Column('profile_path', TEXT)
)

movies = Table('movies', metadata,
    Column('adult', BOOLEAN, nullable=False),
    Column('backdrop_path', TEXT),
    Column('budget', INTEGER, nullable=False),
    Column('id', INTEGER, primary_key=True),
    Column('overview', TEXT),
    Column('popularity', FLOAT, nullable=False),
    Column('poster_path', TEXT),
    Column('release_date', DATE),
    Column('revenue', INTEGER, nullable=False),
    Column('runtime', INTEGER),
    Column('tagline', TEXT),
    Column('title', TEXT, nullable=False),
    Column('vote_average', FLOAT, nullable=False),
    Column('vote_count', INTEGER, nullable=False)
)

movie_series = Table('movie_series', metadata,
    Column('id' , INTEGER, primary_key=True),
    Column('name', TEXT, nullable=False),
    Column('overview', TEXT, nullable=False),
    Column('poster_path', TEXT),
    Column('backdrop_path', TEXT)
)

genres = Table('genres', metadata,
    Column('id', INTEGER, primary_key=True),
    Column('name', TEXT, nullable=False),
    Column('movie_id', INTEGER, ForeignKey('movies.id', ondelete='CASCADE'))
)

videos = Table('videos', metadata,
    Column('id', TEXT, primary_key=True),
    Column('key', TEXT, nullable=False),
    Column('name', TEXT, nullable=False),
    Column('type', TEXT),
    Column('movie_id', INTEGER, ForeignKey('movies.id', ondelete='CASCADE'))
)

cast_in_movie = Table('cast_in_movie', metadata,
    Column('character', TEXT, nullable=False),
    Column('movie_id', INTEGER, ForeignKey('movies.id', ondelete='CASCADE')),
    Column('person_id', INTEGER, ForeignKey('people.id', ondelete='CASCADE'))
)

crew_in_movie = Table('crew_in_movie', metadata,
    Column('department', TEXT, nullable=False),
    Column('job', TEXT, nullable=False),
    Column('movie_id', INTEGER, ForeignKey('movies.id', ondelete='CASCADE')),
    Column('person_id', INTEGER, ForeignKey('people.id', ondelete='CASCADE'))
)

part_of_series = Table('part_of_series', metadata,
    Column('movie_series_id' , INTEGER, ForeignKey('movie_series.id', ondelete='CASCADE')),
    Column('movie_id' , INTEGER, ForeignKey('movies.id', ondelete='CASCADE'))
)