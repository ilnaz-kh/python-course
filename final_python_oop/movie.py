import requests
from configparser import ConfigParser 
from configparser import Error
from exceptions import FileError, MovieError

class Movie:
    def __init__(self, file):
        self.file = file

    
    def save_movie(self, movie_id, title, original_language, overview, genres, runtime, vote_average, vote_count, release_date):
            data_dict = {
                'movie_id': movie_id,
                'title': title,
                'original_language': original_language,
                'overview': overview,
                'genres': genres,
                'runtime': runtime,
                'vote_average': vote_average,
                'vote_count': vote_count,
                'release_date': release_date
            }
            ## save the user's informations to the associated file
            self.file.save_data('Movie', data_dict)


    def fetch_save_movie(self, query):
        ## Get the API KEY from a config.ini file
        try:
            configur = ConfigParser() 
            configur.read('config.ini')
            API_KEY = configur['Movie']['API_KEY']
            API_URL = "https://api.themoviedb.org/3/search/movie"
            params = {'query': query,
                    'api_key': API_KEY}
            
            response = requests.get(API_URL, params=params)
            if response.status_code == 200:
                movie_items = response.json()
                if movie_items['results']:
                    movie_dict = movie_items['results'][0] # return the first movie in the results
                    movie_id = str(movie_dict['id'])
                    ## request for the second time to fetch more details about movie using movie id:
                    API_URL = "https://api.themoviedb.org/3/movie/" + movie_id + "?api_key=" + API_KEY
                    response = requests.get(API_URL)
                    if response.status_code == 200:
                        movie_details = response.json()
                        ## 
                        genres_details = movie_details.get('genres', []) # a list of dictionaries: [{'id': 35, 'name': 'Comedy'}, {'id': 10749, 'name': 'Romance'}]
                        genre = [item['name'] for item in genres_details] # a list of genre names
                        ## save data
                        self.save_movie(
                            movie_id= movie_id, title= movie_details.get('title', ""),
                            original_language = movie_details.get('original_language', ""),
                            overview = movie_details.get('overview', ""),
                            genres = genre, 
                            runtime= movie_details.get('runtime', None),
                            vote_average = movie_details.get('vote_average', None),
                            vote_count = movie_details.get('vote_count', None),
                            release_date = movie_details.get('release_date', None)
                        )
                    else:
                        print("Cannot fetch the details of the movie") 
                else:
                    print("Nothing found! Please use another term to search")
            else:
                print("Failed! Cannot connect to the API")
        except FileError as e:
            raise MovieError(e.__str__())
        except Error as e: # configparser Error
            raise MovieError(e.__str__())
        except Exception as e:
            raise MovieError(f"{e.__class__.__name__}: {e.__str__()}")
