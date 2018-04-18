import pymysql.cursors
import statistics
import math
import numpy as np
import sklearn.svm


class Helper:
    def __init__(self):
        print('new helper')

    @staticmethod
    def train_svm():
        file = open('files/train-r.txt', 'r')
        file2 = open('files/labels-r.txt', 'r')
        lines = file.readlines()
        train = []
        for line in lines:
            train.append(np.fromstring(line, dtype=float, count=2, sep=';'))
        lines2 = file2.readlines()
        labels = []
        for line in lines2:
            labels.append(line.strip('\n'))

        clf = sklearn.svm.SVC(decision_function_shape='ovr')
        clf.fit(train, labels)
        print(clf)
        return clf

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
        if len(ratings) > 0:
            genre_rating = statistics.median(ratings)
        else:
            genre_rating = 5.0
        vector = [movie_rating, genre_rating]
        return vector

    @staticmethod
    def one_check(mov_id, us_id, rat):
        user_corr = Helper.check_with_user(mov_id=mov_id, us_id=us_id, rat=rat)
        if not user_corr:
            movie_corr = Helper.check_with_movie(mov_id=mov_id, rat=rat)
            return movie_corr
        return user_corr

    @staticmethod
    def check_with_user(mov_id, us_id, rat):
        genres_ratings = Helper.create_genres_vector(mov_id=mov_id, us_id=us_id)
        print(genres_ratings)
        mean = statistics.mean(genres_ratings)
        if len(genres_ratings) >= 2:
            sigma = statistics.stdev(genres_ratings)
        else:
            sigma = genres_ratings[0]
        D = abs(rat - mean)
        print('D = ' + str(D))
        print('sigma = ' + str(sigma))
        if D < sigma * 2:
            correct = True
        else:
            correct = False
        return correct

    @staticmethod
    def check_with_movie(mov_id, rat):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='small_rekomendacyjny')
        cur_rating = conn.cursor()
        cur_rating.execute("SELECT rating FROM movie WHERE `id` = %s", mov_id)
        rating = cur_rating.fetchone()
        rating = float(rating[0])
        R = abs(rat - rating)
        print('R = ' + str(R))
        print('rating = ' + str(rating))
        if R < 0.3 * rating:
            correct = True
        else:
            correct = False
        return correct

    @staticmethod
    def create_genres_vector(mov_id, us_id):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='small_rekomendacyjny')
        cur_genres = conn.cursor()
        cur_genres.execute("SELECT genre_id FROM movie_genre WHERE `movie_id` = %s", mov_id)
        genres_ids = cur_genres.fetchall()
        genres_ratings = []
        for gid in genres_ids:
            cur_rat = conn.cursor()
            cur_rat.execute("SELECT rating FROM rating WHERE `user_id` = %s AND `genre_id` = %s", [us_id, gid])
            rating = cur_rat.fetchone()

            if rating is not None:
                rating = float(rating[0])
            else:
                rating = 3.5
            genres_ratings.append(rating)
        return genres_ratings

    @staticmethod
    def count_movie_ratings(movie):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='small_rekomendacyjny')
        cur = conn.cursor()
        cur.execute("SELECT * FROM help WHERE checked = 1 AND movie_id = movie")
        sum = 0
        counter = 0

        for row in cur:
            sum += float(row[2])
            counter += 1
        if counter > 0:
            mr = sum / counter
        else:
            mr = 3.5
        new_curr = conn.cursor()
        new_curr.execute("UPDATE movie SET rating=%s where movie_id = %s",
                         [mr, movie])
        conn.commit()

    @staticmethod
    def count_genre_ratings(us_id, gen_id, rating):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='small_rekomendacyjny')
        cur = conn.cursor()
        cur.execute("SELECT * FROM rating WHERE user_id = us_id AND genre_id => gen_id")
        row = cur.fetchone()
        rowcount = cur.rowcount

        if rowcount == 1:
            rating_new = (rating + float(row[2])) / 2
            new_curr = conn.cursor()
            new_curr.execute("UPDATE rating SET rating=%s where user_id = %s AND movie_id = %s",
                             [rating_new, row[0], row[1]])
            conn.commit()
        else:
            new_curr = conn.cursor()
            new_curr.execute("INSERT INTO rating VALUES (%s, %s, %s)",
                             [us_id, gen_id, rating])
            conn.commit()

    @staticmethod
    def repare():
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='small_rekomendacyjny')
        cur = conn.cursor()
        cur.execute("SELECT * FROM help WHERE checked is NULL AND correct = 0")
        svm = Helper.train_svm()
        for row in cur:
            print(row)
            vector = [Helper.prepare_vector(mov_id=row[1], us_id=row[0], rat=float(row[2]))]
            repared = svm.predict(vector)
            repared = float(repared[0])

            new_curr = conn.cursor()
            print('stara: ' + str(float(row[2])) + ' poprawiona: ' + str(repared))
            new_curr.execute(
                "UPDATE help SET rating=%s, checked = 1, correct = 2, where user_id = %s AND movie_id = %s",
                [repared, row[0], row[1]])
        conn.commit()

    @staticmethod
    def repare_one(svc, movie_id, user_id, rating):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='small_rekomendacyjny')
        # cur = conn.cursor()
        # cur.execute("SELECT * FROM help WHERE checked is NULL AND correct = 0")
        svm = svc
        # for row in cur:
        # print(row)
        vector = [Helper.prepare_vector(mov_id=movie_id, us_id=user_id, rat=rating)]
        print(vector)
        repared = svm.predict(vector)
        print(repared)
        repared = float(repared[0])
        new_one = round(repared + rating) / 2.0
        new_curr = conn.cursor()
        print('stara: ' + str(rating) + ' poprawiona: ' + str(new_one))
        new_curr.execute(
            "UPDATE help SET rating=%s, checked = 1, correct = 2 WHERE user_id = %s AND movie_id = %s",
            [new_one, user_id, movie_id])
        conn.commit()
