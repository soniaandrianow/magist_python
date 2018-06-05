from Helper import Helper
import pymysql.cursors
import time


conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='small_rekomendacyjny')
cur = conn.cursor()
cur.execute("SELECT * FROM help WHERE checked = 1 AND correct = 0")


svm = Helper.train_svm()
start_time = time.time()
for row in cur:
    print(row)
    vector = [Helper.prepare_vector(mov_id=row[1], us_id=row[0], rat=float(row[2]))]
    repared = svm.predict(vector)
    repared = float(repared[0])

    print("--- %s seconds ---" % (time.time() - start_time))
    new_curr = conn.cursor()
    print('stara: ' + str(float(row[2])) + ' poprawiona: ' + str(repared))
    new_curr.execute("UPDATE help SET corrected=%s, correct = 2 where user_id = %s AND movie_id = %s",
                     [repared, row[0], row[1]])
conn.commit()
print('END')
