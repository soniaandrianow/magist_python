#!/usr/bin/python
import pymysql.cursors
from Helper import Helper
from sklearn.metrics import mean_squared_error
from math import sqrt

correct_count = 0
not_correct_count = 0
wrong_data = []

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='small_rekomendacyjny')
cur = conn.cursor()
cur.execute("SELECT * FROM help WHERE correct = 2")
actual = []
corrected = []
for row in cur:
    print(row)
    actual.append(row[6])
    corrected.append(row[5])
    correct = Helper.one_check(mov_id=row[1], us_id=row[0], rat=float(row[5]))
    print(correct)
    if not correct:
            not_correct_count += 1
            wrong_data.append([row[0], row[1], float(row[2])])
    else:
            correct_count += 1

print('Wszystkie: ' + str(cur.rowcount))
print('Poprawne: ' + str(correct_count))
print('Niepoprawne: ' + str(not_correct_count))

print('Poprawne:' + ';'.join(str(e) for e in actual))
print()
print('Poprawione: ' + ';'.join(str(f) for f in corrected))


mse = sqrt(mean_squared_error(actual, corrected))

print('Błąd: ' + str(mse))
