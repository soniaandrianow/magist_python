#!/usr/bin/python
import pymysql.cursors
from Helper import Helper

correct_count = 0
not_correct_count = 0
wrong_correct_count = 0
wrong_not_correct_count = 0
wrong_data = []

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='small_rekomendacyjny')
cur = conn.cursor()
cur.execute("SELECT * FROM help WHERE checked is NULL")
svc = Helper.train_svm()
for row in cur:
    print('########################################################')
    print(row)
    correct = Helper.one_check(mov_id=row[1], us_id=row[0], rat=float(row[2]))
    print(correct)
    if not correct:
        if row[4] == '0':
            print('NOT CORRECT!!! OK')
            not_correct_count += 1
            wrong_data.append([row[0], row[1], float(row[2])])
            #Helper.repare_one(svc=svc, movie_id=row[1], user_id=row[0], rating=float(row[2]))
        else:
            print("WRONG!!! SHOULD BE CORRECT!")
            wrong_not_correct_count += 1
            wrong_data.append([row[0], row[1], float(row[2])])
            #Helper.repare_one(svc=svc, movie_id=row[1], user_id=row[0], rating=float(row[2]))
    else:
        if row[4] == '1':
            print("IT'S CORRECT!!!")
            correct_count += 1
        else:
            print("IT SHOULD BE WRONG!!!")
            wrong_correct_count += 1

print('Wszystkie: ' + str(cur.rowcount))
print('Poprawne: ' + str(correct_count))
print('Niepoprawne: ' + str(not_correct_count))
print('Poprawne uznane za błędne: ' + str(wrong_not_correct_count))
print('Błędne uznane za poprawne: ' + str(wrong_correct_count))

print()
# print('TERAZ POPRAWIAMY')
# for data in wrong_data:
#     Helper.repare_one(svc=svc, movie_id=data[1], user_id=data[0], rating=float(data[2]))
