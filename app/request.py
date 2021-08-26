
import urllib.request,json
from .models import Movie,Genres,Trailer


   # Getting api key
api_key = None

# Getting the movie base url
base_url = None
genres_url = None
genre_movies_url = None

def configure_request(app):
    global api_key,base_url,genres_url,genre_movies_url
    api_key = app.config['MOVIE_API_KEY']
    base_url = app.config['MOVIE_API_BASE_URL']
    genres_url = app.config['GENRES_URL']
    genre_movies_url = app.config['GENRE_MOVIES_URL']

def get_movies(category):
    '''
    Function that gets the json response to our url request
    '''
    get_movies_url = base_url.format(category,api_key)

    with urllib.request.urlopen(get_movies_url) as url:
        get_movies_data = url.read()
        get_movies_response = json.loads(get_movies_data)

        movie_results = None

        if get_movies_response['results']:
            movie_results_list = get_movies_response['results']
            movie_results = process_results(movie_results_list)


    return movie_results

def process_results(movie_list):
    '''
    Function  that processes the movie result and transform them to a list of Objects

    Args:
        movie_list: A list of dictionaries that contain movie details

    Returns :
        movie_results: A list of movie objects
    '''
    movie_results = []
    for movie_item in movie_list:
        id = movie_item.get('id')
        title = movie_item.get('original_title')
        overview = movie_item.get('overview')
        poster = movie_item.get('poster_path')
        vote_average = movie_item.get('vote_average')
        vote_count = movie_item.get('vote_count')

        if poster:
            movie_object = Movie(id,title,overview,poster,vote_average,vote_count)
            movie_results.append(movie_object)

    return movie_results

    
def get_movie(id):
    get_movie_details_url = base_url.format(id,api_key)

    with urllib.request.urlopen(get_movie_details_url) as url:
        movie_details_data = url.read()
        movie_details_response = json.loads(movie_details_data)

        movie_object = None
        if movie_details_response:
            id = movie_details_response.get('id')
            title = movie_details_response.get('original_title')
            overview = movie_details_response.get('overview')
            poster = movie_details_response.get('poster_path')
            vote_average = movie_details_response.get('vote_average')
            vote_count = movie_details_response.get('vote_count')

            movie_object = Movie(id,title,overview,poster,vote_average,vote_count)

    return movie_object


    # We are going to implement a search functionality
def search_movie(movie_name):
    search_movie_url = 'https://api.themoviedb.org/3/search/movie?api_key={}&query={}'.format(api_key,movie_name)
    with urllib.request.urlopen(search_movie_url) as url:
        search_movie_data = url.read()
        search_movie_response = json.loads(search_movie_data)

        search_movie_results = None

        if search_movie_response['results']:
            search_movie_list = search_movie_response['results']
            search_movie_results = process_results(search_movie_list)


    return search_movie_results   


def get_genres():
    get_genres_url = genres_url.format(api_key)
    with urllib.request.urlopen(get_genres_url) as url:
        get_genres_data = url.read()
        get_genres_response = json.loads(get_genres_data)
        
        genres_results = None
        
        if get_genres_response['genres']:
            genres_results_list = get_genres_response['genres']
            genres_results = process_genres_results(genres_results_list)
        
    return genres_results

def process_genres_results(genres_results_list):
    genres_results = []
    for genre_item in genres_results_list:
        id = genre_item.get('id')
        name = genre_item.get('name')
        genre_object = Genres(id,name)
        genres_results.append(genre_object)

    return genres_results



def get_genre_movies(id):
    get_genre_movies_url = genre_movies_url.format(api_key,id)
    with urllib.request.urlopen(get_genre_movies_url) as url:
        genre_movies_data = url.read()
        genre_movies_response = json.loads(genre_movies_data)

        genre_movies_results = None

        if genre_movies_response['results']:
            genre_movies_list = genre_movies_response['results']
            genre_movies_results = process_results(genre_movies_list)
            
    return genre_movies_results

def watch_trailer(id):
    watch_movie_trailer = 'https://api.themoviedb.org/3/movie/{}/videos?api_key={}&language=en-US'.format(
        id, api_key)
    with urllib.request.urlopen(watch_movie_trailer) as url:
        search_trailer_data = url.read()
        search_trailer_response = json.loads(search_trailer_data)
        if search_trailer_response['results']:
            search_trailer_list = search_trailer_response['results']
            search_trailer_results = process_trailer(search_trailer_list)
  
    return search_trailer_results

def process_trailer(trailer_list):
    trailer_results = []
    for trailer_item in trailer_list:
        key=trailer_item.get('key')
        trailer_object = Trailer(key)
        trailer_results.append(trailer_object)
        teazer = trailer_results[0].key
    # print(teazer)
    return teazer