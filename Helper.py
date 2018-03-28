import pymysql.cursors
import statistics

class Helper:
    def __init__(self):
        print('new helper')

    @staticmethod
    def prepare_vector(mov_id, us_id, rat):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='small_rekomendacyjny')
        cur = conn.cursor()
        cur.execute("SELECT rating FROM movie WHERE id = %s", mov_id)
        for row in cur:
            movie_rating = (float(row[0]))
        cur.execute("SELECT genre_id FROM movie_genre WHERE `movie_id` = %s", mov_id)
        genres_ids = cur.fetchall()
        cur.execute("SELECT rating FROM rating WHERE `user_id` = %s AND `genre_id` IN %s", [us_id, genres_ids])
        ratings = []
        for row in cur:
            ratings.append(float(row[0]))
        if ratings:
            genre_rating = statistics.median(ratings)
        else: genre_rating = 3.5
        vector = [rat, movie_rating, genre_rating]
        return vector


