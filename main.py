from flask import Flask, render_template, url_for, request
from data import queries
import json
from operator import itemgetter
import math
from dotenv import load_dotenv


load_dotenv()
app = Flask('codecool_series')

@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)

@app.route('/design')
def design():
    return render_template('design.html')

@app.route('/shows')
def display_all_shows():
    if request.args:
        order_by, direction = request.args['order_by'], request.args['direction']
    else:
        order_by, direction = 'title', 'ASC'
    shows = queries.get_all_shows(order_by, direction)
    return render_template('all-shows.html', shows=shows, order_by=order_by, direction=direction)


@app.route('/shows/most-rated')
def display_show_most_rated():
    if request.args:
        order_by, direction, page = request.args['order_by'], request.args['direction'], int(request.args['page'])
    else:
        order_by, direction, page = 'rating', 'DESC', 1

    most_rated_shows = queries.get_top_rated_shows(page, order_by, direction)
    number_of_shows = queries.count_shows()[0]['amount']
    number_of_pages = math.ceil(number_of_shows/15)
    return render_template('top-rated.html', number_of_pages=number_of_pages, most_rated_shows=most_rated_shows, page=page, order_by=str(order_by), direction=direction)

@app.route('/show/<int:id>')
def display_show_details(id):
    show = queries.get_show_by_id(id)[0]
    seasons = queries.get_seasons_for_show(id)
    trailer = show['trailer']
    if trailer != None:
        video_id = trailer[-11:]
    else:
        video_id =""
    return render_template('details.html', show=show, id=id, seasons=seasons, video_id=video_id)

@app.route('/actors')
def get_first_hundred_actors():
    actors = queries.get_actors()
    return render_template('actors.html', actors=actors)

@app.route('/api/actors-details/<int:id>')
def get_shows_for_actors(id):
    show = queries.get_shows_for_actor(id)[0]['shows']
    return {"show" : show}

@app.route('/rated-shows')
def get_rated_shows():
    shows = queries.get_show_ratings()
    return render_template('rating.html', shows=shows)

@app.route('/api/actors')
@app.route('/api/actors/', methods=['GET'])
def filter_actors_by_genre():
    if request.args:
        genre, name = request.args['genre'], request.args['name']
    else:
        genre, name = 'Action', ''
    print(genre, name)
    return queries.filter_actors_by_genre_and_name(genre, name)


@app.route('/filter-actors')
def filter_actors():
    genres = queries.get_all_genres()
    return render_template('filter.html', genres=genres)


@app.route('/ordered-shows')
def ordered_shows():
    if request.args:
        order = request.args['order']
    else:
        order = 'DESC'
    shows = queries.get_ordered_ratings(order)
    return render_template('ordered-shows.html', shows=shows, direction=order)

@app.route('/test')
def test1():
    return render_template('test.html')

@app.route('/api/test')
def test():
    season = request.args['season']
    print(queries.filter_actors_by_genre_and_name(season))
    return queries.filter_actors_by_genre_and_name(season)

@app.route('/stars')
def get_stars():
    return render_template('stars.html')

@app.route('/api/stars')
def send_stars():
    return queries.get_twenty_actors()

@app.route('/api/stars/<int:id>')
def get_movie(id):
    return queries.get_movie(id)

@app.route('/series')
def display_series():
    return render_template('series.html')

@app.route('/api/series')
def get_series():
    return queries.get_series()

@app.route('/api/series/<id>')
def get_act_data(id):
    print(id)
    return queries.get_act_data(id)

@app.route('/show-episodes')
def get_episodes():
    return render_template('episodes.html')

@app.route('/show-episodes/<season>')
def show_episode(season):
    print(season)
    return queries.get_episodes(season)

@app.template_filter('flip_direction')
def flip_direction(direction):
    return 'ASC' if direction == 'DESC' else 'DESC'

@app.template_filter('convert_direction_to_arrow')
def convert(direction):
    if direction == 'ASC':
        return '⇧'
    else:
        return '⇩'

@app.template_filter('convert_runtime')
def convert_runtime(runtime):
    if runtime < 60:
        return f'{runtime}m'
    else:
        hours = f'{runtime//60}h' if runtime // 60 > 0 else ''
        minutes = f'{runtime % 60}m' if runtime % 60 > 0 else ''
        return hours + ' ' + minutes

def main():
    app.run(port='5000',
            host='0.0.0.0',
            debug=False)

if __name__ == '__main__':
    main()
