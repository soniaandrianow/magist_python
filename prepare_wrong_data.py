#!/usr/bin/python

import pymysql.cursors
import sklearn.svm
import numpy as np
from Helper import Helper
import random
import math

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='small_rekomendacyjny')
cur = conn.cursor()
cur.execute("SELECT * FROM help WHERE correct = 1 AND checked is NULL ORDER BY RAND() LIMIT 100")

file = open('files/train.txt', 'r')
file2 = open('files/labels.txt', 'r')
lines = file.readlines()
train = []
for line in lines:
    train.append(np.fromstring(line, dtype=float, count=3, sep=';'))
lines2 = file2.readlines()
labels = []
for line in lines2:
    labels.append(line.strip('\n'))

clf = sklearn.svm.SVC(decision_function_shape='ovr')
clf.fit(train, labels)
print(clf)

for row in cur:
    vector = [Helper.prepare_vector(mov_id=row[1], us_id=row[0], rat=float(row[2]))]
    predicted = clf.predict(vector)
    predicted = float(predicted[0])
    print(predicted)
    if predicted:
        add = random.randint(0, 1)
        if 5.0 - predicted <= 2.0:
            value = 2.0
        else:
            value = random.randint(2, 5.0 - math.ceil(predicted))
        if add == 1:
            new = predicted + value
            if new > 5.0:
                new = predicted - value
        else :
            new = predicted - value
            if new < 0.5:
                new = predicted + value
    new_curr = conn.cursor()
    new_curr.execute("UPDATE help SET rating=%s, correct = 0 where user_id = %s AND movie_id = %s", [new, row[0], row[1]])
conn.commit()

file.close()
file2.close()