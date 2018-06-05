#!/usr/bin/python

import pymysql.cursors
import sklearn.svm
import numpy as np
from Helper import Helper
import random
import math
from Helper import Helper

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='small_rekomendacyjny')
cur = conn.cursor()
cur.execute("SELECT * FROM help WHERE correct = 1 "
            "AND movie_id not in (1, 4, 5, 7, 8, 19, 22, 26, 28, 30, 31, 32, 36, 37, 46, 47) "
            "AND checked = 5 ORDER BY RAND() LIMIT 50")

for row in cur:
    add = random.randint(0, 1)
    if 10.0 - float(row[2]) <= 4.0:
        value = 4.0
    else:
        value = float(random.randint(4, 10.0 - float(row[2])))
    if add == 1:
        new = float(row[2]) + value
        if new > 10.0:
            new = float(row[2]) - value
    else:
        new = float(row[2]) - value
        if new < 1:
            new = float(row[2]) + value

    # if 5 - float(row[2]) <= 2.5:
    #     value = 2.5
    # else:
    #     value = float(random.randint(2, 5.0 - float(row[2])))
    # if add == 1:
    #     new = float(row[2]) + value
    #     if new > 5.5:
    #         new = float(row[2]) - value
    # else:
    #     new = float(row[2]) - value
    #     if new < 0.5:
    #         new = float(row[2]) + value

    new_curr = conn.cursor()
    print('stara: ' + str(float(row[2])) + ' nowa: ' + str(new))
    new_curr.execute("UPDATE help SET rating=%s, correct = 0 WHERE user_id = %s AND movie_id = %s", [new, row[0], row[1]])
conn.commit()

