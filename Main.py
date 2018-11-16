import os
import json
import gzip
import shutil
import time
import requests
import argparse
import traceback
from datetime import datetime
from sqlalchemy import create_engine, func, select

import Schema
import Insert

NOW = datetime.now()

API_KEY = ''

PATHS = ['movie_ids',
         'collection_ids',
         'person_ids']

def download_file_exports():
    for path in PATHS:
        arg = '{}_{}_{}_{}.json.gz'.format(path, str(NOW.month).zfill(2), str(NOW.day - 1).zfill(2), NOW.year)
        url = 'http://files.tmdb.org/p/exports/{}'.format(arg)

        req = requests.get(url)

        formatted_path = '{}/{}.json.gz'.format('temp', path)
        formatted_path_without_ext = formatted_path.replace('.gz', '')

        if req.status_code == 200:
            with open(formatted_path, 'wb') as f:
                f.write(req.content)

            # Uncompress downloaded files
            with gzip.open(formatted_path, 'r') as f_in, open(formatted_path_without_ext, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

            os.remove(formatted_path)
        else:
            print(req.text)

def connect_to_db(name):
    try:
        engine = create_engine('sqlite:///{}'.format(name), echo=False)
        return engine
    except Exception as e:
        print(e)

def create_tables(engine):
    try:
        Schema.metadata.create_all(engine)
    except Exception as e:
        print(e)

def populate_movies(engine, latest_movie_id):
    conn = engine.connect()

    with open('{}/{}.json'.format('temp', PATHS[0])) as f:
        lines = f.readlines()

        start_time = time.time()
        request_count = 0

        try:
            for line in lines:
                movie_id = json.loads(line)['id']
                
                if movie_id > latest_movie_id:
                    url = 'https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US&append_to_response=videos'.format(movie_id, API_KEY)

                    req = requests.get(url)
                    request_count += 1
                    print(url)

                    if request_count >= 38:
                        duration = time.time() - start_time
                        if duration < 10:
                            time.sleep(10 - duration)

                        start_time = time.time()
                        request_count = 0

                    if(req.status_code == 200):
                        res = json.loads(req.text)

                        conn.execute(Insert.insert_movie(res))

                        for genre in res['genres']:
                            conn.execute(Insert.insert_movie_genre(genre, movie_id))

                        for video in res['videos']['results']:
                            conn.execute(Insert.insert_video(video, movie_id))
                    else:
                        print(req.text)
        except:
            print(traceback.print_exc())
        finally:
            f.close()
            conn.close()
            
def populate_collection(engine, latest_movie_collection_id):
    conn = engine.connect()
    
    with open('{}/{}.json'.format('temp', PATHS[1])) as f:
        lines = f.readlines()

        start_time = time.time()
        request_count = 0

        try:
            for line in lines:
                collection_id = json.loads(line)['id']

                if collection_id > latest_movie_collection_id:
                    url = 'https://api.themoviedb.org/3/collection/{}?api_key={}&language=en-US'.format(collection_id, API_KEY)

                    req = requests.get(url)
                    request_count += 1
                    print(url)

                    if request_count >= 38:
                        duration = time.time() - start_time
                        if duration < 10:
                            time.sleep(10 - duration)

                        start_time = time.time()
                        request_count = 0

                    if(req.status_code == 200):
                        res = json.loads(req.text)

                        conn.execute(Insert.insert_movie_series(res))

                        for movie in res['parts']:
                            conn.execute(Insert.insert_part_of_series(res, movie['id']))
                    else:
                        print(req.text)
        except:
            print(traceback.print_exc())
        finally:
            f.close()
            conn.close()
                                
def populate_person(engine, latest_person_id):
    conn = engine.connect()

    with open('{}/{}.json'.format('temp', PATHS[2])) as f:
        start_time = time.time()
        request_count = 0

        try:
            for line in f.readlines():
                person_id = json.loads(line)['id']
                
                if person_id > latest_person_id:
                    url = 'https://api.themoviedb.org/3/person/{}?api_key={}&language=en-US&append_to_response=movie_credits'.format(person_id, API_KEY)

                    req = requests.get(url)
                    request_count += 1
                    print(url)

                    if request_count >= 38:
                        duration = time.time() - start_time
                        if duration < 10:
                            time.sleep(10 - duration)

                        start_time = time.time()
                        request_count = 0

                    if(req.status_code == 200):
                        res = json.loads(req.text)

                        conn.execute(Insert.insert_person(res))
                         
                        for cast in res['movie_credits']['cast']:
                            conn.execute(Insert.insert_movie_cast(cast, person_id))

                        for crew in res['movie_credits']['crew']:
                            conn.execute(Insert.insert_movie_crew(crew, person_id))
                    else:
                        print(req.text)
        except:
            print(traceback.print_exc())
        finally:
            f.close()
            conn.close()

def main():
    if not os.path.isdir('temp'):
        os.mkdir('temp')
    
        download_file_exports()
        
    if os.path.isfile('NLIM.db'):
        engine = connect_to_db('NLIM.db')

        conn = engine.connect()

        latest_movie_id = conn.execute(select([func.max(Schema.movies.c.id)])).fetchone()[0] 
        latest_movie_collection_id = conn.execute(select([func.max(Schema.movie_series.c.id)])).fetchone()[0]
        latest_person_id = conn.execute(select([func.max(Schema.people.c.id)])).fetchone()[0]

        populate_movies(engine, latest_movie_id if latest_movie_id is not None else -1)
        populate_collection(engine, latest_movie_collection_id if latest_movie_collection_id is not None else -1)
        populate_person(engine, latest_person_id if latest_person_id is not None else -1)

    else:
        engine = connect_to_db('NLIM.db')

        create_tables(engine)
    
        populate_movies(engine, -1)
        populate_collection(engine, -1)
        populate_person(engine, -1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--api-key', dest='api_key', type=str, required=True, help='The Movie DB API Key')
    args = parser.parse_args()
    
    API_KEY = args.api_key.strip()

    main()