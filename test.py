from Helper import Helper
import pymysql.cursors
import sklearn.svm

svm = Helper.train_svm()
vector = [[2.0, 4.9]]
repared = svm.predict(vector)
print(vector)
print(repared)

#vector = Helper.prepare_vector(mov_id=4643, us_id=6, rat=1.5)
#print(vector)
#ratings = Helper.create_genres_vector(mov_id=103228, us_id=486)
#check = Helper.one_check(mov_id=4643, us_id=6, rat=1.5)
#print(ratings)

# conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='small_rekomendacyjny')
# cur = conn.cursor()
# cur.execute("SELECT * FROM rating WHERE user_id = 1 AND genre_id = 21")
# row = cur.fetchone()
# print(row)
# rowcount = cur.rowcount
# print(rowcount)
