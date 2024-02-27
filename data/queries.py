from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_all_shows(category, direction):
    return data_manager.execute_select(f'''
        SELECT
            shows.id,
            shows.title as title,
            shows.year,
            shows.runtime,
            ROUND( rating, 1 ) as rating,
            STRING_AGG(genres.name,',' ORDER BY genres.name) AS genres,
            shows.trailer,
            shows.homepage
        FROM shows
        LEFT JOIN show_genres on shows.id = show_genres.show_id
        LEFT JOIN genres on show_genres.genre_id = genres.id
        GROUP BY  shows.id
        ORDER BY {category} {direction};
        ''', variables={"category": category, "direction": direction})


def get_top_rated_shows(page, category, direction):
    return data_manager.execute_select(f'''SELECT shows.id,
        shows.title,
        shows.year,
        shows.runtime,
        ROUND( shows.rating, 1 ) as rating,
        STRING_AGG(genres.name,',' ORDER BY genres.name) AS genres,
        shows.trailer,
        shows.homepage
        FROM shows
        LEFT JOIN show_genres ON shows.id = show_genres.show_id
        LEFT JOIN genres on show_genres.genre_id = genres.id
        GROUP BY shows.id
        ORDER BY {category} {direction}
        OFFSET ((%(page)s - 1) * 15)
        LIMIT 15;''', variables={"page": page, "category": category, "direction": direction})


def count_shows():
    return data_manager.execute_select(''' SELECT COUNT(id) AS amount FROM shows;''')


def get_show_by_id(id):
    return data_manager.execute_select(f'''SELECT shows.title,
       shows.runtime,
       ROUND( shows.rating, 1 ) as rating,
       genre.genres as genres,
       shows.overview,
       string_agg(stars.name, ',') as stars,
       shows.trailer
       FROM shows
       LEFT JOIN (
            SELECT show_id, string_agg(genres.name, ', ' ORDER BY genres.name) as genres
            FROM genres
            JOIN show_genres on genres.id = show_genres.genre_id
            GROUP BY show_id
            ) as genre on shows.id = genre.show_id
       LEFT JOIN (
            SELECT show_id, name
            FROM actors
            JOIN show_characters on actors.id = show_characters.actor_id
            WHERE show_id = %(id)s
            GROUP BY show_id, name, show_characters.id
            ORDER BY show_characters.id
            FETCH FIRST 3 ROWS ONLY
            ) as stars on stars.show_id = shows.id
        WHERE shows.id = %(id)s
        GROUP BY shows.id, shows.title, shows.runtime, shows.rating, genre.genres, shows.overview, shows.trailer;''',
                                       variables={"id": id})


def get_seasons_for_show(id):
    return data_manager.execute_select(f'''SELECT season_number, 
        title, 
        overview 
        FROM seasons
        WHERE show_id = {id}
        ORDER BY season_number;''', variables={'id': id})


def get_actors():
    return data_manager.execute_select(f'''SELECT id, split_part(actors.name,' ', 1) as first_name 
        FROM actors
        ORDER BY actors.birthday
        LIMIT 100;''')


def get_shows_for_actor(id):
    return data_manager.execute_select(f'''SELECT split_part(actors.name,' ', 1) as first_name, 
        string_agg(shows.title, ', ') as shows FROM actors
        JOIN show_characters on actors.id = show_characters.actor_id
        JOIN shows on show_characters.show_id = shows.id
        WHERE actors.id = {id}
        GROUP BY actors.name;''', variables={'id': id})


def get_show_ratings():
    return data_manager.execute_select(f'''SELECT title, to_char(round((rating - avg), 2), 'SG0.99') as diff, 
        count(a.name) as actor_count FROM shows
        JOIN show_characters sc on shows.id = sc.show_id
        JOIN actors a on a.id = sc.actor_id
        CROSS JOIN (
        SELECT avg(rating) as avg from shows) as all_ratings
        GROUP BY title, rating, all_ratings.avg
        ORDER BY actor_count DESC
        FETCH FIRST 10 ROWS ONLY''')


def get_ordered_ratings(order):
    return data_manager.execute_select(f'''SELECT shows.title, round(shows.rating, 2) AS rating, count(seasons.title) as episodes
        FROM shows
        JOIN seasons on shows.id = seasons.show_id
        JOIN episodes on episodes.season_id = seasons.id
        GROUP BY shows.title, shows.rating
        ORDER BY episodes {order}
        FETCH FIRST 10 ROWS ONLY;''', variables={'order': order})


def get_ordered_ratings(order):
    return data_manager.execute_select(f'''
        SELECT title, (round(rating)) AS rating FROM shows
        ORDER BY shows.rating {order}
        FETCH FIRST 10 ROWS ONLY;''', variables={'order': order})


def get_all_genres():
    return data_manager.execute_select(f'''SELECT DISTINCT genres.id, name from genres
        INNER JOIN show_genres on genres.id = show_genres.genre_id
        ORDER BY name;''')


def filter_actors_by_genre_and_name(genre, name):
    name = "%" + name + "%"
    return data_manager.execute_select(f'''SELECT actors.name, genres.name as genre from actors
        JOIN show_characters on actors.id = show_characters.actor_id
        JOIN shows on show_characters.show_id = shows.id
        JOIN show_genres on shows.id = show_genres.show_id
        JOIN genres on show_genres.genre_id = genres.id
        WHERE genres.name = %(genre)s and actors.name LIKE %(name)s
        GROUP BY actors.name ,genres.name
        LIMIT 20;''',
                                       variables={'genre': genre, 'name': name})


def filter_actors_by_genre_and(season):
    return data_manager.execute_select(f'''SELECT episodes.title as overview, 
    seasons.title from seasons
    Join episodes on seasons.id = episodes.season_id
    join shows on seasons.show_id = shows.id
    where shows.title = 'The Penguins of Madagascar' and seasons.title = %(season)s;''',
                                       variables={'season': season})


def get_twenty_actors():
    return data_manager.execute_select(f'''Select actors.id, actors.name, actors.birthday, count(show_characters.show_id) as count
        from actors
        join show_characters on actors.id = show_characters.actor_id
        GROUP BY actors.id
        Order by count desc
        limit 20;''')


def get_movie(id):
    return data_manager.execute_select(f'''Select actors.id, string_agg(shows.title, ', ' ORDER BY shows.title)
        from actors
        join show_characters on actors.id = show_characters.actor_id
        join shows on show_characters.show_id = shows.id
        where actors.id = {id}
        GROUP BY actors.id
        Order by count(show_characters.show_id) desc
        limit 20;''', variables={'id': id})


def get_series():
    return data_manager.execute_select(f'''SELECT show_characters.actor_id, show_characters.character_name
        FROM show_characters
        JOIN shows on show_characters.show_id = shows.id
        Where shows.title = 'House'
''')


def get_act_data(id):
    return data_manager.execute_select(f'''SELECT show_characters.character_name, actors.name, actors.birthday
                FROM show_characters
                    JOIN shows on show_characters.show_id = shows.id
                    join actors on show_characters.actor_id = actors.id
                    Where shows.title = 'House' and show_characters.character_name = %(id)s;''', variables={'id': id})


def get_episodes(season):
    return data_manager.execute_select(f'''SELECT episodes.title, episodes.overview
            FROM episodes
            Join seasons on episodes.season_id = seasons.id
            JOIN shows on seasons.show_id = shows.id
            Where shows.title = 'House' and seasons.title = %(season)s;''', variables={'season': season})
